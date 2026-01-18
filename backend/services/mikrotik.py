import random
from datetime import datetime, timedelta

class MikrotikMock:
    def __init__(self):
        self._start_time = datetime.now() - timedelta(days=12)

    def get_system_status(self):
        # Simulate data from a CHR
        return {
            "identity": "Mikrotik-CHR-Core",
            "cpu_load": random.randint(5, 25),
            "memory_usage": random.randint(15, 40),
            "uptime": str(datetime.now() - self._start_time).split('.')[0],
            "board_name": "CHR",
            "version": "7.12 (stable)",
            "wan_status": "Connected (Starlink)",
            "wan_ip": f"100.64.{random.randint(10,99)}.{random.randint(2,250)}"  # CGNAT typical for Starlink
        }
    
    def get_interface_stats(self):
        return [
            {"name": "ether1-wan", "tx": f"{random.randint(10,50)} Mbps", "rx": f"{random.randint(50, 300)} Mbps"},
            {"name": "bridge-local", "tx": f"{random.randint(50,300)} Mbps", "rx": f"{random.randint(10, 50)} Mbps"}
        ]

mikrotik_service = MikrotikMock()
