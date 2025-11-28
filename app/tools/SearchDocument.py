from typing import List
from config.setting import env


class SearchDocument:
    def __init__(self, qdrant, memory_store):
         self.client = qdrant.client
         self.is_active = qdrant.is_active
         self.memory_store = memory_store
    def search(self, vector: List[float], limit: int = 2) -> List[str]:
            if self.is_active:
                hits = self.client.search(
                    collection_name=env.COLLECTION_NAME, 
                    query_vector=vector, 
                    limit=limit
                )
                return [hit.payload["text"] for hit in hits]
            else:
                if not self.memory_store:
                    return []
                results = []
                first_doc = self.memory_store[0]
                if isinstance(first_doc, dict):
                    results.append(first_doc["text"])
                else:
                    results.append(first_doc)
                    
                return results