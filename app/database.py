from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

SQLALCHEMY_DATABASE_URL = (f"{settings.database_type}://{settings.database_username}:{settings.database_password}@"
                           f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
