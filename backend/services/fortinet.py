from netmiko import ConnectHandler
import re
from database import SessionLocal
import models

class FortinetService:
    def _get_config(self):
        db = SessionLocal()
        settings = db.query(models.Settings).first()
        db.close()
        return settings

    def _get_connection(self):
        s = self._get_config()
        if not s or not s.fortinet_enabled or not s.fortinet_ip:
            return None
        
        device = {
            'device_type': 'fortinet',
            'host': s.fortinet_ip,
            'username': s.fortinet_user,
            'password': s.fortinet_password,
            'port': s.fortinet_port or 22,
            'global_delay_factor': 2
        }
        return ConnectHandler(**device)

    def get_system_status(self):
        try:
            s = self._get_config()
            net_connect = self._get_connection()
            if not net_connect:
                return {"identity": "Deshabilitado", "wan_ip": "---", "uptime": "---", "status": "Offline"}
            
            # 1. Obtener el Hostname
            sys_output = net_connect.send_command("get system status")
            host_match = re.search(r"Hostname:\s*(.*)", sys_output, re.IGNORECASE)
            hostname = host_match.group(1).strip() if host_match else "FortiGate"
            
            # 2. Obtener el Uptime
            perf_output = net_connect.send_command("get system performance status")
            up_match = re.search(r"Uptime:\s*(.*)", perf_output, re.IGNORECASE)
            uptime_raw = up_match.group(1).strip() if up_match else "Activo"
            
            # 3. Obtener WAN IP - PLAN INFALIBLE
            wan_ip = s.fortinet_ip # Si falla la lectura, usamos la IP de conexión
            try:
                # Este comando lista las IPs activas a bajo nivel
                wan_output = net_connect.send_command("diagnose ip address list")
                # Buscamos la IP asignada al port1
                wan_ip_match = re.search(r"IP=([\d\.]+).*devname=port1", wan_output, re.IGNORECASE)
                if wan_ip_match:
                    wan_ip = wan_ip_match.group(1)
            except Exception:
                pass # Ignoramos el error silenciosamente y dejamos el plan B
            
            net_connect.disconnect()
            
            return {
                "identity": hostname,
                "uptime": uptime_raw,
                "wan_ip": wan_ip,
                "status": "Online"
            }
        except Exception as e:
            print(f"DEBUG Fortinet Status: {e}")
            return {"identity": "Error", "wan_ip": "Error", "uptime": "---", "status": "Offline"}

fortinet_service = FortinetService()