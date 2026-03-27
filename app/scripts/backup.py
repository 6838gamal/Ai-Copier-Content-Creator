import shutil
from app.db.vector_store import INDEX_FILE, TEXTS_FILE

def backup(destination_folder="backup"):
    shutil.copy(INDEX_FILE, f"{destination_folder}/faiss.index")
    shutil.copy(TEXTS_FILE, f"{destination_folder}/texts.pkl")
