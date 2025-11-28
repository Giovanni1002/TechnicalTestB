import time
from langgraph.graph import StateGraph, END
from app.schemas.Chat import QuestionRequest, DocumentRequest
from config.qdrant import QdrantConnection
from app.services.EmbeddingService import EmbeddingService
from app.services.ChatService import ChatService
from app.tools.SearchDocument import SearchDocument
from app.tools.UpsertDocument import SaveDocument

class RagController:
    def __init__(self):
        self.qdrant = QdrantConnection()
        self.embedder = EmbeddingService()
        self.shared_memory = []
        self.search_tool = SearchDocument(self.qdrant, self.shared_memory)
        self.save_tool = SaveDocument(self.qdrant, self.shared_memory)

        self.chat_service = ChatService(self.search_tool, self.embedder)
        self.chain = self.built_graph()

    def built_graph(self):
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self.chat_service.retrieve)
        workflow.add_node("answer", self.chat_service.generate_answer)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        chain = workflow.compile()
        return chain

    def handle_ask(self, req: QuestionRequest):
        start = time.time()
        result = self.chain.invoke({"question": req.question})
        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3)
        }
    
    def handle_add(self, req: DocumentRequest):
        vector = self.embedder.generate(req.text)
        doc_id = self.save_tool.save(req.text, vector)
        
        return {"id": doc_id, "status": "added"}
    
    def get_status(self):
        count = len(self.save_tool.memory_store)
        return {
            "qdrant_active": self.qdrant.is_active,
            "in_memory_docs_count": count,
            "graph_ready": self.chain is not None
        }
    
rag_controller = RagController()
