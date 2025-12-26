from fastapi import FastAPI
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/todo/")
def home():
    return  {"message": "Todo API is running"}