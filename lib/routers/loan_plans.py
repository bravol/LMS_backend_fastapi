from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from lib.database.database import SessionLocal
from lib.py_models.users import UserModel
from lib.py_models.loans import LoanPlanCreate, LoanPlanModel,LoanPlanUpdate
from lib.repo import auth, loan_plans


router = APIRouter(prefix='/loan-plans', tags=['Loan Plans'])

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserModel, Depends(auth.authenticate_request)]

# GET ALL LOAN PLANS
@router.get('')
def get_loan_plans(db: db_dependency, user: user_dependency):
    return loan_plans.getLoanPlans(db=db, user=user)

# GET LOAN PLAN BY ID
@router.get('/{loan_plan_id}')
def get_loan_plan(db: db_dependency, user: user_dependency, loan_plan_id: str):
    return loan_plans.getLoanPlan(db=db, user=user, plan_id=loan_plan_id)

# CREATE LOAN PLAN
@router.post('')
def create_loan_plan(db: db_dependency, user: user_dependency, data: LoanPlanCreate):
    return loan_plans.createLoanPlan(db=db, user=user, data=data)

# UPDATE LOAN PLAN
@router.put('/{loan_plan_id}')
def update_loan_plan(db: db_dependency, user: user_dependency, data: LoanPlanUpdate, loan_plan_id: str):
    return loan_plans.updateLoanPlan(db=db, user=user, plan_id=loan_plan_id, loan_plan_update=data)

# DELETE LOAN PLAN
@router.delete('/{loan_plan_id}')
def delete_loan_plan(db: db_dependency, user: user_dependency, loan_plan_id: str):
    return loan_plans.deleteLoanPlan(db=db, user=user, plan_id=loan_plan_id)
