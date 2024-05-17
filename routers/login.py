from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from . import auth
from . import get_db
from .schemas import Token, UserActivityCreate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .activity import log_activity


router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    await log_activity(UserActivityCreate(activity_type="login"), db, user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/home")
async def read_home(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth.get_current_user(token, db)
    return templates.TemplateResponse("home.html", {"request": request, "username": user.username})
