from sqlalchemy import create_engine
from quantum_core.core.config import settings

# Database engine (core connection to Postgres)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)