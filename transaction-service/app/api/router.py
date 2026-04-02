from fastapi import APIRouter
from app.api.routes.transfers import router as transfer_router

api_router = APIRouter()

api_router.include_router(transfer_router, prefix="/api", tags=["transfers"])
