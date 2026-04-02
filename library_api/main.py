from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, Members, Books, Loans 
from schemas import MemberCreate, MemberResponse, BookCreate, BookResponse, LoanCreate, LoanResponse
from typing import List
from datetime import datetime

Base.metadata.create_all(bind = engine) 

app = FastAPI()

@app.get("/books", response_model = List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Books).all()

@app.post("/books", response_model=BookResponse)

def add_new_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Books(**book.model_dump(), available_copies = book.total_copies)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book 

@app.get("/members", response_model = List[MemberResponse])
def get_member(db: Session = Depends(get_db)):
    return db.query(Members).all()

@app.post("/members",response_model = MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    new_member = Members(**member.model_dump())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member 

@app.get("/loans", response_model = List[LoanResponse])
def get_loan(db: Session = Depends(get_db)):
    return db.query(Loans).all()

@app.post("/loans", response_model = LoanResponse)

def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    member = db.query(Members).filter(Members.member_id == loan.member_id).first()
    if not member:
        raise HTTPException(status_code = 404 , detail = "Member not found")
    book = db.query(Books).filter(Books.book_id == loan.book_id).first()
    if not book:
        raise HTTPException(status_code = 404 , detail = "Book not found")
    if book.available_copies == 0:
        raise HTTPException(status_code = 404, detail = "Book not available")
    
    new_loan = Loans(**loan.model_dump())
    book.available_copies -=1
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    
    return new_loan

@app.put("/loans/{loan_id}/return", response_model = LoanResponse)

def return_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loans).filter(Loans.loan_id == loan_id).first()
    if not loan:
        raise HTTPException(status_code = 404, detail = "Loan not Found")
    loan.returned_at = datetime.utcnow()
    book_id = loan.book_id 
    book = db.query(Books).filter(Books.book_id == book_id).first()
    book.available_copies += 1 
    db.commit()
    db.refresh(loan)
    return loan