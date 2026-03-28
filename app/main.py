import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
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
# Lifespan
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
    version="1.0.0",
    lifespan=lifespan
)

# ---------------------------
# Paths & Templates / Static
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # app/
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Templates
if os.path.isdir(TEMPLATES_DIR):
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
    logger.info(f"✅ Templates loaded from {TEMPLATES_DIR}")
else:
    templates = None
    logger.warning(f"⚠️ Templates folder not found at {TEMPLATES_DIR}")

# Static
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    logger.info(f"✅ Static files mounted at {STATIC_DIR}")
else:
    logger.warning(f"⚠️ Static folder not found at {STATIC_DIR}")

# ---------------------------
# CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Routes (HTML Pages)
# ---------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    if not templates:
        return HTMLResponse("<h1>Templates folder not found!</h1>", status_code=500)
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/generate", response_class=HTMLResponse)
def generate_page(request: Request):
    if not templates:
        return HTMLResponse("<h1>Templates folder not found!</h1>", status_code=500)
    return templates.TemplateResponse(
        "generate.html",
        {"request": request}
    )

@app.get("/status-page", response_class=HTMLResponse)
def status_page(request: Request):
    if not templates:
        return HTMLResponse("<h1>Templates folder not found!</h1>", status_code=500)
    return templates.TemplateResponse(
        "status.html",
        {"request": request}
    )

# ---------------------------
# API Routers
# ---------------------------
app.include_router(generate_router, prefix="/api", tags=["AI Generate"])
app.include_router(status_router, prefix="/api", tags=["System Status"])
app.include_router(ingest_router, prefix="/api", tags=["Data Ingestion"])

# ---------------------------
# Health Check
# ---------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Gamal AI",
        "version": "1.0.0"
    }

# ---------------------------
# Global Error Handler
# ---------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc)
        }
    )
