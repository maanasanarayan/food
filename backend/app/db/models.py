from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    preferences: Optional["UserPreferences"] = Relationship(back_populates="user")
    sessions: list["ChatSession"] = Relationship(back_populates="user")


class UserPreferences(SQLModel, table=True):
    __tablename__ = "user_preferences"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", unique=True)
    dietary_type: str = Field(default="vegetarian")
    spice_level: str = Field(default="medium")
    allergies: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    dislikes: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    health_goals: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    preferred_cuisines: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: Optional[User] = Relationship(back_populates="preferences")


class Food(SQLModel, table=True):
    __tablename__ = "foods"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(index=True)
    description: str
    cuisine: str = Field(default="indian")
    meal_type: str = Field(default="main")
    course: str = Field(default="main")
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    allergens: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    nutrition: dict = Field(default_factory=dict, sa_column=Column(JSON))
    prep_time_mins: int = Field(default=30)
    spice_level: str = Field(default="medium")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_sessions"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    title: str = Field(default="New Chat")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: Optional[User] = Relationship(back_populates="sessions")
    messages: list["ChatMessage"] = Relationship(back_populates="session")


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    session_id: str = Field(foreign_key="chat_sessions.id")
    role: str
    content: str
    recommendations: list[dict] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    session: Optional[ChatSession] = Relationship(back_populates="messages")
