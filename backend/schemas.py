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
        orm_mode = True

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

class Client(ClientBase):
    id: int
    created_at: datetime
    invoices: List[Invoice] = []

    class Config:
        orm_mode = True
