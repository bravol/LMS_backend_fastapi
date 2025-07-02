from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from lib.database.tables import FAQ, UserRolesEnum
from lib.py_models.faqs import FAQModel, FAQUpdate
from lib.py_models.users import UserModel

# GETTING ALL FAQS
def getFAQs(db: Session,user:UserModel, skip: int, limit: int):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    try:
        return db.query(FAQ).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR GETTING FAQs: {e}")

# GETTING FAQ BY ID
def getFAQ(db: Session, user:UserModel, faq_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    try:
        return db.query(FAQ).filter(FAQ.id == faq_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR GETTING FAQ: {e}")

# CREATE NEW FAQ
def createFAQ(db: Session, user:UserModel, faq: FAQModel):
    if user.role != UserRolesEnum.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    try:
        db_faq = FAQ(**faq.model_dump())
        db.add(db_faq)
        db.commit()
        db.refresh(db_faq)
        return {"message": "FAQ created successfully", "status": 200}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR IN CREATING FAQ: {e}")


# UPDATE FAQ
def updateFAQ(db: Session, user:UserModel, faq_id: str, faq: FAQUpdate):
    if user.role != UserRolesEnum.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    try:
        db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
        if db_faq:
            # only update provided values and leave the rest untouched
            for key, value in faq.model_dump(exclude_unset=True).items():
                setattr(db_faq, key, value)
            db.commit()
        return {"message": "FAQ updated successfully", "status": 200}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR IN UPDATING FAQ: {e}")


# Delete FAQ
def deleteFAQ(db: Session, user:UserModel, faq_id: str):
    if user.role != UserRolesEnum.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    try:
        db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
        if db_faq:
            db.delete(db_faq)
            db.commit()
        return {"message": "FAQ deleted successfully", "status": 200}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR IN UPDATING FAQ: {e}")

