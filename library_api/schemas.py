from pydantic import BaseModel 
from typing import Optional 
from datetime import datetime

class MemberCreate(BaseModel):
    name: str 
    email: str

class MemberResponse(BaseModel):
    member_id: int
    name: str 
    email: str

    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    book_name: str 
    total_copies: int 

class BookResponse(BaseModel):
    book_id: int
    book_name: str
    total_copies: int
    available_copies: int

    class Config:
        from_attributes = True


class LoanCreate(BaseModel):
    book_id: int 
    member_id: int 

class LoanResponse(BaseModel):
    loan_id: int
    book_id: int
    member_id: int
    borrowed_at: datetime
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True
