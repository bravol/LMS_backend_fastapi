from pydantic import BaseModel
from datetime import datetime
from typing import Optional



# LOAN MODELS
class LoanBase(BaseModel):
    amount: float
    created_at: datetime
    due_date: datetime
    is_cleared: bool
    loan_balance: float
    loan_plan_id: str
    payback_amount: float
    phone_number: str
    updated_at: datetime
    status: str

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









