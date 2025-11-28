import uuid
from typing import List
from qdrant_client.models import PointStruct
from config.setting import env

class SaveDocument:
    def __init__(self, qdrant, memory_store):
        self.client = qdrant.client
        self.is_active = qdrant.is_active
        self.memory_store= memory_store
    def save(self, text: str, vector: List[float]) -> int:
        doc_id = str(uuid.uuid4()) # Simple ID logic
        
        if self.is_active:
            payload = {"text": text}
            self.client.upsert(
                collection_name=env.COLLECTION_NAME,
                points=[PointStruct(id=doc_id, vector=vector, payload=payload)]
            )
        
        self.memory_store.append({"id": doc_id, "text": text})
        return doc_id