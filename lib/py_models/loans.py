from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class LoanCreate(BaseModel):
    amount:float
    loan_plan_id:str


class LoanRepay(BaseModel):
    repayment_amount: float
    loan_id: str


# LOAN PLAN MODELS
class LoanPlanCreate(BaseModel):
    interest_rate: float
    duration: int


class LoanPlanUpdate(BaseModel):
    interest_rate: Optional[float] = None
    duration: Optional[int] = None

class LoanPlanModel(BaseModel):
    id: int
    interest_rate: float
    duration: int
    created_at: datetime
    updated_at: datetime









