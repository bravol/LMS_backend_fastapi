from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from lib.py_models.loans import LoanCreate
from lib.py_models.users import UserModel
from lib.database.tables import Loan, LoanStatusEnum
from lib.utils.helpers import formatPhoneNumber
from datetime import datetime

# A METHOD TO REQUEST LOAN


#  A METHOD TO REPAY A LOAN



# GETTING LOANS
def get_loans(db: Session,user:UserModel, skip: int, limit: int):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    try:
        return db.query(Loan).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ERROR GETTING Loans: {e}")
    

# GETTING USER LOANS
def get_user_loans(db:Session,user:UserModel,phone_number:str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    phoneNumber= formatPhoneNumber(phone_number)
    try:
        return db.query(Loan).filter(Loan.phone_number == phoneNumber).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"failed to get user loans: {e}")
    
# GETTING SINGLE LOAN
def get_loan_details(db:Session,user:UserModel,loan_id:str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    try:
        return db.query(Loan).filter(Loan.id == loan_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"failed to loan details: {e}")

# UPDATING LOAN
def updteLoan(db: Session, user:UserModel,loan_id: str, updates: dict):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    try:
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        for key, value in updates.items():
            if hasattr(loan, key):
                setattr(loan, key, value)
        db.commit()
        db.refresh(loan)
        return {"message": "Loan updated successfully", "loan": loan}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Loan could not be updated")
    

    # METHOD TO GET USER UNPAID LOANS
def getUnpaidLoans(db: Session, user:UserModel, phone_number: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    phoneNumber=formatPhoneNumber(phone_number)
    try:
        return db.query(Loan).filter(Loan.phone_number == phoneNumber,Loan.status.in_([LoanStatusEnum.approved, LoanStatusEnum.overdue, LoanStatusEnum.defaulted])).all()
    except Exception as e:
        return None


    #GET USER UNPAID LOAN
def getUserUnpaidLoan(db: Session,user:UserModel, phone_number: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    phoneNumber=formatPhoneNumber(phone_number)
    try:
        return db.query(Loan).filter(Loan.phone_number == phoneNumber,Loan.status.in_([LoanStatusEnum.approved, LoanStatusEnum.overdue, LoanStatusEnum.defaulted])).first()
    except Exception as e:
        return None
    

# GETTING USER LOAN BALANCE
def getUserLoanBalance(db: Session, user: UserModel, phone_number: str) -> float:
    if not user:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication Failed")
    phoneNumber = formatPhoneNumber(phone_number)
    try:
        loans = db.query(Loan).filter(Loan.phone_number == phoneNumber,Loan.status == LoanStatusEnum.approved).all()
        loan_balance = sum(loan.amount for loan in loans)
        return loan_balance
    except Exception as e:
        return 0.0
    
# GETTING USER PAYBACK AMOUNT
def getUserPayBackBalance(db: Session, user: UserModel, phone_number: str) -> float:
    if not user:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication Failed")
    phoneNumber = formatPhoneNumber(phone_number)
    try:
        loans = db.query(Loan).filter(Loan.phone_number == phoneNumber).all()
        amount = sum(loan.loan_balance for loan in loans)
        return amount
    except Exception as e:
        return 0.0
    
# GETTING USER PAYBACK AMOUNT
def getUserOverdueAmount(db: Session, user: UserModel, phone_number: str) -> float:
    if not user:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication Failed")
    phoneNumber = formatPhoneNumber(phone_number)
    try:
        current_date = datetime.now()
        loans = db.query(Loan).filter(Loan.phone_number == phoneNumber,Loan.due_date <= current_date,Loan.status == LoanStatusEnum.approved).all()
        amount = sum(loan.loan_balance for loan in loans)
        return amount
    except Exception as e:
        return 0.0
