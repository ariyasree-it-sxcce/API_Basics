from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models 
from database import SessionLocal, engine

#Create tables in database
models.Base.metadata.create_all(bind=engine)

ariya = FastAPI()

# Database dependency
def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Home route
@ariya.get("/")
def home():
    return  {"message": "Todo API is running"}

#REQUEST BODY MODEL
class TodoItemCreate(BaseModel):
    title: str

#ADD TODO ITEM
@ariya.post("/tasks")
def add_task(todo: TodoItemCreate, db : Session = Depends(get_db)):
    new_task = models.Todo(title=todo.title,completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

#View ALL TODO ITEMS
@ariya.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

#Mark TODO ITEM AS COMPLETED
@ariya.put("/tasks/{task_id}")
def mark_task_completed(task_id: int, db: Session = Depends(get_db)):
    task= db.query(models.Todo).filter(models.Todo.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    task.completed = True
    db.commit()
    return {"message": "Task marked as completed"}  

#DELETE TODO ITEM
@ariya.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task= db.query(models.Todo).filter(models.Todo.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    if not task.completed:
        return {"error": "Task not completed yet"}
    db.delete(task)
    db.commit()     
    return {"message": "Task deleted successfully"}