from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from app.rag import search_foods
from app.llm import generate_streaming_response

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    preferences: Optional[dict] = None


@router.post("/chat")
async def chat(request: ChatRequest):
    prefs = request.preferences or {}
    
    # Search for relevant foods with preference filtering
    foods = search_foods(
        query=request.message,
        allergies=prefs.get("allergies", []),
        dietary_type=prefs.get("dietary_type"),
        cuisines=prefs.get("preferred_cuisines", []),
        spice_level=prefs.get("spice_level"),
        n_results=6,
    )
    
    # Build context from retrieved foods
    context = ""
    if foods:
        context_parts = []
        for f in foods:
            meta = f.get("metadata", {})
            context_parts.append(
                f"- {meta.get('name', 'Unknown')}: {f.get('content', '')}"
            )
        context = "\n".join(context_parts)
    
    messages = [{"role": "user", "content": request.message}]
    
    async def event_generator():
        async for chunk in generate_streaming_response(messages, context):
            import json
            yield {"event": "message", "data": json.dumps({"content": chunk})}
        yield {"event": "done", "data": ""}
    
    return EventSourceResponse(event_generator())
