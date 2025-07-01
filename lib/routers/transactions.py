from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lib.database.database import SessionLocal
from lib.py_models.users import UserModel
from lib.py_models.transaction import TransactionCreate
from lib.repo import auth, transaction


router = APIRouter(prefix='/transactions', tags=['Transactions'])

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserModel, Depends(auth.authenticate_request)]

@router.get('')
def get_transactions(db:db_dependency,user:user_dependency, skip:int=0,limit:int=20):
    return transaction.getTransactions(db=db,user=user,skip=skip,limit=limit)

@router.get('/user/{phone_number}')
def get_user_transactions(db:db_dependency,user:user_dependency,phone_number:str):
    return transaction.getUserTransactions(db=db,user=user,phoneNumber=phone_number)

@router.get('/{transaction_id}')
def get_transaction(db:db_dependency,user:user_dependency,transaction_id:str):
    return transaction.getTransaction(db=db,user=user,transaction_id=transaction_id)

