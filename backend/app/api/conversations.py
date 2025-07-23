from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter
from sqlmodel import select
from datetime import datetime

from app.db.database import get_sync_session
from app.db.models import User, ChatSession, ChatMessage

router = APIRouter()


class NewConversation(BaseModel):
    user_id: str
    title: Optional[str] = "New Chat"


class NewMessage(BaseModel):
    role: str
    content: str


@router.get("/conversations/{user_id}")
def list_conversations(user_id: str):
    with get_sync_session() as session:
        sessions = session.exec(
            select(ChatSession)
            .where(ChatSession.user_id == user_id)
            .order_by(ChatSession.updated_at.desc())
        ).all()
        return sessions


@router.post("/conversations")
def create_conversation(data: NewConversation):
    with get_sync_session() as session:
        user = session.get(User, data.user_id)
        if not user:
            user = User(id=data.user_id)
            session.add(user)
            session.commit()
        
        chat = ChatSession(user_id=data.user_id, title=data.title)
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat


@router.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id: str):
    with get_sync_session() as session:
        messages = session.exec(
            select(ChatMessage)
            .where(ChatMessage.session_id == conversation_id)
            .order_by(ChatMessage.created_at.asc())
        ).all()
        return messages


@router.post("/conversations/{conversation_id}/messages")
def add_message(conversation_id: str, message: NewMessage):
    with get_sync_session() as session:
        msg = ChatMessage(
            session_id=conversation_id,
            role=message.role,
            content=message.content,
        )
        session.add(msg)
        
        # Update conversation timestamp
        conv = session.get(ChatSession, conversation_id)
        if conv:
            conv.updated_at = datetime.utcnow()
        
        session.commit()
        session.refresh(msg)
        return msg
