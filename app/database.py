from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# The engine is the starting point for SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Each instance of the SessionLocal class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for our models to inherit from and be mapped by the ORM
Base = declarative_base()


def get_db():
    """
    Dependency Injection: Ensures that the session opens at the start of the request
    and closes obligatorily at the end (finally).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()