import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.generate import router as generate_router
from app.routes.status import router as status_router
from app.routes.ingest_api import router as ingest_router
from app.db.vector_store import load as load_faiss
from app.db.database import init_db

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# إعداد FastAPI
# ---------------------------
app = FastAPI(
    title="Gamal Gemini AI - Render Ready",
    description="API لتوليد المحتوى باستخدام Gemini + FAISS",
    version="1.0.0"
)

# ---------------------------
# CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # عدّلها لاحقًا
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Startup Event
# ---------------------------
@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting app...")
    init_db()
    load_faiss()
    logger.info("✅ DB & FAISS Loaded")

# ---------------------------
# Routers
# ---------------------------
app.include_router(generate_router, prefix="/api")
app.include_router(status_router, prefix="/api")
app.include_router(ingest_router, prefix="/api")
