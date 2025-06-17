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
def authenticate_user(db:Session,user:Login):
    phone_number=helpers.formatPhoneNumber(user.phone_number)
    user_db = db.query(User).filter(User.phone_number==phone_number).first()
    verify_user= bcrypt_context.verify(user.password, user_db.password)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found in the database")

    if not verify_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid phone number or password")
    return UserModel.model_validate(user_db) 
# cleanly returns a validated Pydantic model

# CREATING ACCESS TOKEN
def create_access_token(user:UserModel, expires_delta:timedelta):
    phone_number=helpers.formatPhoneNumber(user.phone_number)
    encode ={"phone_number":phone_number,"role":user.role}
    expires =datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# DECRYPT AND VERIFY THE TOKEN
def authenticate_request(credentials: HTTPAuthorizationCredentials=Depends(security)):
    try:
        payload= jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        exp=payload.get('exp')
        if exp:
            exp_datetime= datetime.fromtimestamp(exp, tz=timezone.utc)
            if datetime.now(timezone.utc) > exp_datetime:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Token expired')
            
            # extract user info from payload
            phone_number:str= payload.get('phone_number')
            role:str= payload.get('role')

            if phone_number is None or role is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Access denied,  Could not validaate the user')
            return {"phone_number":phone_number, 'role':role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied, Invalid token received")

# ENCRYPTING PASSWORD
def has_password(password:str):
    return bcrypt_context.hash(password)

# VERIFY PASSWORD
def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)