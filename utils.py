import os
import tiktoken
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("OPENAI_API_KEY.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tokenizer = tiktoken.get_encoding("cl100k_base")

def get_embedding(text: str) -> list[float]:
    """Generate embedding vector for the input text."""
    return client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    ).data[0].embedding

def search_similar_chunks(query: str, top_k: int = 5):
    """Return top-k most similar text chunks and their reference URLs."""
    data = np.load("data/embeddings.npz", allow_pickle=True)
    chunks = data["chunks"]
    embeddings = data["embeddings"]
    metadata = data["metadata"]
    query_vec = get_embedding(query)
    query_vec = np.array(query_vec)
    embeddings = np.array(embeddings)
    scores = np.dot(embeddings, query_vec) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_vec)
    )
    top_indices = np.argsort(scores)[-top_k:][::-1]

    top_chunks = [str(chunks[i]) for i in top_indices]
    top_metadata = [metadata[i] for i in top_indices] 

    return top_chunks, top_metadata

   