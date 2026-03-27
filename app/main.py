import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.generate import router as generate_router
from app.routes.status import router as status_router
from app.routes.ingest_api import router as ingest_router
from app.db.vector_store import load as load_faiss
from app.db.database import init_db

# ---------------------------
# إعداد FastAPI
# ---------------------------
app = FastAPI(
    title="Gamal Gemini AI - Render Ready",
    description="API لتوليد المحتوى باستخدام Gemini + FAISS",
    version="1.0.0"
)

# السماح بالوصول من أي مكان (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# تحميل قاعدة FAISS و DB
# ---------------------------
init_db()       # إنشاء الجداول لو لم تكن موجودة
load_faiss()    # تحميل FAISS index والنصوص المخزنة

# ---------------------------
# تسجيل الروترات
# ---------------------------
app.include_router(generate_router, prefix="/api")
app.include_router(status_router, prefix="/api")
app.include_router(ingest_router, prefix="/api")

# ---------------------------
# Main Run (للـ Render)
# ---------------------------
if __name__ == "__main__":
    import uvicorn

    # Render يمرر المنفذ عبر متغير PORT
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
