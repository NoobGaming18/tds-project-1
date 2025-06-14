import numpy as np
from numpy.linalg import norm
from openai import OpenAI
import tiktoken
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ENCODER = tiktoken.encoding_for_model("text-embedding-3-small")

def get_query_embedding(query):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[query]
    )
    return np.array(response.data[0].embedding)

def load_embeddings():
    data = np.load("./embeddings.npz", allow_pickle=True)
    return data["chunks"], data["vectors"]

def search_similar_chunks(query, top_k=3):
    chunks, vectors = load_embeddings()
    query_vec = get_query_embedding(query)
    sims = vectors @ query_vec / (norm(vectors, axis=1) * norm(query_vec) + 1e-8)
    top_indices = np.argsort(sims)[-top_k:][::-1]
    return [chunks[i] for i in top_indices]
