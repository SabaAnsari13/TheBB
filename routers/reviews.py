from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from . import get_db
from .tables import Book, Review
from .schemas import BookDetailsResponse, ReviewResponse
from fastapi.templating import Jinja2Templates
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")  

@router.get("/books/{book_id}/details", response_class=HTMLResponse)
async def get_book_details(request: Request, book_id: int, db: Session = Depends(get_db)):
    # Query the database to retrieve the book details by its ID
    book = db.query(Book).filter(Book.book_id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Query the database to retrieve the reviews associated with the book
    reviews = db.query(Review).filter(Review.book_id == book_id).all()

    # Render the book details and associated reviews in the bookreview.html template
    return templates.TemplateResponse("bookdetails.html", {"request": request, "book": book, "reviews": reviews})


@router.get("/books/{book_id}/reviews", response_model=List[ReviewResponse])
async def get_reviews(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    return reviews