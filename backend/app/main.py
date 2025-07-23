from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, preferences, conversations, admin
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Food Recommendation API",
    description="AI-powered Indian vegetarian food recommendations",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(preferences.router, prefix="/api", tags=["preferences"])
app.include_router(conversations.router, prefix="/api", tags=["conversations"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "food-api"}


@app.get("/")
async def root():
    return {
        "name": "Food Recommendation API",
        "version": "1.0.0",
        "docs": "/docs",
    }
