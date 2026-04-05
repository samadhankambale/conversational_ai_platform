from app.core.embeddings import generate_embedding
from app.db.vector_db import search_vectors
from app.core.exceptions import BadRequestException



def retrieve_context(message: str):
    try:
        embedding = generate_embedding(message)
        results = search_vectors(embedding)
        return results
    except Exception as e:
        print(f"RAG error: {e}")
        raise BadRequestException(detail="Failed to retrieve context")