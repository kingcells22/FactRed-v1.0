import os
from sqlalchemy import create_engine, text
from database import Base, engine, SQLALCHEMY_DATABASE_URL
from models import Client, Invoice
from dotenv import load_dotenv

load_dotenv()

def create_database():
    # Parse the URL to get the base connection string (without DB name)
    # This is a bit hacky but works for standard connection strings
    # Assuming format: postgresql://user:pass@host:port/dbname
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not found in .env")
        return

    # Connect to 'postgres' database to create the new database
    if "/factred" in db_url:
        root_url = db_url.replace("/factred", "/postgres")
    else:
        print("Could not deduce root URL from DATABASE_URL")
        return

    try:
        root_engine = create_engine(root_url, isolation_level="AUTOCOMMIT")
        with root_engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'factred'"))
            if not result.fetchone():
                print("Creating database 'factred'...")
                conn.execute(text("CREATE DATABASE factred"))
                print("Database created successfully.")
            else:
                print("Database 'factred' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")
        print("Please ensure your PostgreSQL server is running and credentials in .env are correct.")

def create_tables():
    print("Creating tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_database()
    create_tables()
