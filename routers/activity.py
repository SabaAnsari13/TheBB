from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from . import get_db  # Ensure this is the correct import path
from .tables import UserActivity

def log_activity(
    user_id: int,
    activity_type: str,
    db: Session = Depends(get_db)
):
    db_activity = UserActivity(user_id=user_id, activity_type=activity_type)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

