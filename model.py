from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(query, context):
    system_prompt = (
        "You are a helpful Teaching Assistant for IITM's Tools in Data Science course.\n"
        "Answer questions using the provided context. Be precise and cite supporting points."
    )
    user_prompt = f"Context:\n{context}\n\nQuestion:\n{query}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content
