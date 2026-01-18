from sqlalchemy.orm import Session
from sqlalchemy import or_
import models, schemas

def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def get_client_by_identity(db: Session, identity_doc: str):
    return db.query(models.Client).filter(models.Client.identity_doc == identity_doc).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Client)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                models.Client.first_name.ilike(search_filter),
                models.Client.last_name.ilike(search_filter),
                models.Client.identity_doc.ilike(search_filter),
                models.Client.ip_address.ilike(search_filter)
            )
        )
    return query.offset(skip).limit(limit).all()

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, client: schemas.ClientUpdate):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client:
        update_data = client.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_client, key, value)
        db.commit()
        db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client:
        db.delete(db_client)
        db.commit()
    return db_client
