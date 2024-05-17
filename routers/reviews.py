from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import get_db
from .tables import Review, Book, User
from .auth import get_current_user
from .schemas import ReviewCreate, ReviewResponse
from . import get_db
from typing import List

router = APIRouter()

@router.post("/books/{book_id}/reviews", response_model=ReviewResponse)
async def create_review(book_id: int, review: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_review = Review(user_id=current_user.id, book_id=book_id, review_text=review.review_text, rating=review.rating)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review

@router.get("/books/{book_id}/reviews", response_model=List[ReviewResponse])
async def get_reviews(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    return reviews
