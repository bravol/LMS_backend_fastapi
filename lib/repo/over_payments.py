from sqlalchemy.orm import Session
from starlette import status
from lib.py_models.users import UserModel
from fastapi import HTTPException
from lib.database.tables import Overpayment
from lib.utils.helpers import formatPhoneNumber



def getOverpayments(db: Session, user: UserModel, skip: int, limit: int):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    try:
        return db.query(Overpayment).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error in getting all over payments: {e}")

def getUserOverpayments(db: Session, user: UserModel, phoneNumber: str):
    phone_number = formatPhoneNumber(phoneNumber)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    try:
        return db.query(Overpayment).filter(Overpayment.phone_number == phone_number).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error in getting user over payments: {e}")
