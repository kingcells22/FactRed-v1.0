from fastapi.responses import HTMLResponse
import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import clients, billing, util, setup, auth
import models  
from database import engine  
from fastapi.staticfiles import StaticFiles

# --- CREACIÓN DE TABLAS ---
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FactRed API", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers de gestión (Aquí es donde vive el login y los clientes)
app.include_router(clients.router)
app.include_router(billing.router)
app.include_router(util.router)
app.include_router(setup.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"status": "FactRed API is running smoothly"}

# HEMOS ELIMINADO LA MALLA TEMPORALMENTE PARA RECUPERAR EL ACCESO