from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False} if settings.SQLALCHEMY_DATABASE_URI.startswith('sqlite') else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase): pass

def init_db():
    from . import models  # noqa
    Base.metadata.create_all(bind=engine)
