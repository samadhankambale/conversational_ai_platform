from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.db.vector_db import init_collection
from app.db.database import Base, engine
from app.core.middleware import ExceptionHandlerMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    init_collection()
    yield

app = FastAPI(title="Conversational_AI_Platform")

app.include_router(auth_router)
app.include_router(router)
app.add_middleware(ExceptionHandlerMiddleware)
