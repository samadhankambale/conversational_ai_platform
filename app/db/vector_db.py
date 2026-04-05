from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from app.core.config import QDRANT_URL

client = QdrantClient(url=QDRANT_URL)

COLLECTION_NAME = "conversations"

def init_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

def upsert_vector(id: str, vector, payload: dict):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(id=id, vector=vector, payload=payload)
        ]
    )

def search_vectors(query_vector, limit=5):
    return client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    ).points