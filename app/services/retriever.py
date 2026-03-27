from app.services.embedding import get_embedding
from app.db.vector_store import search

def retrieve_relevant_texts(query: str):
    vector = get_embedding(query)
    return search(vector)
