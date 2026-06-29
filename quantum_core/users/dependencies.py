from fastapi import Depends, HTTPException
from quantum_core.database.session import get_db


def get_current_user():
    # placeholder for JWT auth later
    raise HTTPException(status_code=501, detail="Not implemented yet")