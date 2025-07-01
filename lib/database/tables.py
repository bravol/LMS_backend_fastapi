from sqlalchemy import Boolean, Column, DateTime, Date, Enum as SQLEnum, ForeignKey, Integer, String, Float, UniqueConstraint, func
from sqlalchemy.orm import relationship
import enum 
from lib.database.database import Base
from uuid import uuid4

# TIMESTAMP MIXIN TO AVOID REPITION OF DATE
class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class LoanStatusEnum(enum.Enum):
    pending = "pending"
    approved = "approved"
    cleared = "cleared"
    overdue = "overdue"
    defaulted = "defaulted"
    failed = "failed"

class TransactionStatusEnum(enum.Enum):
    pending = "pending"
    successful = "successful"
    failed = "failed"
class TransactionTypeEnum(enum.Enum):
    request_loan = "request Loan"
    repay_loan = "repay loan"

class UserRolesEnum(enum.Enum):
    admin='admin'
    user='user'
    manager='manager'
    support='support'

    
# USERS TABLE
class User(Base, TimestampMixin):
    __tablename__ = "users"

    phone_number = Column(String(30), primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    nin = Column(String(100), nullable=True)
    profile_pic = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    password = Column(String(100), nullable=False)
    loan_balance = Column(Float, nullable=True, default=0)
    loan_limit = Column(Float, nullable=True, default=0)
    verified = Column(Boolean, nullable=True, default=False)
    role = Column(String(100), nullable=False, default="user")
    is_active = Column(Boolean,nullable=False, default=True)
    gender = Column(String(100), nullable=True)
    dob = Column(Date, nullable=True)
    
    loans = relationship("Loan", back_populates="user", passive_deletes=True)
    transactions = relationship("Transaction", back_populates="user", passive_deletes=True)


# LOANS TABLE
class Loan(Base, TimestampMixin):
    __tablename__ = "loans"

    id = Column(String(50),primary_key=True, default=lambda: uuid4().hex)
    phone_number = Column(String(30), ForeignKey("users.phone_number", ondelete='SET NULL'), nullable=True)
    amount = Column(Float, nullable=False)
    amount_paid = Column(Float, nullable=True, default=0)
    charges = Column(Float, nullable=True)
    payback_amount = Column(Float, nullable=False)
    is_cleared=  Column(Boolean, nullable=True, default=False)
    penalty = Column(Float, nullable=True, default=0)
    loan_balance = Column(Float, nullable=False)
    loan_plan_id = Column(String(50), ForeignKey("loan_plans.id", ondelete='SET NULL'), nullable=True)
    due_date = Column(DateTime, nullable=False)
    status = Column(SQLEnum(LoanStatusEnum), nullable=False, default=LoanStatusEnum.pending, index=True)
    last_repayment_date = Column(DateTime, nullable=True)
    loan_plan = relationship("LoanPlan", back_populates="loan", passive_deletes=True)
    user = relationship("User", back_populates="loans", passive_deletes=True)
    transactions = relationship("Transaction", back_populates="loan", passive_deletes=True)



# TRANSACTIONS TABLE
class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(String(50),primary_key=True, default=lambda: uuid4().hex)
    phone_number = Column(String(30), ForeignKey("users.phone_number", ondelete='SET NULL'), nullable=True, index=True)
    loan_id = Column(String(50), ForeignKey("loans.id", ondelete='SET NULL'), nullable=True, index=True)
    amount = Column(Float, nullable=False)
    charges = Column(Float, nullable=True)
    status = Column(SQLEnum(TransactionStatusEnum), nullable=False, default=TransactionStatusEnum.pending)
    payment_method = Column(String(100), nullable=True)
    transaction_type = Column(String(50), nullable=True)
    
    user = relationship("User", back_populates="transactions", passive_deletes=True)
    loan = relationship("Loan", back_populates="transactions", passive_deletes=True)


# LOAN PLANS
class LoanPlan(Base, TimestampMixin):
    __tablename__ = "loan_plans"

    id = Column(String(50),primary_key=True, default=lambda: uuid4().hex)
    interest_rate = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    
    loan = relationship("Loan", back_populates="loan_plan", passive_deletes=True)


    
# FREQUENTLY ASKED QUESTIONS
class FAQ(Base, TimestampMixin):
    __tablename__ = "faqs"

    id = Column(String(50),primary_key=True, default=lambda: uuid4().hex)
    question = Column(String(500), index=True, nullable=False)
    answer = Column(String(1000), nullable=True)



# TABLE TO HANDLE OVERPAYMENTS
class Overpayment(Base, TimestampMixin):
    __tablename__ = "overpayments"

    id = Column(String(50),primary_key=True, default=lambda: uuid4().hex)
    phone_number = Column(String(30), ForeignKey("users.phone_number", ondelete='SET NULL'), nullable=True, index=True)
    loan_id = Column(String(50), ForeignKey("loans.id", ondelete='SET NULL'), nullable=True, index=True)
    transaction_id = Column(String(50), ForeignKey("transactions.id", ondelete='SET NULL'), nullable=True, index=True)
    overpaid_amount = Column(Float, nullable=False)
    refunded = Column(Boolean, default=False, nullable=False)      
    # Relationships
    user = relationship("User", backref="overpayments", passive_deletes=True)
    loan = relationship("Loan", backref="overpayments", passive_deletes=True)
    transaction = relationship("Transaction", backref="overpayments", passive_deletes=True)



    
    

