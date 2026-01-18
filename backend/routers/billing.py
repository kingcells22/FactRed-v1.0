from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
import models, schemas, database, crud
from typing import List

router = APIRouter(
    prefix="/billing",
    tags=["billing"],
)

# Mock notification service
def send_whatsapp_notification(phone: str, message: str):
    print(f"--- WHATSAPP MOCK ({phone}) ---")
    print(message)
    print("-------------------------------")
    return True

# Mock network service
def suspend_service(ip_address: str):
    if not ip_address:
        return
    print(f"--- NETWORK SUSPEND ({ip_address}) ---")
    print(f"Service suspended for IP {ip_address}")
    return True

@router.post("/process-daily")
def process_daily_billing(db: Session = Depends(database.get_db)):
    """
    Checks all clients for billing dates and performs actions:
    1. Generate invoice if billing date is newly reached.
    2. Send reminder if close to due date.
    3. Suspend if overdue.
    """
    today = date.today()
    clients = db.query(models.Client).filter(models.Client.service_status == "Active").all()
    results = []

    for client in clients:
        # Simple Logic: Billing day is the day of month client must pay
        # E.g., if billing_day is 5.
        
        # 1. Check if we need to generate an invoice for this month
        # Logic: If today is billing_day, generate invoice (due in 5 days?)
        # For simplicity, let's assume cutting date = billing_day
        
        # This is a rigorous implementation of "Corte" vs "Vencimiento"
        # Let's say: Create Invoice 5 days BEFORE Cutting Date
        # Due Date = Cutting Date
        
        # ... Implementation simplified for the MVP:
        # If today == billing_day: Generate Invoice due in 5 days.
        
        if today.day == client.billing_day:
            # Check if invoice already exists for this month/year
            # (Skipping check for simplicity in this MVP step, assume single run)
            
            invoice = models.Invoice(
                client_id=client.id,
                amount=client.plan_amount,
                issue_date=today,
                due_date=today + timedelta(days=5),
                status="Pending"
            )
            db.add(invoice)
            db.commit()
            
            msg = f"Hola {client.first_name}, tu factura #{invoice.id} de {client.plan_amount} ya fue generada. Vence el {invoice.due_date}."
            send_whatsapp_notification(client.contact_number, msg)
            results.append(f"Generated invoice for {client.first_name}")

        # 2. Check Overdue
        # Find pending invoices that are past due date
        overdue_invoices = db.query(models.Invoice).filter(
            models.Invoice.client_id == client.id,
            models.Invoice.status == "Pending",
            models.Invoice.due_date < today
        ).all()

        if overdue_invoices:
            # Suspend Service!
            client.service_status = "Suspended"
            suspend_service(client.ip_address)
            
            msg = f"AVISO DE CORTE: {client.first_name}, servicio suspendido por facturas vencidas. Total deuda: {sum(i.amount for i in overdue_invoices)}"
            send_whatsapp_notification(client.contact_number, msg)
            results.append(f"Suspended {client.first_name}")
            db.commit()

    return {"processed": True, "details": results}

@router.get("/invoices/{client_id}", response_model=List[schemas.Invoice])
def get_client_invoices(client_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Invoice).filter(models.Invoice.client_id == client_id).all()

@router.get("/stats")
def get_billing_stats(db: Session = Depends(database.get_db)):
    # Total Pending Amount
    pending_invoices = db.query(models.Invoice).filter(models.Invoice.status == "Pending").all()
    total_pending = sum(inv.amount for inv in pending_invoices)
    
    # Count overdue (assuming today is checking date)
    today = date.today()
    overdue_count = db.query(models.Invoice).filter(
        models.Invoice.status == "Pending",
        models.Invoice.due_date < today
    ).count()

    # Network Status (Mock based on suspended clients)
    suspended_count = db.query(models.Client).filter(models.Client.service_status == "Suspended").count()
    
    return {
        "pending_amount": total_pending,
        "overdue_invoices": overdue_count,
        "suspended_clients": suspended_count
    }
