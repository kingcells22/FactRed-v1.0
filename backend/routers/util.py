from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pyDolarVenezuela.pages import BCV
from pyDolarVenezuela import Monitor
from pydantic import BaseModel
from datetime import datetime
import routeros_api
import models, database, schemas 
import re 
from services.fortinet import fortinet_service 
import socket 
from netmiko import ConnectHandler 

router = APIRouter(
    prefix="/util",
    tags=["utility"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# 1. ESTADO DE RED (DASHBOARD) - DINÁMICO MULTIMARCA
# ---------------------------------------------------------
@router.get("/network/status")
def get_network_status(db: Session = Depends(get_db)):
    devices = db.query(models.NetworkDevice).all()
    active_cores = []
    
    if not devices:
        return {"cores": []}

    for dev in devices:
        core_data = {
            "name": dev.name,
            "vendor": dev.vendor,
            "wan_ip": dev.ip_address,
            "status": "Offline",
            "uptime": "---",
            "cpu_load": "0%",
            "interfaces": [] 
        }
        
        if dev.vendor == "MikroTik":
            try:
                connection = routeros_api.RouterOsApiPool(
                    dev.ip_address, username=dev.username, password=dev.password, 
                    port=8728, plaintext_login=True
                )
                api = connection.get_api()
                resources = api.get_resource('/system/resource').get()
                addresses = api.get_resource('/ip/address').get() 
                
                core_data["status"] = "Online"
                core_data["uptime"] = resources[0].get('uptime', '0s')
                core_data["cpu_load"] = f"{resources[0].get('cpu-load', 0)}%"
                
                for addr in addresses:
                    core_data["interfaces"].append({
                        "name": addr.get('interface', 'Unknown'),
                        "ip": addr.get('address', '0.0.0.0')
                    })
                connection.disconnect()
            except Exception as e: 
                print(f"Error MikroTik: {e}")
            
        elif dev.vendor == "Fortinet":
            try:
                net_connect = ConnectHandler(
                    device_type='fortinet', host=dev.ip_address, 
                    username=dev.username, password=dev.password, 
                    timeout=4, global_delay_factor=2
                )
                perf_output = net_connect.send_command("get system performance status")
                up_match = re.search(r"Uptime:\s*(.*)", perf_output, re.IGNORECASE)
                
                core_data["status"] = "Online"
                core_data["uptime"] = up_match.group(1).strip() if up_match else "Activo"
                core_data["cpu_load"] = "N/A" 
                
                iface_output = net_connect.send_command("diagnose ip address list")
                for line in iface_output.splitlines():
                    match = re.search(r"IP=([\d\.]+).*devname=([a-zA-Z0-9_\-]+)", line, re.IGNORECASE)
                    if match:
                        ip_val, iface_name = match.groups()
                        if ip_val != "127.0.0.1": 
                            core_data["interfaces"].append({
                                "name": iface_name,
                                "ip": ip_val
                            })
                net_connect.disconnect()
            except Exception as e: 
                print(f"Error Fortinet: {e}")
            
        elif dev.vendor == "Cisco":
            core_data["status"] = is_online(dev.ip_address)
            
        active_cores.append(core_data)

    return {"cores": active_cores}

# ---------------------------------------------------------
# 2. TASA BCV - INTACTO
# ---------------------------------------------------------
@router.get("/exchange-rate")
def get_exchange_rate():
    try:
        import requests 
        resp = requests.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=5)
        data = resp.json()
        rate = float(data.get("promedio", 344.87))
        return {"rate": rate, "source": "DolarAPI (Oficial BCV)", "last_updated": datetime.now().isoformat()}
    except:
        return {"rate": 344.87, "source": "Fallback", "last_updated": datetime.now().isoformat()}


# =========================================================
# 3. GESTIÓN DE SWITCHES E ISPS 
# =========================================================

# --- FUNCION PARA DETECTAR MARCA AL GUARDAR ---
def detect_vendor(ip, user, pwd):
    try:
        socket.create_connection((ip, 8728), timeout=1.5) 
        conn = routeros_api.RouterOsApiPool(ip, username=user, password=pwd, plaintext_login=True)
        api = conn.get_api()
        conn.disconnect()
        return "MikroTik"
    except: 
        pass 

    try:
        socket.create_connection((ip, 22), timeout=1.5)
        
        try:
            net_connect = ConnectHandler(device_type='fortinet', host=ip, username=user, password=pwd, timeout=4, global_delay_factor=2)
            net_connect.disconnect()
            return "Fortinet"
        except: pass

        try:
            net_connect = ConnectHandler(device_type='cisco_ios', host=ip, username=user, password=pwd, timeout=4)
            net_connect.disconnect()
            return "Cisco"
        except: pass
    except:
        pass

    return "Desconocido"

# --- FUNCION PARA PING RAPIDO ---
def is_online(ip):
    try:
        socket.create_connection((ip, 22), timeout=1)
        return "Online"
    except:
        try:
            socket.create_connection((ip, 8728), timeout=1)
            return "Online"
        except:
            return "Offline"

# --- RUTAS DE LA TABLA ---

@router.post("/switches", response_model=schemas.SwitchResponse)
def create_switch(device: schemas.SwitchCreate, db: Session = Depends(get_db)):
    detected_vendor = detect_vendor(device.ip_address, device.username, device.password)
    
    new_device = models.NetworkDevice(
        name=device.name,
        location=device.location,
        ip_address=device.ip_address,
        username=device.username,
        password=device.password,
        lan_segment=device.lan_segment,
        vendor=detected_vendor
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    
    return {**new_device.__dict__, "status": is_online(new_device.ip_address)}

@router.get("/switches", response_model=list[schemas.SwitchResponse])
def get_switches(db: Session = Depends(get_db)):
    devices = db.query(models.NetworkDevice).all()
    result = []
    for d in devices:
        current_status = is_online(d.ip_address)
        result.append({**d.__dict__, "status": current_status})
    return result

@router.delete("/switches/{device_id}")
def delete_switch(device_id: int, db: Session = Depends(get_db)):
    device = db.query(models.NetworkDevice).filter(models.NetworkDevice.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    db.delete(device)
    db.commit()
    return {"message": "Equipo eliminado correctamente"}

# ---------------------------------------------------------
# 4. VARITA MAGICA (PARTE 1) - ESCANEO PRE-VUELO
# ---------------------------------------------------------
@router.get("/switches/{device_id}/check-init")
def check_device_initialization(device_id: int, db: Session = Depends(get_db)):
    device = db.query(models.NetworkDevice).filter(models.NetworkDevice.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    report = {
        "status": "clean", 
        "vendor": device.vendor,
        "details": [],
        "message": "El equipo esta limpio. Se inyectaran los grupos de cortes y redireccion de pagos."
    }

    if device.vendor == "MikroTik":
        try:
            conn = routeros_api.RouterOsApiPool(
                device.ip_address, username=device.username, password=device.password,
                port=8728, plaintext_login=True
            )
            api = conn.get_api()

            # 1. Buscamos si existe el grupo de morosos
            address_lists = api.get_resource('/ip/firewall/address-list').get()
            has_morosos = any(item.get('list') == 'MOROSOS_FACTRED' for item in address_lists)

            # 2. Buscamos si existe regla de redireccion al puerto 8000
            nat_rules = api.get_resource('/ip/firewall/nat').get()
            has_nat = any('8000' in item.get('dst-port', '') for item in nat_rules)

            if has_morosos or has_nat:
                report["status"] = "partial"
                report["message"] = "Atencion: Se detectaron reglas de FactRed previas en este equipo."
                if has_morosos:
                    report["details"].append("El grupo MOROSOS_FACTRED ya existe (Se omitira).")
                if has_nat:
                    report["details"].append("La regla NAT de redireccion ya existe (Se omitira).")
            else:
                report["details"].append("No se detectaron Address Lists de FactRed.")
                report["details"].append("No se detectaron redirecciones NAT al portal.")

            conn.disconnect()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error leyendo MikroTik: {str(e)}")

    elif device.vendor == "Fortinet":
        try:
            net_connect = ConnectHandler(
                device_type='fortinet', host=device.ip_address,
                username=device.username, password=device.password,
                timeout=4, global_delay_factor=2
            )
            
            # Buscamos si existe el grupo de morosos en el firewall
            output = net_connect.send_command("show firewall addrgrp MOROSOS_FACTRED")
            
            if "edit \"MOROSOS_FACTRED\"" in output or ("MOROSOS_FACTRED" in output and "command parse error" not in output.lower()):
                report["status"] = "partial"
                report["message"] = "Atencion: Se detectaron reglas de FactRed previas en este equipo."
                report["details"].append("El grupo MOROSOS_FACTRED ya existe en el firewall (Se omitira).")
            else:
                report["details"].append("El equipo esta libre de grupos de corte.")
                report["details"].append("Listo para inyectar la politica maestra de bloqueo.")

            net_connect.disconnect()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error leyendo Fortinet: {str(e)}")
            
    else:
        raise HTTPException(status_code=400, detail="Operacion no soportada para este fabricante.")

    return report


# ---------------------------------------------------------
# 5. VARITA MAGICA (PARTE 2) - INYECCION SEGURA
# ---------------------------------------------------------
@router.post("/switches/{device_id}/init")
def initialize_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(models.NetworkDevice).filter(models.NetworkDevice.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    log = []

    if device.vendor == "MikroTik":
        try:
            conn = routeros_api.RouterOsApiPool(
                device.ip_address, username=device.username, password=device.password,
                port=8728, plaintext_login=True
            )
            api = conn.get_api()

            # 1. Address Lists
            address_lists = api.get_resource('/ip/firewall/address-list').get()
            if not any(item.get('list') == 'MOROSOS_FACTRED' for item in address_lists):
                api.get_resource('/ip/firewall/address-list').add(list="MOROSOS_FACTRED", address="127.0.0.2", comment="FactRed: Grupo Base Morosos")
                log.append("Creada lista MOROSOS_FACTRED.")
            
            if not any(item.get('list') == 'SUSPENDIDOS_FACTRED' for item in address_lists):
                api.get_resource('/ip/firewall/address-list').add(list="SUSPENDIDOS_FACTRED", address="127.0.0.3", comment="FactRed: Grupo Base Suspendidos")
                log.append("Creada lista SUSPENDIDOS_FACTRED.")

            # 2. Redireccion NAT (Portal de Pago)
            nat_rules = api.get_resource('/ip/firewall/nat').get()
            if not any('8000' in item.get('dst-port', '') for item in nat_rules):
                api.get_resource('/ip/firewall/nat').add(
                    chain="dstnat", action="dst-nat", to_addresses="172.31.45.56", to_ports="8000",
                    protocol="tcp", src_address_list="MOROSOS_FACTRED", dst_port="80",
                    comment="FactRed: Redireccion Portal", place_before="0"
                )
                log.append("Regla NAT de redireccion insertada en el tope.")

            # 3. Reglas Filter de Drop
            filter_rules = api.get_resource('/ip/firewall/filter').get()
            if not any(item.get('src-address-list') == 'MOROSOS_FACTRED' and item.get('action') == 'drop' for item in filter_rules):
                api.get_resource('/ip/firewall/filter').add(
                    chain="forward", action="drop", src_address_list="MOROSOS_FACTRED",
                    comment="FactRed: Corte a Morosos", place_before="0"
                )
                log.append("Regla Filter Drop (Morosos) insertada en el tope.")

            if not any(item.get('src-address-list') == 'SUSPENDIDOS_FACTRED' and item.get('action') == 'drop' for item in filter_rules):
                api.get_resource('/ip/firewall/filter').add(
                    chain="forward", action="drop", src_address_list="SUSPENDIDOS_FACTRED",
                    comment="FactRed: Suspension Administrativa", place_before="0"
                )
                log.append("Regla Filter Drop (Suspendidos) insertada en el tope.")

            conn.disconnect()
            
            if not log:
                log.append("El equipo ya estaba 100% configurado. No se modificaron reglas para evitar conflictos.")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error configurando MikroTik: {str(e)}")

    elif device.vendor == "Fortinet":
        try:
            net_connect = ConnectHandler(
                device_type='fortinet', host=device.ip_address,
                username=device.username, password=device.password,
                timeout=4, global_delay_factor=2
            )
            
            # 1. Revisar y crear Grupo MOROSOS_FACTRED
            output = net_connect.send_command("show firewall addrgrp MOROSOS_FACTRED")
            if "edit \"MOROSOS_FACTRED\"" not in output:
                config_commands = [
                    "config firewall address",
                    "edit \"DUMMY_FACTRED\"",
                    "set type ipmask",
                    "set subnet 127.0.0.9 255.255.255.255",
                    "next",
                    "end",
                    "config firewall addrgrp",
                    "edit \"MOROSOS_FACTRED\"",
                    "set member \"DUMMY_FACTRED\"",
                    "next",
                    "end"
                ]
                net_connect.send_config_set(config_commands)
                log.append("Grupo MOROSOS_FACTRED creado.")
            
            # 2. Revisar y crear Virtual IP (VIP) para redireccion al portal
            vip_check = net_connect.send_command("show firewall vip | grep PORTAL_FACTRED")
            if "PORTAL_FACTRED" not in vip_check:
                vip_commands = [
                    "config firewall vip",
                    "edit \"PORTAL_FACTRED\"",
                    "set extip 0.0.0.0-255.255.255.255",
                    "set extintf \"any\"",
                    "set portforward enable",
                    "set mappedip \"172.31.45.56\"",
                    "set extport 80",
                    "set mappedport 8000",
                    "next",
                    "end"
                ]
                net_connect.send_config_set(vip_commands)
                log.append("Virtual IP (VIP) de redireccion creado.")

            # 3. Revisar y crear Política Maestra de Bloqueo
            policy_block_check = net_connect.send_command("show firewall policy | grep FACTRED_CORTE_MOROSOS")
            if "FACTRED_CORTE_MOROSOS" not in policy_block_check:
                policy_block_cmds = [
                    "config firewall policy",
                    "edit 0",
                    "set name \"FACTRED_CORTE_MOROSOS\"",
                    "set srcintf \"any\"",
                    "set dstintf \"any\"",
                    "set srcaddr \"MOROSOS_FACTRED\"",
                    "set dstaddr \"all\"",
                    "set action deny",
                    "set schedule \"always\"",
                    "set service \"ALL\"",
                    "set logtraffic all",
                    "next",
                    "end",
                    "config firewall policy",
                    "move FACTRED_CORTE_MOROSOS before 1", 
                    "end"
                ]
                net_connect.send_config_set(policy_block_cmds)
                log.append("Politica de bloqueo (DENY) insertada.")

            # 4. Revisar y crear Política de Redireccion (Debe ir antes que el bloqueo)
            policy_redir_check = net_connect.send_command("show firewall policy | grep FACTRED_REDIRECCION")
            if "FACTRED_REDIRECCION" not in policy_redir_check:
                policy_redir_cmds = [
                    "config firewall policy",
                    "edit 0",
                    "set name \"FACTRED_REDIRECCION\"",
                    "set srcintf \"any\"",
                    "set dstintf \"any\"",
                    "set srcaddr \"MOROSOS_FACTRED\"",
                    "set dstaddr \"PORTAL_FACTRED\"",
                    "set action accept",
                    "set schedule \"always\"",
                    "set service \"ALL\"",
                    "set nat enable",
                    "next",
                    "end",
                    "config firewall policy",
                    "move FACTRED_REDIRECCION before 1", # La subimos por encima del DENY
                    "end"
                ]
                net_connect.send_config_set(policy_redir_cmds)
                log.append("Politica de redireccion (VIP) insertada en el tope.")

            net_connect.disconnect()
            
            if not log:
                log.append("El FortiGate ya tiene los grupos y politicas de FactRed.")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error configurando Fortinet: {str(e)}")
            
    else:
        raise HTTPException(status_code=400, detail="Operacion no soportada.")

    return {"message": "Inicializacion completada", "log": log}