from sqlalchemy.orm import Session
from starlette import status
from lib.py_models.users import UserModel
from fastapi import HTTPException
from lib.database.tables import Overpayment,UserRolesEnum
from lib.utils.helpers import formatPhoneNumber


# GETTING ALL THE OVER PAYMENTS
def getOverpayments(db: Session, user: UserModel, skip: int, limit: int):
    if user.role != UserRolesEnum.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not an admin to access this data')
    try:
        return db.query(Overpayment).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error in getting all over payments: {e}")

# GETTING USER OVER PAYMENTS
def getUserOverpayments(db: Session, user: UserModel, phoneNumber: str):
    phone_number = formatPhoneNumber(phoneNumber)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    try:
        return db.query(Overpayment).filter(Overpayment.phone_number == phone_number).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error in getting user over payments: {e}")
    

    # GET OVERPAYMENT DETAILS
def getOverpayment(db: Session, user:UserModel, over_payment_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    try:
        return db.query(Overpayment).filter(Overpayment.id == over_payment_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR GETTING a single over payment: {e}")
