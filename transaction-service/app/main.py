from fastapi import FastAPI
from app.db.session import engine, Base
import app.db.base
from app.api.router import api_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="Money Transfer Service API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(api_router)
