from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# During MVP development, we can use a local SQLite DB if PostgreSQL isn't running yet,
# but the schema will be fully PostgreSQL compatible (using models.py).
# For now, let's setup the connection string.
# To switch to postgres, set DATABASE_URL=postgresql://user:password@localhost/nexus
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nexus_mvp.db")

# If using SQLite for fast local iteration, we need connect_args
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
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
