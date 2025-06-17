from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from lib.database.database import SessionLocal
from lib.py_models.users import UserModel,UserUpdate
from lib.repo import auth, users


router = APIRouter(prefix='/users', tags=['Users'])

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserModel, Depends(auth.authenticate_request)]


# get all users
@router.get("")
def get_users(db: db_dependency, user: user_dependency, skip: int = 0, limit: int = 10):
    return users.get_users(db=db, user=user, skip=skip, limit=limit)

# get user details
@router.get("/{phone_number}")
def user_profile(phone_number: str, db: db_dependency, user: user_dependency):
    return users.get_user_data(db=db, user=user, phone_number=phone_number)


@router.put("/{phone_number}")
def update_user(db: db_dependency, user: user_dependency, data: UserUpdate, phone_number: str):
    return users.update_user(db=db, user=user,data=data, phone_number=phone_number)

@router.delete("/{phone_number}")
def delete_user(db: db_dependency, user: user_dependency, phone_number: str):
    return users.delete_user(db=db, user=user, phone_number=phone_number)





