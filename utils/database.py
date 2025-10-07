from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from utils.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class for all SQLAlchemy models to inherit from
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
