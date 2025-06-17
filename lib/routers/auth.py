from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lib.database.database import SessionLocal
from lib.py_models.users import UserModel, Login, Signup,ChangePassword,ResetPassword
from lib.repo import auth, users


router = APIRouter(tags=['Auth'])

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserModel, Depends(auth.authenticate_request)]

@router.post("/signup")
async def create_user(db: db_dependency, data: Signup):
    return users.signup_user(db=db, data=data)

@router.post("/login")
async def login(db: db_dependency, data: Login):
    return users.login_user(db=db, data=data)


@router.post("/change_password")
def change_password(db: db_dependency, user: user_dependency, data: ChangePassword):
    return users.changePassword(db=db, user=user, data=data)

@router.post("/reset_password")
def reset_password(db: db_dependency, data: ResetPassword):
    return users.reset_password(db=db, data=data)
