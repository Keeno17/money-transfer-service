from fastapi import FastAPI
import app.db.base
from app.api.router import api_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="Money Transfer Service API", version="1.0.0")

app.include_router(api_router)
