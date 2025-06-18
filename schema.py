from pydantic import BaseModel
from typing import Optional

class Query(BaseModel):
    question: str
    image: Optional[str] = None  # Reserved for future use

class Answer(BaseModel):
    answer: str
    links: list[dict]
