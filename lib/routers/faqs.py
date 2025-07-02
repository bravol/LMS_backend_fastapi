from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from lib.database.database import SessionLocal
from lib.py_models.users import UserModel
from lib.py_models.faqs import FAQModel,FAQUpdate
from lib.repo import auth, faqs


router = APIRouter(prefix='/faqs', tags=['FAQS'])

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserModel, Depends(auth.authenticate_request)]


# CREATE FAQ
@router.post("")
async def create_faq(db:db_dependency,user:user_dependency,faq:FAQModel):
    return faqs.createFAQ(db, user, faq)

# GET FAQS
@router.get("")
async def get_faqs(db:db_dependency, user:user_dependency, skip:int=0, limit:int=20):
    return faqs.getFAQs(db, user, skip, limit)

# GETTING FAQ
@router.get("/{faq_id}")
async def get_faq(db:db_dependency,user:user_dependency,faq_id:str):
    return faqs.getFAQ(db, user, faq_id)

# UPDATE FAQ
@router.put("/{faq_id}")
async def update_faq(db:db_dependency,user:user_dependency,faq_id:str, faq:FAQUpdate):
    return faqs.updateFAQ(db, user, faq_id, faq)

# DELETE FAQ
@router.delete("/{faq_id}")
async def delete_faq(db:db_dependency,user:user_dependency,faq_id:str):
    return faqs.deleteFAQ(db, user, faq_id)