# Reserved for future user-specific dependencies
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db


def get_user_service(
    db: Session = Depends(get_db)
):

    return db