from app.core.embeddings import generate_embedding
from app.db.vector_db import search_vectors
from app.services.rerank_service import rerank_results
from app.core.exceptions import BadRequestException


def retrieve_context(message: str):
    try:
        
        embedding = generate_embedding(message)
 
        results = search_vectors(embedding)

        if not results:
            return ""
  
        reranked_results = rerank_results(message, results)

        top_contexts = [
            r.payload.get("text", "")
            for r in reranked_results[:3]
            if r.payload and "text" in r.payload
        ]

        
        return "\n".join(top_contexts)

    except Exception as e:
        print(f"RAG error: {e}")
        raise BadRequestException(detail="Failed to retrieve context")