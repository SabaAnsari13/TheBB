from fastapi import APIRouter
from sqlalchemy import ARRAY, Date, Integer, PrimaryKeyConstraint, Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import engine


router = APIRouter()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  
    hashed_password = Column(String)
    reviews = relationship("Review", back_populates="user")
    activities = relationship("UserActivity", back_populates="user")

class Book(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    isbn = Column(String, unique=True, index=True)
    description = Column(String)
    cover_image = Column(String)
    reviews = relationship("Review", back_populates="book")

class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    book_id = Column(Integer, ForeignKey("books.book_id"))
    review_text = Column(String)
    rating = Column(Integer)

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")

class UserActivity(Base):
    __tablename__ = "user_activities"
    activity_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    activity_type = Column(String)
    timestamp = Column(DateTime, server_default=func.now())
    user = relationship("User", back_populates="activities")

Base.metadata.create_all(bind=engine)