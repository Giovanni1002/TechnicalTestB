from fastapi import APIRouter, HTTPException
from app.schemas.Chat import QuestionRequest, DocumentRequest
from app.controllers.RagController import rag_controller # Assuming file is in controllers folder

router = APIRouter()

@router.post("/ask")
def ask_question(req: QuestionRequest):
    try:
        return rag_controller.handle_ask(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add")
def add_document(req: DocumentRequest):
    try:
        return rag_controller.handle_add(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
def status():
    return rag_controller.get_status()