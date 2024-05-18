from dotenv import load_dotenv
load_dotenv()
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import login
from routers import register
from routers import search
from routers import reviews
from routers import get_db
import os

app = FastAPI()

templates = Jinja2Templates(directory="frontend/templates")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(register.router)
app.include_router(search.router)
app.include_router(reviews.router)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

