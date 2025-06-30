from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status
from lib.py_models.transaction import TransactionUpdate, TransactionModel, TransactionCreate
from lib.py_models.users import UserModel
from lib.database.tables import Transaction, TransactionStatusEnum,Loan
from lib.utils.helpers import formatPhoneNumber, identifyProvider


class TransactionRepo:

    # get all transactions
    @staticmethod
    def getTransactions(db: Session, user: UserModel, skip: int, limit: int):
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
        try:
            return db.query(Transaction).offset(skip).limit(limit).all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error in getting all transactions: {e}")

    # create transaction
    @staticmethod
    def createTransaction(db: Session, user:UserModel, transaction: TransactionCreate):
        phone_number = formatPhoneNumber(transaction.phone_number)
        provider = identifyProvider(transaction.phone_number)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

        active_loan = db.query(Loan).filter(Loan.id == transaction.loan_id,Loan.phone_number==phone_number,Loan.status.in_(['pending', 'approved']),Loan.loan_balance > 0).first()

        if not active_loan:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Loan not found")

        try:
            db_transaction = Transaction(
                phone_number = phone_number,
                user_phone = user.phone_number,
                loan_id = active_loan.id,
                amount = transaction.amount,
                charges = transaction.charges or 0,
                status = TransactionStatusEnum.successful,
                payment_method = provider,
                narration = f"Loan transaction for {transaction.amount} has been done"
            )
            db.add(db_transaction)
            db.commit()
            db.refresh(db_transaction)
            return {"message": "Transaction created successfully", "status": 200}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR IN CREATING TRANSACTION: {e}")

    # get single transaction
    @staticmethod
    def getTransaction(db: Session, user:UserModel, transaction_id: str):
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
        try:
            return db.query(Transaction).filter(Transaction.id == transaction_id).first()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR GETTING transaction: {e}")


    # Update an existing transaction
    @staticmethod
    def updateTransaction(db: Session, user:UserModel, transaction_id: str, transaction: TransactionUpdate):
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
        try:
            db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
            if db_transaction:
                # only update provided values and leave the rest untouched
                for key, value in transaction.model_dump(exclude_unset=True).items():
                    setattr(db_transaction, key, value)
                db.commit()
            return {"message": "Transaction updated successfully", "status": 200}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR IN UPDATING TRANSACTION: {e}")

    # Delete an FAQ
    @staticmethod
    def deleteTransaction(db: Session, user:UserModel, transaction_id: str):
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
        try:
            db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
            if db_transaction:
                db.delete(db_transaction)
                db.commit()
            return {"message": "Transaction deleted successfully", "status": 200}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR IN UPDATING TRANSACTION: {e}")

    @staticmethod
    def getUserTransactions(db: Session, user: UserModel, phoneNumber: str):
        phone_number = formatPhoneNumber(phoneNumber)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
        try:
            return db.query(Transaction).filter(Transaction.phone_number == phone_number,Transaction.user_phone == phone_number).all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error in getting user transactions: {e}")
