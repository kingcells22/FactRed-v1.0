from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas, database, models
import re 
import routeros_api
from netmiko import ConnectHandler

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- TRADUCTOR DE PLANES ---
def parse_speed(plan_name: str):
    if not plan_name:
        return "5M/5M" 

    match = re.search(r'\d+', plan_name)
    if match:
        speed = match.group()
        return f"{speed}M/{speed}M"
    else:
        return "10M/10M"

# =========================================================
# EL "CEREBRO" MULTIMARCA (DESPACHADOR DINÁMICO)
# =========================================================
def provision_client(db: Session, client: models.Client, action: str):
    """
    actions: 'create', 'update', 'suspend', 'activate', 'cancel', 'delete'
    """
    if not client.network_device_id or not client.ip_address:
        return # Si no tiene equipo o IP asignada, no hacemos nada en la red
    
    device = db.query(models.NetworkDevice).filter(models.NetworkDevice.id == client.network_device_id).first()
    if not device:
        return

    speed = parse_speed(client.plan_type)
    full_name = f"{client.first_name} {client.last_name}"

    # ------------------- LÓGICA MIKROTIK -------------------
    if device.vendor == "MikroTik":
        try:
            conn = routeros_api.RouterOsApiPool(
                device.ip_address, username=device.username, password=device.password, port=8728, plaintext_login=True
            )
            api = conn.get_api()

            # 1. Gestionar Velocidad (Simple Queues)
            if action in ["create", "update", "activate"]:
                queues = api.get_resource('/queue/simple')
                existing_q = queues.get(target=f"{client.ip_address}/32")
                if existing_q:
                    queues.set(id=existing_q[0]['id'], max_limit=speed, name=full_name)
                else:
                    queues.add(name=full_name, target=f"{client.ip_address}/32", max_limit=speed)
            elif action in ["delete", "cancel"]:
                queues = api.get_resource('/queue/simple')
                existing_q = queues.get(target=f"{client.ip_address}/32")
                if existing_q: 
                    queues.remove(id=existing_q[0]['id'])

            # 2. Gestionar Cortes (Address Lists)
            addr_list = api.get_resource('/ip/firewall/address-list')
            existing_a = addr_list.get(address=client.ip_address)
            
            # Limpiamos al cliente de cualquier lista de castigo primero
            for item in existing_a:
                if item.get('list') in ['MOROSOS_FACTRED', 'SUSPENDIDOS_FACTRED']:
                    addr_list.remove(id=item['id'])
            
            # Si la acción es castigar, lo metemos en la lista correspondiente
            if action == "suspend":
                addr_list.add(list="MOROSOS_FACTRED", address=client.ip_address, comment=f"Corte: {full_name}")
            elif action == "cancel":
                addr_list.add(list="SUSPENDIDOS_FACTRED", address=client.ip_address, comment=f"Cancelado: {full_name}")

            conn.disconnect()
        except Exception as e:
            print(f"Error provisionando en MikroTik: {str(e)}")

    # ------------------- LÓGICA FORTINET -------------------
    elif device.vendor == "Fortinet":
        try:
            # Aumentamos el timeout y el delay para evitar el error "Pattern not detected"
            net_connect = ConnectHandler(
                device_type='fortinet', 
                host=device.ip_address, 
                username=device.username, 
                password=device.password, 
                timeout=15,             # Más tiempo para negociar SSH
                global_delay_factor=2   # Factor de espera entre comandos
            )
            
            # Nombre dinámico del objeto basado en la IP del cliente
            obj_name = f"FACTRED_{client.ip_address}"
            cmds = []

            # 1. Gestión de Objeto de Dirección (Crear/Actualizar)
            if action in ["create", "activate", "update", "suspend"]:
                cmds.extend([
                    "config firewall address",
                    f"edit \"{obj_name}\"",
                    "set type ipmask",
                    f"set subnet {client.ip_address} 255.255.255.255",
                    "next",
                    "end"
                ])

            # 2. Lógica de Suspensión (Meter al grupo de morosos)
            if action in ["suspend", "cancel"]:
                cmds.extend([
                    "config firewall addrgrp",
                    "edit \"MOROSOS_FACTRED\"",
                    f"append member \"{obj_name}\"",
                    "next",
                    "end"
                ])

            # 3. Lógica de Activación (Sacar del grupo de morosos)
            if action == "activate":
                cmds.extend([
                    "config firewall addrgrp",
                    "edit \"MOROSOS_FACTRED\"",
                    f"unselect member \"{obj_name}\"",
                    "next",
                    "end"
                ])

            # 4. Limpieza total (Eliminar objeto si el cliente se borra)
            if action == "delete":
                cmds.extend([
                    "config firewall addrgrp",
                    "edit \"MOROSOS_FACTRED\"",
                    f"unselect member \"{obj_name}\"",
                    "next",
                    "end",
                    "config firewall address",
                    f"delete \"{obj_name}\"",
                    "end"
                ])

            # Ejecutamos todo el bloque de comandos de una vez (SIN el expect_string)
            if cmds:
                net_connect.send_config_set(cmds, cmd_verify=False)

            # CERRAMOS CONEXIÓN
            net_connect.disconnect()
            
        # MANEJO DE ERRORES (Obligatorio para que no se caiga FastAPI)
        except Exception as e:
            print(f"Error provisionando en Fortinet ({client.ip_address}): {str(e)}")

# =========================================================
# RUTAS ESTANDAR
# =========================================================

@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_identity(db, identity_doc=client.identity_doc)
    if db_client:
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese Documento.")
    
    new_client = crud.create_client(db=db, client=client)
    provision_client(db, new_client, "create") # Llamamos al cerebro
    
    return new_client

@router.get("/", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, search: Optional[str] = None, db: Session = Depends(get_db)):
    clients = crud.get_clients(db, skip=skip, limit=limit, search=search)
    return clients

@router.get("/{client_id}", response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.put("/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, client: schemas.ClientUpdate, db: Session = Depends(get_db)):
    db_client = crud.update_client(db, client_id=client_id, client=client)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
        
    provision_client(db, db_client, "update") # Llamamos al cerebro
    return db_client

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client:
        provision_client(db, db_client, "delete") # Limpiamos el router primero
        
    crud.delete_client(db, client_id=client_id)
    return {"ok": True}

# =========================================================
# RUTAS DE GESTION ISP
# =========================================================

@router.post("/{client_id}/suspend")
def suspend_service(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    client.service_status = "Suspended"
    db.commit()
    
    provision_client(db, client, "suspend")
    return {"message": f"Servicio suspendido para {client.first_name}"}

@router.post("/{client_id}/activate")
def activate_service(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    client.service_status = "Active"
    db.commit()
    
    provision_client(db, client, "activate")
    return {"message": f"Servicio activado para {client.first_name}"}

@router.post("/{client_id}/cancel")
def cancel_service(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    client.service_status = "Cancelled"
    db.commit()
    
    provision_client(db, client, "cancel")
    return {"message": "Servicio cancelado"}