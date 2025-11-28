from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from config.setting import env

class QdrantConnection:
    def __init__(self):
        self.is_active = False
        self._init_connection()

    def _init_connection(self):
        try:
            self.client = QdrantClient(env.QDRANT_URL)
            self.client.recreate_collection(
                collection_name=env.COLLECTION_NAME,
                vectors_config=VectorParams(size=128, distance=Distance.COSINE)
            )
            self.is_active = True
            print("Qdrant Connected")
        except Exception as e:
            print(f"Qdrant Offline ({e}). Using In-Memory Fallback.")
            self.is_active = False