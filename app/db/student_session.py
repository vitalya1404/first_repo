from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

sync_engine = create_engine(settings.database_url, echo=True)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


# Залежність для FastAPI
def get_db() -> Session:
    db = session_factory()
    try:
        yield db
    finally:
        db.close()