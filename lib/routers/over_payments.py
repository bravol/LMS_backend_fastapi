from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from lib.database.database import SessionLocal
from lib.py_models.users import UserModel
from lib.repo import auth, over_payments


router = APIRouter(prefix='/overpayments', tags=['OverPayments'])

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserModel, Depends(auth.authenticate_request)]

# GETTING ALL THE OVER PAYMENTS
@router.get('')
def get_overpayments(db:db_dependency,user:user_dependency,skip:int=0,limit:int=20):
    return over_payments.getOverpayments(db=db,user=user,skip=skip,limit=limit)

# GETTING USER OVER PAYMENTS
@router.get('/user/{phone_number}')
def get_user_overpayments(db:db_dependency,user:user_dependency,phone_number:str):
    return over_payments.getUserOverpayments(db=db,user=user,phoneNumber=phone_number)

# GETTING OVER PAYMENT DETAILS
@router.get('/{over_payment_id}')
def get_overpayment(db:db_dependency,user:user_dependency,over_payment_id:str):
    return over_payments.getOverpayment(db=db,user=user,over_payment_id=over_payment_id)