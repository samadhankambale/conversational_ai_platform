from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse
from app.services.conversation_service import generate_response
from app.services.analytics_service import analyze_conversation
from app.services.db_conversation_service import get_history
from app.db.database import SessionLocal
from app.api.deps import get_current_user
from app.core.exceptions import BadRequestException
from fastapi import HTTPException
from app.services.db_conversation_service import delete_session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.post("/chat", response_model=ChatResponse, tags=["Conversation"])
def chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        reply = generate_response(db, req.session_id, user, req.message)
        return ChatResponse(response=reply)
    except Exception as e:
        print(f"Chat error: {e}")
        raise BadRequestException(detail="Failed to generate response")


@router.get("/conversation/{session_id}", tags=["Conversation"])
def get_conversation(
    session_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    history = get_history(db, user, session_id)

    if not history:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return history


@router.delete("/conversation/{session_id}", tags=["Danger Zone"])
def delete_conversation(
    session_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    success = delete_session(db, user, session_id)

    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {"message": "Conversation deleted successfully"}


@router.get("/analytics/{session_id}", tags=["Conversation"])
def analytics(
    session_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    history = get_history(db, user, session_id)

    if not history:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return analyze_conversation(history)