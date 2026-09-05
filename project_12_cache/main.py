from fastapi import FastAPI
from pydantic import BaseModel
from cache import SemanticCache
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="Semantic Cache Gateway", description="An API for caching and retrieving semantically similar queries.", version="1.0.0")
cache = SemanticCache(similarity_threshold=0.85)
model = genai.GenerativeModel("gemini-1.5-flash")

class QueryRequest(BaseModel):
    query: str

class CacheResponse(BaseModel):
    answer: str
    is_cached: bool
    similarity_score: float

@app.post("/chat")
async def semantic_cache_query(request: QueryRequest) -> CacheResponse:
    cached = cache.find_similar(request.query)

    if cached:
        return CacheResponse(
            answer=cached.response,
            is_cached=True,
            similarity_score=1.0
        )

    response = model.generate_content(request.query)
    answer = response.text

    cache.store(request.query, answer)

    return CacheResponse(
        answer=answer,
        is_cached=False,
        similarity_score=0.0
    )

@app.get("/cache/stats")
async def get_cache_stats():
    return cache.stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)