import httpx

from app.config import get_settings

settings = get_settings()
ML_BASE = settings["ML_SERVICE_URL"]


async def ml_post(endpoint: str, body: dict) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(f"{ML_BASE}{endpoint}", json=body)
        response.raise_for_status()
        return response.json()


call_ml_service = ml_post
