import faiss
import numpy as np
import pickle
import os

INDEX_FILE = "faiss.index"
TEXTS_FILE = "texts.pkl"

dimension = 384
index = faiss.IndexFlatL2(dimension)
stored_texts = []

def save():
    faiss.write_index(index, INDEX_FILE)
    with open(TEXTS_FILE, "wb") as f:
        pickle.dump(stored_texts, f)

def load():
    global index, stored_texts
    if os.path.exists(INDEX_FILE):
        index = faiss.read_index(INDEX_FILE)
    if os.path.exists(TEXTS_FILE):
        with open(TEXTS_FILE, "rb") as f:
            stored_texts = pickle.load(f)

def add_vector(vector, text):
    index.add(np.array([vector]).astype("float32"))
    stored_texts.append(text)

def search(vector, k=5):
    D, I = index.search(np.array([vector]).astype("float32"), k)
    return [stored_texts[i] for i in I[0] if i < len(stored_texts)]
