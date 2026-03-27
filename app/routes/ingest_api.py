from fastapi import APIRouter
from app.scripts.ingest import ingest_content

router = APIRouter()

@router.post("/ingest")
def ingest(data: dict):
    ingest_content(data.get("texts", []))
    return {"status": "ingested"}
