from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, future=True)
Base = declarative_base()

SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def SessionLocal() -> Session:
    return SessionFactory()


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
