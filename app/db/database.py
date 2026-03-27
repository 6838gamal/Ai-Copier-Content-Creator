from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
import os

# مثال لقاعدة SQLite محلية، يمكن تغييرها لاحقًا إلى MySQL/Postgres
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./digital_store.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# إنشاء الجداول لو لم تكن موجودة
def init_db():
    Base.metadata.create_all(bind=engine)
