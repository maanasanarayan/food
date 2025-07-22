from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from app.core.config import settings

sync_engine = create_engine(
    settings.database_url.replace("postgresql://", "postgresql+psycopg2://"),
    echo=False,
)

async_engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=False,
)

async_session_factory = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    from app.db.models import User, UserPreferences, Food, ChatSession, ChatMessage
    SQLModel.metadata.create_all(sync_engine)


def get_sync_session() -> Session:
    return Session(sync_engine)


@asynccontextmanager
async def get_async_session():
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_session():
    async with async_session_factory() as session:
        yield session
