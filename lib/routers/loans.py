from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lib.database.database import SessionLocal
from lib.py_models.users import UserModel
from lib.py_models.loans import LoanCreate, LoanRepay
from lib.repo import auth, loans


router = APIRouter(prefix='/loans', tags=['Loans'])

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserModel, Depends(auth.authenticate_request)]


# REQUEST LOAN
@router.post('/request-loan')
def request_loan(db:db_dependency, user:user_dependency, data:LoanCreate):
    return loans.requestLoan(db=db,user=user,data=data)

# REPAY LOAN
@router.post('/repay-loan')
def repay_loan(db:db_dependency, user:user_dependency, data:LoanRepay):
    return loans.repayLoan(db=db,user=user,data=data)

# GETTING ALL THE LOANS
@router.get("")
def get_loans(db:db_dependency, user:user_dependency, skip:int=0, limit:int=20):
    return loans.get_loans(db=db,user=user,skip=skip,limit=limit)


# GETTING UN PAID LOANS
@router.get("/unpaid-loans")
def get_unpaid_loans(db:db_dependency, user:user_dependency):
    return loans.getUnpaidLoans(db=db,user=user)

# GETTING USER UN PAID LOANS
@router.get("/unpaid-loans/{phone_number}")
def get_user_unpaid_loans(db:db_dependency, user:user_dependency,phone_number:str):
    return loans.getUserUnpaidLoan(db=db,user=user,phone_number=phone_number)

# GETTING USER LOANS
@router.get("/user/{phone_number}")
def get_user_loans(db:db_dependency, user:user_dependency, phone_number:str):
    return loans.get_user_loans(db=db,user=user,phone_number=phone_number)


# GETTING USER LOAN BALANCE
@router.get("/loan-balance/{phone_number}")
def get_user_loan_balance(db:db_dependency, user:user_dependency, phone_number:str):
    return loans.getUserLoanBalance(db=db,user=user,phone_number=phone_number)

# GETTING USER OVER DUE AMOUNT
@router.get("/overdue/{phone_number}")
def get_user_overdue(db:db_dependency, user:user_dependency, phone_number:str):
    return loans.getUserOverdueAmount(db=db,user=user,phone_number=phone_number)

# GETTING USER PAY BACK AMOUNT
@router.get("/payback/{phone_number}")
def get_user_payback(db:db_dependency, user:user_dependency, phone_number:str):
    return loans.getUserPayBackBalance(db=db,user=user,phone_number=phone_number)


# GETTING LOAN DETAILS
@router.get("/{loan_id}")
def get_loan_details(db:db_dependency, user:user_dependency, loan_id:str):
    return loans.get_loan_details(db=db,user=user,loan_id=loan_id)


