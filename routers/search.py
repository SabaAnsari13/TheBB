from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from .tables import Book, Review
from .schemas import BookResponse
from . import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")



@router.get("/search", response_model=List[BookResponse])
async def search_books(
    title: str = Query(None),
    author: str = Query(None),
    isbn: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    
    if title:
        print('hi')
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if isbn:
        query = query.filter(Book.isbn == isbn)
    
    results = query.all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No books found matching the search criteria")
    
    return results

@router.get("/search/{book_id}", response_class=JSONResponse)
async def book_details(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    return templates.TemplateResponse("bookdetails.html", {"request": request, "book": book, "reviews": reviews})
