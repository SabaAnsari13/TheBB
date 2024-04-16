from fastapi import APIRouter
from sqlalchemy import ARRAY, Date, Integer, PrimaryKeyConstraint, Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from . import engine

router = APIRouter()

Base = declarative_base()

class User(Base):
    __tablename__ = "creds"
    email = Column(String)
    username = Column(String, primary_key=True, index=True)
    password = Column(String)

class Search(Base):
    __tablename__ = "books"
    bkname = Column(String, primary_key=True, index=True)
    isbn = Column(Integer)
    author = Column(String)
    bkdesc = Column(String)
    cover_image = Column(String)

Base.metadata.create_all(bind=engine)