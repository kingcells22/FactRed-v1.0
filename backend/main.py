from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import clients, billing, util

app = FastAPI(title="FactRed API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clients.router)
app.include_router(billing.router)
app.include_router(util.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema FactRed"}
