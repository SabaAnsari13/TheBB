from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import sys
sys.path.append("..")  # Add the parent directory to the Python path
import routers.auth as auth
from routers.auth import get_password_hash
from routers import get_db
from .tables import User

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.post("/register")
async def create_account(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = auth.get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()

    return templates.TemplateResponse("login.html", {"request": request})

