from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.db.database import get_sync_session
from app.db.models import User, UserPreferences

router = APIRouter()


class PreferencesUpdate(BaseModel):
    dietary_type: Optional[str] = None
    spice_level: Optional[str] = None
    allergies: Optional[list[str]] = None
    dislikes: Optional[list[str]] = None
    health_goals: Optional[list[str]] = None
    preferred_cuisines: Optional[list[str]] = None


@router.get("/preferences/{user_id}")
def get_preferences(user_id: str):
    with get_sync_session() as session:
        prefs = session.exec(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        ).first()
        
        if not prefs:
            return {
                "user_id": user_id,
                "dietary_type": "vegetarian",
                "spice_level": "medium",
                "allergies": [],
                "dislikes": [],
                "health_goals": [],
                "preferred_cuisines": ["south_indian", "north_indian"],
            }
        
        return prefs


@router.put("/preferences/{user_id}")
def update_preferences(user_id: str, update: PreferencesUpdate):
    with get_sync_session() as session:
        # Ensure user exists
        user = session.get(User, user_id)
        if not user:
            user = User(id=user_id)
            session.add(user)
            session.commit()
        
        # Get or create preferences
        prefs = session.exec(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        ).first()
        
        if not prefs:
            prefs = UserPreferences(user_id=user_id)
            session.add(prefs)
        
        # Update fields
        for field, value in update.model_dump(exclude_unset=True).items():
            setattr(prefs, field, value)
        
        session.commit()
        session.refresh(prefs)
        
        return prefs
