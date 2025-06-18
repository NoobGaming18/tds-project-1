from fastapi import FastAPI
from app.schema import Query
from app.model import generate_answer

app = FastAPI()

@app.post("/api")
def answer_query(payload: Query):
    return generate_answer(payload.question)
