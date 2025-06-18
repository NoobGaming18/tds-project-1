import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from app.prompt import build_prompt
from app.utils import search_similar_chunks

load_dotenv("OPENAI_API_KEY.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  

def generate_answer(question: str):
    top_chunks, top_metadata = search_similar_chunks(question, top_k=5)

    context = "\n\n".join(top_chunks)

    urls = list({m["url"] for m in top_metadata})[:2]

    prompt = build_prompt(context, question)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = completion.choices[0].message.content

    return {
        "answer": answer,
        "links": [{"url": u, "text": f"Reference {i+1}"} for i, u in enumerate(urls)]
    }
