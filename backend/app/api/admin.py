import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from openai import OpenAI

from app.core.config import settings
from app.db.database import get_sync_session
from app.db.models import Food
from app.rag import get_collection

router = APIRouter()


@router.post("/ingest")
def ingest_foods():
    data_file = Path(__file__).parent.parent.parent / "data" / "foods.json"
    
    if not data_file.exists():
        raise HTTPException(status_code=404, detail="foods.json not found")
    
    with open(data_file) as f:
        foods_data = json.load(f)
    
    # Insert into Postgres
    with get_sync_session() as session:
        for item in foods_data:
            food = Food(
                id=item["id"],
                name=item["name"],
                description=item["description"],
                cuisine=item.get("cuisine", "indian"),
                meal_type=item.get("meal_type", "main"),
                course=item.get("course", "main"),
                tags=item.get("tags", []),
                allergens=item.get("allergens", []),
                nutrition=item.get("nutrition", {}),
                prep_time_mins=item.get("prep_time_mins", 30),
                spice_level=item.get("spice_level", "medium"),
            )
            session.merge(food)
        session.commit()
    
    # Create embeddings and insert into ChromaDB
    client = OpenAI(api_key=settings.openai_api_key)
    collection = get_collection()
    
    ids = []
    documents = []
    metadatas = []
    
    for item in foods_data:
        doc = f"{item['name']}: {item['description']}. Tags: {', '.join(item.get('tags', []))}. Cuisine: {item.get('cuisine', 'indian')}."
        ids.append(item["id"])
        documents.append(doc)
        metadatas.append({
            "name": item["name"],
            "cuisine": item.get("cuisine", "indian"),
            "meal_type": item.get("meal_type", "main"),
            "spice_level": item.get("spice_level", "medium"),
            "tags": ",".join(item.get("tags", [])),
            "allergens": ",".join(item.get("allergens", [])),
        })
    
    # Upsert to ChromaDB (it will auto-embed with default embedder)
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    
    return {"ingested": len(foods_data), "status": "success"}


@router.get("/stats")
def get_stats():
    collection = get_collection()
    count = collection.count()
    
    with get_sync_session() as session:
        from sqlmodel import select, func
        food_count = session.exec(select(func.count()).select_from(Food)).one()
    
    return {
        "chroma_documents": count,
        "postgres_foods": food_count,
    }
