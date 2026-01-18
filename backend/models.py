from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    identity_doc = Column(String, unique=True, index=True) # Cedula/Pasaporte
    address = Column(String)
    plan_type = Column(String) # Could be a foreign key to a Plan table later
    plan_amount = Column(Float)
    contact_number = Column(String)
    ip_address = Column(String, nullable=True)
    service_status = Column(String, default="Active") # Active, Suspended
    billing_day = Column(Integer) # Day of month to cut
    created_at = Column(DateTime, default=datetime.utcnow)

    invoices = relationship("Invoice", back_populates="client")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    amount = Column(Float)
    status = Column(String, default="Pending") # Pending, Paid, Overdue
    issue_date = Column(Date)
    due_date = Column(Date)
    
    client = relationship("Client", back_populates="invoices")
