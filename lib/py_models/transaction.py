from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import Enum


# transaction update
class TransactionUpdate(BaseModel):
    phone_number: str = None
    amount: float = None
    transaction_type: str = None
    status: str = None


# request payment
class RequestPayment(BaseModel):
    phone_number: str
    amount: str
    narration: Optional[str] = None
    transaction_id: str


# LOAN REPAYMENT request
class RepayLoanModel(BaseModel):
    phone_number: str
    amount: float
    loan_id: str
    platform: Optional[str] = None


# TRANSACTION MODEL
class TransactionModel(BaseModel):
    id: str 
    phone_number: str
    user_phone: str
    amount: float
    loan_id:str
    charges:float
    status: str
    payment_method: Optional[str] 
    transaction_type: Optional[str]
    created_at: datetime
    updated_at: datetime


class TransactionCreate(BaseModel):
    phone_number: str
    amount: float
    loan_id: str
    charges: Optional[float] = 0

class OverpaymentBase(BaseModel):
    phone_number: Optional[str]
    loan_id: Optional[str]
    transaction_id: Optional[str]
    amount: float
    note: Optional[str]

class OverpaymentCreate(OverpaymentBase):
    pass

class OverpaymentUpdate(BaseModel):
    refunded: Optional[bool]
    note: Optional[str]

class TransactionStatus(str, Enum):
    pending = "pending"
    successful = "successful"
    failed = "failed"

class OverpaymentResponse(OverpaymentBase):
    id: str
    refunded: bool
    created_at: datetime
    updated_at: datetime



