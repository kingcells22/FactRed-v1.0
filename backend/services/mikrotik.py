import routeros_api
import os
from dotenv import load_dotenv
from netmiko import ConnectHandler 
from sqlalchemy.orm import Session
from database import SessionLocal
import models

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"))

class MikrotikService:
    def __init__(self):
        self.default_host = os.getenv("MIKROTIK_HOST")
        self.default_user = os.getenv("MIKROTIK_USER")
        self.default_pass = os.getenv("MIKROTIK_PASSWORD")
        self.default_port = int(os.getenv("MIKROTIK_PORT", 8728))

    def _get_active_config(self):
        try:
            db = SessionLocal()
            settings = db.query(models.Settings).first()
            db.close()
            if settings and settings.is_installed:
                return {
                    "vendor": settings.vendor,
                    "host": settings.mikrotik_ip,
                    "user": settings.mikrotik_user,
                    "password": settings.mikrotik_password,
                    "port": settings.mikrotik_port
                }
        except: pass
        return { "vendor": "mikrotik", "host": self.default_host, "user": self.default_user, "password": self.default_pass, "port": self.default_port }

    def _get_connection(self, config):
        try:
            return routeros_api.RouterOsApiPool(
                config['host'], username=config['user'], password=config['password'], 
                port=config['port'], plaintext_login=True
            )
        except Exception as e:
            print(f"Error MikroTik: {e}")
            return None

    def toggle_service(self, ip_cliente, activar=True):
        config = self._get_active_config()
        
        # LOGICA MIKROTIK (TUYA ORIGINAL)
        if config['vendor'] == 'mikrotik':
            connection = self._get_connection(config)
            if not connection: return False
            try:
                api = connection.get_api()
                list_morosos = api.get_resource('/ip/firewall/address-list')
                cliente_en_lista = list_morosos.get(address=ip_cliente, list='morosos')
                if activar:
                    for item in cliente_en_lista: list_morosos.remove(id=item['id'])
                else:
                    if not cliente_en_lista: list_morosos.add(list='morosos', address=ip_cliente, comment='Corte_FactRed')
                return True
            except: return False
            finally: connection.disconnect()

        # LOGICA CISCO (NUEVA)
        elif config['vendor'] == 'cisco_ios':
            try:
                device = {
                    'device_type': 'cisco_ios', 'host': config['host'],
                    'username': config['user'], 'password': config['password'],
                    'port': config['port'] or 22
                }
                net_connect = ConnectHandler(**device)
                net_connect.enable()
                cmd = f"no access-list 101 deny ip host {ip_cliente} any" if activar else f"access-list 101 deny ip host {ip_cliente} any"
                net_connect.send_config_set([cmd])
                net_connect.disconnect()
                return True
            except: return False
        return False

    def sync_queue(self, nombre_cliente, ip_cliente, plan_velocidad):
        config = self._get_active_config()
        
        # LOGICA MIKROTIK (TUYA ORIGINAL)
        if config['vendor'] == 'mikrotik':
            connection = self._get_connection(config)
            if not connection: return False
            try:
                api = connection.get_api()
                queues = api.get_resource('/queue/simple')
                safe_name = f"{nombre_cliente}_{ip_cliente.split('.')[-1]}"
                existing = queues.get(target=f"{ip_cliente}/32")
                if existing:
                    queues.set(id=existing[0]['id'], max_limit=plan_velocidad, name=safe_name)
                else:
                    queues.add(name=safe_name, target=ip_cliente, max_limit=plan_velocidad)
                return True
            except: return False
            finally: connection.disconnect()
            
        elif config['vendor'] == 'cisco_ios':
            # Cisco usa Policy Maps
            return True
        return False

    def remove_queue(self, ip_cliente):
        config = self._get_active_config()
        if config['vendor'] == 'mikrotik':
            connection = self._get_connection(config)
            if not connection: return False
            try:
                api = connection.get_api()
                queues = api.get_resource('/queue/simple')
                existing = queues.get(target=f"{ip_cliente}/32")
                for item in existing: queues.remove(id=item['id'])
                return True
            except: return False
            finally: connection.disconnect()
        return True

    def get_system_status(self):
        config = self._get_active_config()
        if config['vendor'] == 'mikrotik':
            connection = self._get_connection(config)
            if not connection: return {"identity": "Offline", "wan_ip": "---"}
            try:
                api = connection.get_api()
                res = api.get_resource('/system/resource').get()[0]
                ips = api.get_resource('/ip/address').get(interface='ether1')
                wan_ip = ips[0].get('address') if ips else "Sin IP"
                return {"identity": api.get_resource('/system/identity').get()[0].get('name'), "cpu_load": int(res.get('cpu-load', 0)), "uptime": res.get('uptime', '0'), "wan_ip": wan_ip}
            except: return {"identity": "Error", "wan_ip": "Error"}
            finally: connection.disconnect()
        return {}

    def get_interface_stats(self):
        return []

mikrotik_service = MikrotikService()