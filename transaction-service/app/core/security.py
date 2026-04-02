import secrets
from fastapi import Header, HTTPException, status
from app.core.config import SERVICE_API_KEY


def verify_service_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    if not SERVICE_API_KEY:
        raise RuntimeError("Service API key is not configured")

    if not secrets.compare_digest(x_api_key, SERVICE_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return x_api_key
