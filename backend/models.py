from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    identity_doc = Column(String, unique=True, index=True) 
    address = Column(String)
    plan_type = Column(String) 
    plan_amount = Column(Float)
    contact_number = Column(String)
    ip_address = Column(String, nullable=True)
    service_status = Column(String, default="Active") 
    billing_day = Column(Integer) 
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # --- NUEVA RELACIÓN DE ENRUTADOR/SWITCH ---
    network_device_id = Column(Integer, ForeignKey("network_devices.id"), nullable=True)

    invoices = relationship("Invoice", back_populates="client")
    network_device = relationship("NetworkDevice", back_populates="clients")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    amount = Column(Float)
    status = Column(String, default="Pending") 
    issue_date = Column(Date)
    due_date = Column(Date)
    
    client = relationship("Client", back_populates="invoices")

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    is_installed = Column(Boolean, default=False)
    vendor = Column(String, default="mikrotik") 
    mikrotik_ip = Column(String, default="")
    mikrotik_user = Column(String, default="")
    mikrotik_password = Column(String, default="") 
    mikrotik_port = Column(Integer, default=8728)  
    fortinet_ip = Column(String, default="")
    fortinet_user = Column(String, default="")
    fortinet_password = Column(String, default="")
    fortinet_port = Column(Integer, default=22) 
    fortinet_enabled = Column(Boolean, default=False) 
    company_name = Column(String, default="Kingsystem Solutions")
    admin_password_changed = Column(Boolean, default=False) 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) 
    is_active = Column(Boolean, default=True)

class NetworkDevice(Base):
    __tablename__ = "network_devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String, default="Nodo Principal")
    ip_address = Column(String)
    username = Column(String)
    password = Column(String)
    vendor = Column(String, default="Detectando...") 
    lan_segment = Column(String, nullable=True)
    
    clients = relationship("Client", back_populates="network_device")