from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas, database

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(database.get_db)):
    db_client = crud.get_client_by_identity(db, identity_doc=client.identity_doc)
    if db_client:
        raise HTTPException(status_code=400, detail="Client with this ID document already exists")
    return crud.create_client(db=db, client=client)

@router.get("/", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, search: Optional[str] = None, db: Session = Depends(database.get_db)):
    clients = crud.get_clients(db, skip=skip, limit=limit, search=search)
    return clients

@router.get("/{client_id}", response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(database.get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.put("/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, client: schemas.ClientUpdate, db: Session = Depends(database.get_db)):
    db_client = crud.update_client(db, client_id=client_id, client=client)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(database.get_db)):
    crud.delete_client(db, client_id=client_id)
    return {"ok": True}
