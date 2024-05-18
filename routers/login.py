from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from . import get_db
from .schemas import UserActivityBase
from .tables import User
from .activity import log_activity

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

from fastapi.responses import JSONResponse, RedirectResponse

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )
    
    if user.hashed_password != password:
        raise HTTPException(
            status_code=401,
            detail="Wrong password",
        )

    response = JSONResponse(content={"detail": "Login successful"})
    response.set_cookie(key="username", value=user.username)
    log_activity(activity_type="login", user_id=user.user_id, db=db)
    return response
