from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from lib.py_models.loans import LoanCreate, LoanRepay
from lib.py_models.users import UserModel
from lib.database.tables import Loan, LoanStatusEnum, LoanPlan
from lib.utils.helpers import formatPhoneNumber
from datetime import datetime, timedelta

# A METHOD TO REQUEST LOAN
def requestLoan(db: Session, user: UserModel, data: LoanCreate):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    previous_loans = db.query(Loan).filter(Loan.phone_number == user.phone_number).all()

    if not previous_loans:
        if data.amount > 5000:
            return {"message":"As a first-time borrower, you can only request up to 5000","status":403}
    else:
        unpaid_loans = [loan for loan in previous_loans if not loan.is_cleared]
        if unpaid_loans:
            return {"message":"You still have unpaid loans. Please clear them before requesting another", "status":403}

    charges = data.amount * 0.01
    paybackAmount = data.amount + charges
    loan_plan = db.query(LoanPlan).filter(LoanPlan.id == data.loan_plan_id).first()

    if not loan_plan:
        raise HTTPException(status_code=404, detail="Loan plan not found")
    due_date = datetime.now() + timedelta(days=loan_plan.duration)

    new_loan = Loan(
        amount=data.amount,
        loan_plan_id=data.loan_plan_id,
        charges=charges,
        loan_balance=paybackAmount,
        payback_amount=paybackAmount,
        phone_number=user.phone_number,
        due_date=due_date,
        status=LoanStatusEnum.approved
    )
   # update the user loan balance
    user.loan_balance += paybackAmount

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    db.refresh(user)
    return {"message": "Loan request submitted successfully", "status": 200}



#  A METHOD TO REPAY A LOAN
def repayLoan(db: Session, user: UserModel, data:LoanRepay):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    loan = db.query(Loan).filter(Loan.id == data.loan_id,Loan.phone_number == user.phone_number).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.is_cleared:
        raise HTTPException(status_code=400, detail="Loan is already fully repaid")

    if data.repayment_amount <= 0:
        raise HTTPException(status_code=400, detail="Repayment amount must be greater than zero")

    if data.repayment_amount > loan.loan_balance:
        raise HTTPException(status_code=400, detail="Repayment amount exceeds remaining loan balance")

    #Update loan fields
    loan.loan_balance -= data.repayment_amount
    loan.amount_paid = (loan.amount_paid or 0) + data.repayment_amount
    loan.updated_at = datetime.now()
    loan.last_repayment_date = datetime.now()

    #If fully repaid, clear loan and reward user
    if loan.loan_balance <= 0:
        loan.loan_balance = 0
        loan.is_cleared = True
        loan.status = LoanStatusEnum.cleared
        #Increase user loan limit by 5000
        user.loan_limit += 5000

    active_loans = db.query(Loan).filter(Loan.phone_number == user.phone_number,Loan.is_cleared == False).all()
    user.loan_balance = sum(loan.loan_balance for loan in active_loans)

    db.commit()
    db.refresh(loan)
    db.refresh(user)

    return {"message": f"Repayment of {data.repayment_amount} received successfully.","status": 200}




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
def updateLoan(db: Session, user:UserModel,loan_id: str, updates: dict):
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
