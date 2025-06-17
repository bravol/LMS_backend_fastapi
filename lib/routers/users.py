from fastapi import APIRouter
from lib.database.database import SessionLocal
from typing import Annotated 
from lib.py_models.users import UserModel
from fastapi import Depends
from sqlalchemy.orm import Session
from lib.repo import auth,users
from lib.py_models.users import Login,Signup,SuspendUser


router= APIRouter(prefix='/users',tags=['Users'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserModel,Depends(auth.authenticate_request)]


@router.post("/signup")
async def create_user(db:db_dependency,data:Signup):
    return users.signup_user(db=db,data=data)

@router.post("/login")
async def login(db: db_dependency,data: Login):
    return users.login_user(db=db,data=data)


# getting all users
@router.get("")
async def all_users(db: db_dependency, user:user_dependency, skip:int=0,limit:int=10):
    return users.get_users(db=db,user=user,skip=skip,limit=limit)

# getting users data
@router.get("/{phone_number}")
async def user_profile(phone_number: str, db: db_dependency, user:user_dependency):
    return users.get_user_data(db=db,user=user,phone_number=phone_number)

@router.post("/suspend_user")
async def user_suspended(db:db_dependency,user:user_dependency,data: SuspendUser):
    return users.suspend_user(db=db, user=user,data=data)