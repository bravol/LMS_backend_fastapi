from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from lib.database.tables import LoanPlan
from lib.py_models.loans import LoanPlanCreate, LoanPlanUpdate
from lib.py_models.users import UserModel
from lib.utils.helpers import tz


# GETTING LOAN PLANS
def getLoanPlans(db: Session, user: UserModel):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    try:
        return db.query(LoanPlan).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error in getting loan plans: {e}")

# GETTING A SPECIFIC LOAN PLAN
def getLoanPlan(db: Session, user: UserModel, plan_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    try:
        return db.query(LoanPlan).filter(LoanPlan.id == plan_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error in getting loan plan: {e}")

# UPDATE LOAN PLAN
def updateLoanPlan(db: Session, user: UserModel, plan_id: str, loan_plan_update: LoanPlanUpdate):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    loan_plan = db.query(LoanPlan).filter(LoanPlan.id == plan_id).first()
    if loan_plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan plan not found")
    # create a dictionary for the field to update
    update_dict = loan_plan_update.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(loan_plan, key, value)

    loan_plan.updated_at = datetime.now(tz)

    try:
        db.commit()
        db.refresh(loan_plan)
        return {"message": "Loan plan updated successfully", "Loan plan": loan_plan}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Failed to update loan plan: {e}")

# CREATING LOAN PLAN
def createLoanPlan(db: Session, user: UserModel, data: LoanPlanCreate):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    new_plan = LoanPlan(**data.model_dump())
    try:
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
        return {"message":"loan plan created successfully","status":200}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating plan: {e}")

# DELETE LOAN PLAN
def deleteLoanPlan(db: Session, user: UserModel, plan_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    loan_plan = db.query(LoanPlan).filter(LoanPlan.id == plan_id).first()
    if not loan_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Loan plan not found")
    try:
        db.delete(loan_plan)
        db.commit()
        return {"message":"Loan plan deleted successfully","status":200}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error in deleting loan plan: {e}")
