from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from . import get_db  # Ensure this is the correct import path
from .auth import get_current_user
from .schemas import UserActivityCreate, UserActivity, User


router = APIRouter()

@router.post("/activities/")
async def log_activity(
    activity: UserActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_activity = UserActivity(**activity.dict(), user_id=current_user.id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity
