from pydantic import BaseModel
from typing import Optional

class TodoItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoItemCreate(TodoItemBase):
    pass

class TodoItem(TodoItemBase):
    id: int

    class Config:
        orm_mode = True