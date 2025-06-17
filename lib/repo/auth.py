from jose import jwt, JWTError
from lib.utils import helpers
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from lib.database.tables import User
from lib.py_models.users import Login,UserModel
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status, Depends



SECRET_KEY = '00cf6789e9cf6ecf780bf12b6117376ff91d8738c7008960481def44977d9bf8'
ALGORITHM = 'HS256'
security = HTTPBearer()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# AUTHENTICATE USER
def authenticate_user(user:Login, db:Session):
    phone_number=helpers.formatPhoneNumber(user.phone_number)
    user_db = db.query(User).filter(User.phone_number==phone_number).first()
    verify_user= bcrypt_context.verify(user.password, user_db.password)

    if not user_db or not verify_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid phone number or password")