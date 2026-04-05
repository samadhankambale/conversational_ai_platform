# FastAPI Conversational AI Platform

## Features

*  JWT-based Authentication (Register, Login, Logout with blacklist)
*  Multi-user conversation isolation
*  Session-based chat system
*  Context-aware responses using RAG
*  Vector search with Qdrant
*  Persistent storage using SQLite
*  Conversation analytics
*  Delete conversation (bulk session delete)
*  Sentence Transformer embeddings
*  Centralized error handling



## Architecture

FastAPI
├── Auth (JWT + SQLite)
├── Conversation (SQLite with user isolation)
├── RAG (Qdrant + Sentence Transformers)
├── Services Layer (modular)
└── Error Handling (custom exceptions + middleware)



## Project Structure

app/
├── api/
│   ├── routes.py
│   ├── auth_routes.py
│   └── deps.py
├── core/
│   ├── config.py
│   ├── security.py
│   ├── embeddings.py
│   ├── exceptions.py
│   ├── middleware.py
│   └── token_blacklist.py
├── db/
│   ├── database.py
│   ├── models.py
│   └── vector_db.py
├── services/
│   ├── conversation_service.py
│   ├── db_conversation_service.py
│   ├── rag_service.py
│   ├── personalization_service.py
│   ├── analytics_service.py
│   └── repair_service.py
├── schemas/
│   ├── request.py
│   ├── response.py
│   └── auth.py
└── main.py


## Setup Instructions

1. Clone Repository
   git clone <repo-url>
   cd conversational_ai

2. Create Virtual Environment
   python -m venv venv
   venv\Scripts\activate

3. Install Dependencies
   pip install -r requirements.txt

4. Setup Environment Variables (`.env`)

OPENAI_API_KEY=your_api_key
QDRANT_URL=http://localhost:6333


5. Start Qdrant (Vector Database)


docker run -p 6333:6333 qdrant/qdrant


6. Run FastAPI Server

uvicorn app.main:app --reload




##  Authentication APIs

### Register

POST /auth/register

### Login

POST /auth/login

Response:
{
"access_token": "JWT_TOKEN",
"token_type": "bearer"
}

### Logout

POST /auth/logout
Header: Authorization: Bearer <token>



##  Conversation APIs

### Chat

POST /chat
Header: Authorization: Bearer <token>

Request:
{
"session_id": "1",
"message": "Hello"
}



### Get Conversation

GET /conversation/{session_id}
Header: Authorization: Bearer <token>

* Returns only the logged-in user's conversation
* Returns **404 if session does not exist**



### Delete Conversation

DELETE /conversation/{session_id}
Header: Authorization: Bearer <token>

* Deletes all messages in the session (bulk delete)
* User can only delete their own sessions
* Returns **404 if session not found**
* Grouped under **Danger Zone** in API docs



### Analytics

GET /analytics/{session_id}
Header: Authorization: Bearer <token>

* Returns conversation metrics
* Returns **404 if session not found**



##  Conversation Management

* Conversations stored in **SQLite**
* Schema includes:

  * `user_id`
  * `session_id`
  * `role`
  * `content`
* Ensures:

  * User isolation (JWT-based)
  * Persistent conversation state
  * Secure multi-user access


##  RAG Implementation

### Flow

1. User sends message
2. Message → embedding (Sentence Transformers)
3. Query Qdrant vector DB
4. Retrieve similar context
5. Rerank results
6. Combine:

   * conversation history
   * retrieved context
   * user message
7. Generate response using LLM



### Components

* Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
* Vector DB: Qdrant
* LLM: OpenAI-compatible API
* Storage: SQLite



##  Analytics

### Metrics

* Conversation Length
* Engagement Score

Formula:
engagement_score = min(len(history) / 10, 1.0)


##  Error Handling

* Custom exception classes
* Global middleware for unexpected errors
* Database rollback on failure
* Graceful handling of:

  * invalid input
  * missing sessions (404)
  * RAG failures


## Security

* JWT-based authentication
* Token blacklist for logout
* User-scoped data access
* No exposure of user_id in APIs



##  Performance Considerations

### Strengths

* Fast vector search (Qdrant)
* Lightweight SQLite storage
* Local embeddings (low latency)
* Bulk delete for conversations

### Limitations

* Synchronous DB operations
* In-memory token blacklist (resets on restart)
* No pagination for long conversations



## Future Improvements

* Async database support
* Redis for token blacklist
* Session listing endpoint
* Pagination for chat history
* Advanced personalization (user preferences)



## Conclusion

This project delivers a **complete Conversational AI backend** with:

* Secure authentication
* Multi-user conversation isolation
* Context-aware RAG pipeline
* Efficient session management
* Analytics and error handling



