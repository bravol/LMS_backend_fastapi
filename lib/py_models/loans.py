from pydantic import BaseModel
from datetime import datetime
from typing import Optional



# LOAN MODELS
class LoanBase(BaseModel):
    amount: float
    amount_paid: float
    created_at: datetime
    due_date: datetime
    is_cleared: bool
    loan_balance: float
    loan_period: int
    meter_number: str
    payback_amount: float
    phone_number: str
    rate: Optional[float] = None
    updated_at: datetime

class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    amount_paid: Optional[float]
    is_cleared: Optional[bool]
    loan_balance: Optional[float]
    updated_at: Optional[datetime]



# LOAN REPAYMENT request
class RepayLoanModel(BaseModel):
    phone_number: str
    amount: float
    loan_id: str
    platform: Optional[str] = None


# Request Loan Request
class RequestLoan(BaseModel):
    meter_number: str
    amount: float
    loan_plan_id: str
    platform: Optional[str] = None




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

    class Config:
        orm_mode = True

#







