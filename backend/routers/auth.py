from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models, database

router = APIRouter(tags=["Auth"])

# Conexion a la BD
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquema de lo que envia el Frontend
class LoginRequest(BaseModel):
    username: str
    password: str

# La ruta para iniciar sesion
@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # 1. Buscamos al usuario en la Base de Datos
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    
    # 2. Verificamos si existe y si la clave es correcta
    # (AQUI LE QUITE LA 'Ñ' A LA PALABRA CONTRASEÑA)
    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o clave incorrectos" 
        )
    
    # 3. Si todo esta bien, le damos acceso
    return {"message": "Login exitoso", "username": user.username}