from app.services.embedding import get_embedding
from app.db.vector_store import add_vector, save

def ingest_content(texts):
    for text in texts:
        vector = get_embedding(text)
        add_vector(vector, text)
    save()
