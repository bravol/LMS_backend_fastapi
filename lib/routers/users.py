from fastapi import APIRouter
from database.database import SessionLocal
from typing import Annotated 
from py_models.users import UserModel
from fastapi import Depends
from sqlalchemy.orm import Session
from repo.auth import authenticate_request

router= APIRouter(prefix='/users',tags='Users')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserModel,Depends(authenticate_request)]