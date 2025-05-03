from sqlalchemy.orm import sessionmaker

from app.db.student_session import sync_engine
from app.models.student_model import Base


def create_tables():
    sync_engine.echo = False
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True


def delete_tables():
    sync_engine.echo = False
    Base.metadata.drop_all(sync_engine)
    sync_engine.echo = True