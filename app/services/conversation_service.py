import uuid
from sqlalchemy.orm import Session
from openai import OpenAI

from app.core.config import OPENAI_API_KEY, OPENAI_BASE_URL
from app.services.personalization_service import personalize_prompt
from app.services.repair_service import repair_conversation
from app.core.embeddings import generate_embedding
from app.db.vector_db import upsert_vector
from app.services.db_conversation_service import save_message, get_history

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

def generate_response(db: Session, session_id: str, user_id: str, message: str):
    
    message = repair_conversation(message)

    
    history = get_history(db, user_id, session_id)

    
    personalized_input = personalize_prompt(user_id, message)

    messages = history + [{"role": "user", "content": personalized_input}]


    response = client.chat.completions.create(
        model="usf1-mini",
        messages=messages
    )

    reply = response.choices[0].message.content

   
    save_message(db, user_id, session_id, "user", message)
    save_message(db, user_id, session_id, "assistant", reply)

    
    embedding = generate_embedding(message)
    upsert_vector(str(uuid.uuid4()), embedding, {"text": message})

    return reply