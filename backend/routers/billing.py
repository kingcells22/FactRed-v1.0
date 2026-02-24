from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
import models, schemas, database
from typing import List
# --- IMPORTAMOS EL SERVICIO REAL ---
from services.mikrotik import mikrotik_service 
# -----------------------------------

router = APIRouter(
    prefix="/billing",
    tags=["billing"],
)

# Mock notification service (Este lo dejamos así por ahora)
def send_whatsapp_notification(phone: str, message: str):
    print(f"--- WHATSAPP MOCK ({phone}) ---")
    print(message)
    print("-------------------------------")
    return True

# --- LÓGICA DE CORTE REAL ---
def toggle_network_access(ip_address: str, allow_access: bool):
    """
    Llama al MikroTik para cortar (allow_access=False) 
    o reconectar (allow_access=True)
    """
    if not ip_address:
        return False
    
    # Si allow_access es False (Cortar), activar=False en el servicio (lo manda a morosos)
    # Si allow_access es True (Pagar), activar=True en el servicio (lo saca de morosos)
    success = mikrotik_service.toggle_service(ip_address, activar=allow_access)
    return success
# ----------------------------

@router.post("/process-daily")
def process_daily_billing(db: Session = Depends(database.get_db)):
    """
    Genera facturas y CORTA el servicio a los morosos.
    """
    today = date.today()
    clients = db.query(models.Client).filter(models.Client.service_status == "Active").all()
    results = []

    for client in clients:
        # 1. Generar Factura (Si es su día de corte)
        # (Lógica simplificada: Si hoy es el día, factura)
        if today.day == client.billing_day or (today.day > 28 and client.billing_day >= 28):
            # Verificar si ya tiene factura este mes para no duplicar
            current_month_invoice = db.query(models.Invoice).filter(
                models.Invoice.client_id == client.id,
                models.Invoice.issue_date >= today.replace(day=1)
            ).first()
            
            if not current_month_invoice:
                invoice = models.Invoice(
                    client_id=client.id,
                    amount=client.plan_amount,
                    issue_date=today,
                    due_date=today + timedelta(days=5), # Vence en 5 días
                    status="Pending"
                )
                db.add(invoice)
                db.commit()
                results.append(f"Factura generada para {client.first_name}")

        # 2. Verificar MOROSIDAD (El Corte)
        # Buscamos facturas pendientes QUE YA VENCIERON (fecha < hoy)
        overdue_invoices = db.query(models.Invoice).filter(
            models.Invoice.client_id == client.id,
            models.Invoice.status == "Pending",
            models.Invoice.due_date < today 
        ).all()

        if overdue_invoices:
            # ¡AQUÍ OCURRE EL CORTE REAL!
            print(f"?? Cliente {client.first_name} tiene deuda. Cortando servicio...")
            
            # 1. Cambiar estado en BD
            client.service_status = "Suspended"
            
            # 2. Mandar orden al MikroTik
            toggle_network_access(client.ip_address, allow_access=False)
            
            results.append(f"CORTADO: {client.first_name} (IP: {client.ip_address})")
            db.commit()

    return {"processed": True, "details": results}

# --- NUEVO ENDPOINT PARA PROBAR EL CORTE MANUALMENTE ---
@router.post("/manual-suspend/{client_id}")
def manual_suspend(client_id: int, db: Session = Depends(database.get_db)):
    """Fuerza el corte de un cliente inmediatamente para pruebas"""
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Cortar en BD
    client.service_status = "Suspended"
    db.commit()
    
    # Cortar en MikroTik
    success = toggle_network_access(client.ip_address, allow_access=False)
    
    if success:
        return {"message": f"Servicio cortado exitosamente a {client.ip_address}"}
    else:
        return {"message": "Error al comunicar con MikroTik, revisa la consola del backend"}

@router.post("/manual-activate/{client_id}")
def manual_activate(client_id: int, db: Session = Depends(database.get_db)):
    """Reactiva el servicio manualmente"""
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    client.service_status = "Active"
    db.commit()
    
    success = toggle_network_access(client.ip_address, allow_access=True)
    
    if success:
        return {"message": f"Servicio reactivado para {client.ip_address}"}
    else:
        return {"message": "Error al comunicar con MikroTik"}
# -------------------------------------------------------

@router.get("/invoices/{client_id}", response_model=List[schemas.Invoice])
def get_client_invoices(client_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Invoice).filter(models.Invoice.client_id == client_id).all()

@router.get("/stats")
def get_billing_stats(db: Session = Depends(database.get_db)):
    pending_invoices = db.query(models.Invoice).filter(models.Invoice.status == "Pending").all()
    total_pending = sum(inv.amount for inv in pending_invoices)
    
    today = date.today()
    overdue_count = db.query(models.Invoice).filter(
        models.Invoice.status == "Pending",
        models.Invoice.due_date < today
    ).count()

    suspended_count = db.query(models.Client).filter(models.Client.service_status == "Suspended").count()
    
    return {
        "pending_amount": total_pending,
        "overdue_invoices": overdue_count,
        "suspended_clients": suspended_count
    }