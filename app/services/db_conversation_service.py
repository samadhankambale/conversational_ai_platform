from sqlalchemy.orm import Session
from app.db.models import ConversationMessage
from app.core.exceptions import BadRequestException


def save_message(db: Session, user_id: str, session_id: str, role: str, content: str):
    try:
        msg = ConversationMessage(
            user_id=user_id,
            session_id=session_id,
            role=role,
            content=content
        )
        db.add(msg)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"DB Error: {e}")
        raise BadRequestException(detail="Failed to save message")
    
    

def get_history(db: Session, user_id: str, session_id: str):
    messages = db.query(ConversationMessage)\
        .filter(
            ConversationMessage.user_id == user_id,      # ✅ FILTER USER
            ConversationMessage.session_id == session_id
        )\
        .order_by(ConversationMessage.id)\
        .all()

    return [{"role": m.role, "content": m.content} for m in messages]



def delete_session(db: Session, user_id: str, session_id: str):
    deleted = db.query(ConversationMessage)\
        .filter(
            ConversationMessage.user_id == user_id,
            ConversationMessage.session_id == session_id
        )\
        .delete()

    db.commit()
    return deleted > 0