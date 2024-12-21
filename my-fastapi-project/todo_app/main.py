from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from models import TodoItem
from schemas import TodoItemCreate, TodoItem as TodoItemSchema

DATABASE_URL = "sqlite:///./data/todo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/items", response_model=TodoItemSchema)
def create_todo(item: TodoItemCreate):
    db: Session = SessionLocal()
db_item = TodoItem(item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items", response_model=list[TodoItemSchema])
def read_todos(skip: int = 0, limit: int = 10):
    db: Session = SessionLocal()
    return db.query(TodoItem).offset(skip).limit(limit).all()

@app.get("/items/{item_id}", response_model=TodoItemSchema)
def read_todo(item_id: int):
    db: Session = SessionLocal()
    item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=TodoItemSchema)
def update_todo(item_id: int, item: TodoItemCreate):
    db: Session = SessionLocal()
    db_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    return db_item

@app.delete("/items/{item_id}")
def delete_todo(item_id: int):
    db: Session = SessionLocal()
    db_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}