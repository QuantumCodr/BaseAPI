from sqlalchemy import create_engine

from quantum_core.core.config import settings

engine = create_engine(settings.DATABASE_URL)

try:
    conn = engine.connect()
    print("DB CONNECTED SUCCESSFULLY")
    conn.close()
except Exception as e:
    print("DB CONNECTION FAILED:", e)