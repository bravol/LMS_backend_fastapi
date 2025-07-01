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


# RESET PASSWORD  
class ChangeRole(BaseModel):
    phone_number: str
    role: str

# TOGGLE USER STATUS
class ToggleUserStatus(BaseModel):
    phone_number: str
    is_active: bool

# USER MODEL
class UserModel(BaseModel):
    full_name: Optional[str] = None
    nin: Optional[str] = None
    phone_number: Optional[str] = None
    profile_pic: Optional[str] = None
    email: Optional[str] = None
    loan_balance: Optional[float] = None
    loan_limit: Optional[float] = None
    verified: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    dob: Optional[datetime] = None
    role: Optional[str] = None
    gender: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


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

# RESET PASSWORD
class ResetPassword(BaseModel):
    new_password: str
    phone_number: str
    

class AuthUser(BaseModel):
    phone_number: str
    role: str
    

class SuspendUser(BaseModel):
    phone_number: str
