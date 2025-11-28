from typing import Dict, Any


class ChatService:
    def __init__(self, tools, embedder):
        self.tool = tools
        self.embedder = embedder

    def retrieve(self, state: dict) -> Dict[str, Any]:
        query = state["question"]
        emb = self.embedder.generate(query)
        results = self.tool.search(emb)
        return {"context": results}

    def generate_answer(self, state: dict) -> Dict[str, Any]:
        ctx = state.get("context", [])
        if ctx:
            ans = f"I found this: '{ctx[0][:100]}...'"
        else:
            ans = "Sorry, I don't know."
        return {"answer": ans}