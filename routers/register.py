from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Depends, Form, HTTPException, APIRouter
from requests import request
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
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routers import register
from routers import login
from routers import search

app=FastAPI()

templates = Jinja2Templates(directory="frontend/templates")

router = APIRouter()

# Load environment variables from .env file
load_dotenv()

# Base class for declarative models
Base = declarative_base()

# Password hashing context

# OAuth2 password bearer for token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic model for registering a new user
class RegisterUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    name: str


class DeleteAccount(BaseModel):
    username: str = None
    email: EmailStr = None

# Function to send OTP to email
@router.post("/verifyemail")
async def email_verification(email: EmailStr):
    otp = str(random.random() * 1000000).replace('.', '')[:6]
    
    message = f"{otp} is your otp valid for 5 minutes."
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    # Login using environment variables for email and password
    s.login(os.getenv('EMAIL'), os.getenv('EMAIL_PASSWORD'))
    s.sendmail('&&&&&&', email, message)

    s.quit()

    return {'email': email, 'otp': otp}

# Function to check if the account exists using either email or username
def account_exists(db: Session, email=None, username=None):
    if username:
        user = db.query(User).filter(User.username == username).first()
    elif email:
        user = db.query(User).filter(User.email == email).first()
    return user is not None

# Function to create the hashed password

# Function to send an email with the user's login details
def send_password_email(email, password, username, name):
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "TheBookwormBurrow Login Details"

    body = f"Hi {name},\nPlease use these details to login to your account.\nUsername: {username}\nEmail: {email}\nPassword: {password}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Use your SMTP server details
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, email, msg.as_string())
    server.quit()

# Signup endpoint
@router.post("/register")
async def create_account(username: str = Form(...),password:str = Form(...) ,db: Session = Depends(get_db)):
    # Checking if username or email already exists in the database
    if account_exists(username=username, db=db):
        return {"message": "Username already exists."}

    # Adding user to database
    db_user = User(email=username, password=password, username=username)
    db.add(db_user)
    db.commit()

    # Sending email about the details
    #send_password_email(user.email, user.password, user.username, user.name)

    return templates.TemplateResponse("home.html", {"request": request})
