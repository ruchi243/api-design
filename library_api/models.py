from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base
from datetime import datetime

class Members(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    email = Column(String)

class Books(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key = True, index = True)
    book_name = Column(String, nullable = False)
    total_copies = Column(Integer, nullable = False)
    available_copies = Column(Integer, nullable = False)

class Loans(Base):
    __tablename__ = "loans"

    loan_id = Column(Integer, primary_key = True, index = False)

    member_id = Column(String, ForeignKey("members.member_id"), nullable = False)
    book_id = Column(String, ForeignKey("books.book_id"), nullable = False)
    borrowed_at = Column(DateTime, default = datetime.utcnow, nullable = False)
    returned_at = Column(DateTime, nullable = True)