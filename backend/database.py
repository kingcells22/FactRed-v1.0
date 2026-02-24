from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# --- CAMBIO IMPORTANTE AQUÍ ---
# Obtenemos la ruta de la carpeta donde está este archivo database.py
base_dir = os.path.dirname(os.path.abspath(__file__))
# Unimos esa ruta con el nombre del archivo .env
env_path = os.path.join(base_dir, ".env")
# Cargamos esa ruta específica
load_dotenv(env_path)
# ------------------------------

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# --- DEBUG (Para que veas en la consola si lo leyó) ---
if SQLALCHEMY_DATABASE_URL is None:
    print("❌ ERROR: No se encontró la variable DATABASE_URL. Revisa el archivo .env")
else:
    print(f"✅ ÉXITO: Conectando a la base de datos...")
# -----------------------------------------------------

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
