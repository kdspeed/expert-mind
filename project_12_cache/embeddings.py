from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str) -> list:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(vec1: list, vec2: list) -> float:
    arr1, arr2 = np.array(vec1), np.array(vec2)
    dot_product = np.dot(arr1, arr2)
    magnitude = np.linalg.norm(arr1) * np.linalg.norm(arr2)
    return dot_product / magnitude if magnitude != 0 else 0.0