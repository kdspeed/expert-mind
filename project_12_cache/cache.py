from typing import Dict, Optional
from dataclasses import dataclass
from embeddings import get_embedding, cosine_similarity

@dataclass
class CachedQuery:
    query: str
    embedding: list
    response: str
    hits: int = 0

class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.85):
        self.cache: Dict[str, CachedQuery] = {}
        self.threshold = similarity_threshold

    def find_similar(self, query: str) -> Optional[CachedQuery]:
        query_embedding = get_embedding(query)
        best_match = None
        best_score = 0

        for cached in self.cache.values():
            score = cosine_similarity(query_embedding, cached.embedding)
            if score > best_score:
                best_score = score
                best_match = cached

        if best_score >= self.threshold:
            best_match.hits += 1
            return best_match
        return None

    def store(self, query: str, response: str) -> None:
        embedding = get_embedding(query)
        self.cache[query] = CachedQuery(
            query=query,
            embedding=embedding,
            response=response
        )

    def stats(self) -> dict:
        return {
            "total_cached": len(self.cache),
            "total_hits": sum(c.hits for c in self.cache.values())
        }