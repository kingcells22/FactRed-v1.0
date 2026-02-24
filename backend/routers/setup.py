from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from netmiko import ConnectHandler 
import models, schemas, database
import routeros_api 
import re # Para procesar texto de Fortinet

router = APIRouter(
    prefix="/setup",
    tags=["Setup"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class InjectOptions(BaseModel):
    mode: str 
    base_lan: str = "192.168.100.1/24"

# ---------------------------------------------------------
# 2. STATUS
# ---------------------------------------------------------
@router.get("/status", response_model=schemas.SetupStatus)
def check_setup_status(db: Session = Depends(get_db)):
    settings = db.query(models.Settings).first()
    if not settings:
        return {"is_installed": False, "company_name": "FactRed"}
    return {"is_installed": settings.is_installed, "company_name": settings.company_name}

# ---------------------------------------------------------
# 3. INSTALL (MODIFICADO PARA FORTINET)
# ---------------------------------------------------------
@router.post("/install")
def run_installation(data: schemas.SetupCreate, db: Session = Depends(get_db)):
    existing_settings = db.query(models.Settings).first()
    
    try:
        if data.vendor == 'mikrotik':
            connection = routeros_api.RouterOsApiPool(
                data.mikrotik_ip, username=data.mikrotik_user, password=data.mikrotik_password,
                port=data.mikrotik_port, plaintext_login=True
            )
            api = connection.get_api()
            connection.disconnect() 
            
        else:
            # Netmiko soporta 'fortinet' y 'cisco_ios'
            device = {
                'device_type': data.vendor, 
                'host': data.mikrotik_ip,
                'username': data.mikrotik_user, 
                'password': data.mikrotik_password,
                'port': data.mikrotik_port, 
                'timeout': 15, # Aumentado para mayor tolerancia
                'global_delay_factor': 2 # Factor de paciencia para el prompt
            }
            net_connect = ConnectHandler(**device)
            net_connect.disconnect()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error conectando con {data.vendor.upper()}: {str(e)}")

    new_settings = existing_settings if existing_settings else models.Settings()

    new_settings.vendor = data.vendor
    new_settings.company_name = data.company_name
    new_settings.is_installed = True 

    # Guardado inteligente por marca
    if data.vendor == 'fortinet':
        new_settings.fortinet_ip = data.mikrotik_ip
        new_settings.fortinet_user = data.mikrotik_user
        new_settings.fortinet_password = data.mikrotik_password
        new_settings.fortinet_port = data.mikrotik_port or 22
        new_settings.fortinet_enabled = True
    else:
        new_settings.mikrotik_ip = data.mikrotik_ip
        new_settings.mikrotik_user = data.mikrotik_user
        new_settings.mikrotik_password = data.mikrotik_password
        new_settings.mikrotik_port = data.mikrotik_port

    db.add(new_settings)

    try:
        admin_user = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin_user:
            admin_user = models.User(username="admin", password=data.new_admin_password, is_active=True)
        else:
            admin_user.password = data.new_admin_password
        db.add(admin_user)
    except Exception as e:
        print(f"Error gestionando usuario: {e}")
    
    db.commit()
    return {"message": "Conexion exitosa. Equipo guardado."}

# ---------------------------------------------------------
# 4. ESCANER (INTEGRADO FORTINET)
# ---------------------------------------------------------
@router.get("/scan-mikrotik") 
def scan_device(db: Session = Depends(get_db)):
    settings = db.query(models.Settings).first()
    if not settings: raise HTTPException(status_code=400, detail="Equipo no configurado.")

    is_virgin = False; interfaces_count = 0; nat_count = 0

    try:
        if settings.vendor == 'mikrotik':
            connection = routeros_api.RouterOsApiPool(
                settings.mikrotik_ip, username=settings.mikrotik_user, password=settings.mikrotik_password,
                port=settings.mikrotik_port, plaintext_login=True
            )
            api = connection.get_api()
            interfaces = api.get_resource('/ip/address').get()
            nats = api.get_resource('/ip/firewall/nat').get()
            connection.disconnect()
            interfaces_count = len(interfaces); nat_count = len(nats); is_virgin = (nat_count == 0)

        elif settings.vendor == 'fortinet':
            device = {
                'device_type': 'fortinet', 'host': settings.fortinet_ip,
                'username': settings.fortinet_user, 'password': settings.fortinet_password,
                'port': settings.fortinet_port or 22,
                'global_delay_factor': 2 # Añadido por seguridad
            }
            net_connect = ConnectHandler(**device)
            # Escaneo de interfaces físicas y políticas de firewall
            out_int = net_connect.send_command("get system interface physical")
            out_pol = net_connect.send_command("show firewall policy")
            net_connect.disconnect()
            
            interfaces_count = len(re.findall(r"== \[.*\]", out_int))
            nat_count = out_pol.count("edit")
            is_virgin = (nat_count <= 2) # Los FortiGate traen reglas base

        return { "is_virgin": is_virgin, "interfaces_count": interfaces_count, "nat_count": nat_count }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo al auditar {settings.vendor}: {str(e)}")

# ---------------------------------------------------------
# 5. ORQUESTADOR (SMART INJECT FORTINET)
# ---------------------------------------------------------
@router.post("/inject-rules")
def inject_rules(options: InjectOptions, db: Session = Depends(get_db)):
    settings = db.query(models.Settings).first()
    
    try:
        if settings.vendor == 'mikrotik':
            connection = routeros_api.RouterOsApiPool(
                settings.mikrotik_ip, username=settings.mikrotik_user, password=settings.mikrotik_password,
                port=settings.mikrotik_port, plaintext_login=True
            )
            api = connection.get_api()
            filter_api = api.get_resource('/ip/firewall/filter')
            
            def smart_add_filter(chain, action, list_name, comment):
                existing = filter_api.get(comment=comment)
                if not existing:
                    filter_api.add(chain=chain, action=action, src_address_list=list_name, comment=comment)

            smart_add_filter("forward", "drop", "MOROSOS_FACTRED", "FactRed: Corte de Servicio a Morosos")
            smart_add_filter("forward", "drop", "SUSPENDIDOS_FACTRED", "FactRed: Suspension Administrativa")
            connection.disconnect()

        elif settings.vendor == 'fortinet':
            device = {
                'device_type': 'fortinet', 'host': settings.fortinet_ip,
                'username': settings.fortinet_user, 'password': settings.fortinet_password,
                'port': settings.fortinet_port or 22,
                'global_delay_factor': 2,
            }
            net_connect = ConnectHandler(**device)
            
            # Comentario sin espacios para que FortiOS no se queje
            commands = [
                "config firewall addrgrp",
                'edit "MOROSOS_FACTRED"',
                "set comment FactRed_Corte_Servicio", 
                "next",
                "end"
            ]
            
            # EL TRUCO MAGICO: cmd_verify=False apaga la verificación estricta
            net_connect.send_config_set(commands, cmd_verify=False)
            
            if options.mode == 'full' and options.base_lan:
                lan_cmds = [
                    "config system interface",
                    "edit port2",
                    f"set ip {options.base_lan}",
                    "set allowaccess ping https ssh",
                    "next",
                    "end"
                ]
                net_connect.send_config_set(lan_cmds, cmd_verify=False)
                
            net_connect.disconnect()

        return {"message": f"Orquestacion {settings.vendor} completada."}
        
    except Exception as e:
        print(f"DEBUG ERROR INYECCION: {str(e)}") 
        raise HTTPException(status_code=500, detail=f"Error en inyeccion: {str(e)}")