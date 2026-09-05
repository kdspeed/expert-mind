import google.generativeai as genai
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str) -> list:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return result['embedding']

def cosine_similarity(vec1: list, vec2: list) -> float:
    arr1, arr2 = np.array(vec1), np.array(vec2)
    dot_product = np.dot(arr1, arr2)
    magnitude = np.linalg.norm(arr1) * np.linalg.norm(arr2)
    return dot_product / magnitude if magnitude != 0 else 0.0