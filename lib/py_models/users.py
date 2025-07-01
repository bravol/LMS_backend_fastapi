from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Login(BaseModel):
    phone_number: str
    password: str


# SIGNUP
class Signup(BaseModel):
    phone_number: str
    password: str
    full_name:str


# RESET PASSWORD  
class ResetPassword(BaseModel):
    phone_number: str
    new_password: str
    

# USER MODEL
class UserModel(BaseModel):
    full_name: Optional[str]
    nin: Optional[str]
    phone_number: Optional[str]
    profile_pic: Optional[str]
    email: Optional[str]
    loan_balance: Optional[float]
    loan_limit: Optional[float]
    verified: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    dob: Optional[datetime]
    role: Optional[str]
    gender: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]


# MODEL TO UPDATE USER
class UserUpdate(BaseModel):
    full_name: Optional[str]
    nin: Optional[str]
    profile_pic: Optional[str]
    email: Optional[str]

# CHANGE PASSWORD MODEL
class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    phone_number: str


# RESET PASSWORD
class ResetPassword(BaseModel):
    new_password: str
    phone_number: str
    

class AuthUser(BaseModel):
    phone_number: str
    role: str
    

class SuspendUser(BaseModel):
    phone_number: str
