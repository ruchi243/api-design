from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, Todo
from schemas import TodoCreate, TodoUpdate, TodoResponse
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    existing = db.query(Todo).filter(Todo.id == todo_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    existing = db.query(Todo).filter(Todo.id == todo_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(existing)
    db.commit()
    return {"message": "Todo deleted"}