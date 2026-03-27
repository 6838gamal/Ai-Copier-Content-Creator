import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
# Lifespan (بديل startup)
# ---------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Gamal AI App...")

    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database Error: {e}")

    try:
        load_faiss()
        logger.info("✅ FAISS loaded")
    except Exception as e:
        logger.error(f"❌ FAISS Error: {e}")

    yield

    logger.info("🛑 Shutting down Gamal AI App...")

# ---------------------------
# App Init
# ---------------------------
app = FastAPI(
    title="Gamal Gemini AI",
    description="AI Content Generator + RAG System",
    version="1.0.0",
    lifespan=lifespan
)

# ---------------------------
# Static & Templates
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

static_path = os.path.join(os.path.dirname(BASE_DIR), "static")
templates_path = os.path.join(os.path.dirname(BASE_DIR), "templates")

if os.path.isdir(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    logger.info("✅ Static files loaded")

templates = Jinja2Templates(directory=templates_path)

# ---------------------------
# CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # عدلها لاحقًا
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Routes (HTML Pages)
# ---------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/generate", response_class=HTMLResponse)
def generate_page(request: Request):
    return templates.TemplateResponse("generate.html", {"request": request})


@app.get("/status-page", response_class=HTMLResponse)
def status_page(request: Request):
    return templates.TemplateResponse("status.html", {"request": request})


# ---------------------------
# API Routers
# ---------------------------
app.include_router(generate_router, prefix="/api", tags=["AI Generate"])
app.include_router(status_router, prefix="/api", tags=["System Status"])
app.include_router(ingest_router, prefix="/api", tags=["Data Ingestion"])


# ---------------------------
# Health Check (مهم لـ Render)
# ---------------------------
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Gamal AI",
        "version": "1.0.0"
    }


# ---------------------------
# Global Error Handler (اختياري)
# ---------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Unhandled error: {exc}")
    return {
        "error": "Internal Server Error",
        "message": str(exc)
    }
