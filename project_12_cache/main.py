from fastapi import FastAPI
from pydantic import BaseModel
from cache import SemanticCache
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app= FastAPI(title="Semantic Cache API", description="An API for caching and retrieving semantically similar queries.", version="1.0.0")
cache = SemanticCache(similarity_threshold=0.85)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class QueryRequest(BaseModel):
    query: str
    model: str = "gpt-4o-mini"

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
    
    response = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.query}]
    )
    
    answer = response.choices[0].message.content
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