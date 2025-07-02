
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FAQModel(BaseModel):
    question: str
    answer: str

class FAQUpdate(BaseModel):
    question: Optional[str]
    answer: Optional[str]