from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class InvoiceBase(BaseModel):
    amount: float
    status: str = "Pending"
    issue_date: date
    due_date: date

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    client_id: int

    class Config:
        from_attributes = True 

class ClientBase(BaseModel):
    first_name: str
    last_name: str
    identity_doc: str
    address: str
    plan_type: str
    plan_amount: float
    contact_number: str
    ip_address: Optional[str] = None
    service_status: str = "Active"
    billing_day: int
    # --- CAMBIO A ID DEL SWITCH ---
    network_device_id: Optional[int] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    identity_doc: Optional[str] = None
    address: Optional[str] = None
    plan_type: Optional[str] = None
    plan_amount: Optional[float] = None
    contact_number: Optional[str] = None
    ip_address: Optional[str] = None
    service_status: Optional[str] = None
    billing_day: Optional[int] = None
    # --- CAMBIO A ID DEL SWITCH ---
    network_device_id: Optional[int] = None

class Client(ClientBase):
    id: int
    created_at: datetime
    invoices: List[Invoice] = []

    class Config:
        from_attributes = True 

class SetupCreate(BaseModel):
    vendor: str = "mikrotik" 
    mikrotik_ip: str
    mikrotik_user: str
    mikrotik_password: str
    mikrotik_port: int = 8728
    company_name: str = "Kingsystem Solutions"
    new_admin_password: str  

class SetupStatus(BaseModel):
    is_installed: bool
    company_name: str

class SwitchCreate(BaseModel):
    name: str
    ip_address: str
    username: str
    password: str
    lan_segment: Optional[str] = None
    location: Optional[str] = "Nodo Principal"

class SwitchResponse(SwitchCreate):
    id: int
    vendor: str
    status: str 

    class Config:
        from_attributes = True