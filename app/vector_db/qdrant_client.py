from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "chat_collection"

def init_qdrant():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=3,
            distance=Distance.COSINE
        )
    )