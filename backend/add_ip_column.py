from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def add_column():
    with engine.connect() as conn:
        try:
            # Postgres specific syntax
            print("Attempting to add ip_address column...")
            conn.execute(text("ALTER TABLE clients ADD COLUMN IF NOT EXISTS ip_address VARCHAR"))
            conn.commit()
            print("Column 'ip_address' added successfully (or already existed).")
        except Exception as e:
            print(f"Error adding column: {e}")

if __name__ == "__main__":
    add_column()
