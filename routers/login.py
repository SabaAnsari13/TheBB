from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Depends, Form, HTTPException, APIRouter, Request
from .tables import User
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.declarative import declarative_base
import smtplib
import os
import random
from dotenv import load_dotenv
from . import get_db
from sqlalchemy.orm import Session
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()

# Load environment variables from .env file
load_dotenv()

# Base class for declarative models
Base = declarative_base()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer for token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory="frontend/templates")

# Pydantic model for user login
class Login(BaseModel):
    username: str
    password: str

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Login endpoint
@router.post("/login")
async def login(request: Request,username: str = Form(...),password:str = Form(...) , db: Session = Depends(get_db)):
    # Check if logging in using either email or username
    user_details = db.query(User).filter(User.username == username).first()
    if user_details:
        return templates.TemplateResponse("home.html", {"request": request})
    return templates.TemplateResponse("home.html", {"request": request})

    # Comparing the password with the hashed password