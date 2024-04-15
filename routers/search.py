from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Query
from .tables import Search  
from sqlalchemy.ext.declarative import declarative_base
import smtplib
import os
import random
from dotenv import load_dotenv
from . import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Load environment variables from .env file
load_dotenv()

# Base class for declarative models
Base = declarative_base()

@router.get("/search")
async def perform_search(search_term: str, db: Session = Depends(get_db)):
    # Construct the query using the Search model
    query = db.query(Search).filter(Search.bkname.ilike(f"%{search_term}%"))

    # Execute the query
    results = query.all()

    # Transform the results into dictionaries for easier serialization
    serialized_results = [result.__dict__ for result in results]

    return serialized_results