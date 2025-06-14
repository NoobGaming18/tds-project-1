from fastapi import FastAPI, Request
from dotenv import load_dotenv
load_dotenv("openAI_api_key.env")
from pydantic import BaseModel
from model import generate_answer
from search import search_similar_chunks
from typing import Optional
import os

app = FastAPI()

class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None  # base64 optional

@app.post("/api/")
def answer_query(payload: QueryInput):
    chunks = search_similar_chunks(payload.question)
    context = "\n\n---\n\n".join(chunks)
    answer = generate_answer(payload.question, context)

    # Fake placeholder links (you can enhance this using topic_id in future)
    links = [
        {"url": "https://discourse.onlinedegree.iitm.ac.in", "text": "Reference 1"},
        {"url": "https://discourse.onlinedegree.iitm.ac.in", "text": "Reference 2"}
    ]
    
    return {"answer": answer, "links": links}
