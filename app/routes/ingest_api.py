from fastapi import APIRouter
from app.services.embedding import get_embedding
from app.db.vector_store import add_vector, save

router = APIRouter()

@router.post("/ingest")
def ingest(data: dict):
    texts = data.get("texts", [])

    for text in texts:
        vector = get_embedding(text)
        add_vector(vector, text)

    save()

    return {"status": "ingested", "count": len(texts)}

