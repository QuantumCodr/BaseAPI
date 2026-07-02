from sqlalchemy.orm import declarative_base

Base = declarative_base()

# IMPORTANT: force model registration
from app.modules.users import models