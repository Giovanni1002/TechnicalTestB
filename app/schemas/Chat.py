from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    question: str

class DocumentRequest(BaseModel):
    text: str
