from fastapi import FastAPI
from app.routes.generate import router as generate_router
from app.routes.status import router as status_router
from app.db.vector_store import load

app = FastAPI(title="Gamal Gemini AI")

load()  # تحميل قاعدة FAISS

app.include_router(generate_router)
app.include_router(status_router)
