from pydantic import BaseModel, Field
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    description: str
    cover_image: str

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    review_text: str
    rating: int

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    review_text: str
    rating: int
    class Config:
        from_attributes = True

class UserActivityBase(BaseModel):
    user_id: int
    activity_type: str

class UserActivityCreate(UserActivityBase):
    pass

class UserActivity(UserActivityBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
