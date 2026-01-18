from fastapi import APIRouter, HTTPException
from pyDolarVenezuela.pages import BCV
from pyDolarVenezuela import Monitor
from pydantic import BaseModel
from datetime import datetime
from services.mikrotik import mikrotik_service

router = APIRouter(
    prefix="/util",
    tags=["utility"]
)

@router.get("/network/status")
def get_network_status():
    return {
        "system": mikrotik_service.get_system_status(),
        "interfaces": mikrotik_service.get_interface_stats()
    }

class ExchangeRateResponse(BaseModel):
    rate: float
    source: str
    last_updated: str

@router.get("/exchange-rate", response_model=ExchangeRateResponse)
def get_exchange_rate():
    try:
        # Use dolarapi.com as requested
        import requests
        resp = requests.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        
        rate = float(data.get("promedio", 0))
        
        if rate == 0:
            rate = 344.87 # Fallback
            
        return {
            "rate": rate,
            "source": "DolarAPI (Oficial BCV)",
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error fetching rate from API: {e}")
        return {
            "rate": 344.87, # Fallback
            "source": "Fallback (Error)",
            "last_updated": datetime.now().isoformat()
        }
