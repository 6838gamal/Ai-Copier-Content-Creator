from app.services.embedding import get_embedding
from app.db.vector_store import add_vector, save
from app.utils.file_manager import read_json

def ingest_file(file_path="app/data/content.json"):
    data = read_json(file_path)

    for item in data:
        text = item["text"]
        vector = get_embedding(text)
        add_vector(vector, text)

    save()

if __name__ == "__main__":
    ingest_file()
