from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db

router = APIRouter(prefix="/nlp", tags=["nlp"])


class NLPRequest(BaseModel):
    """NLP parsing request."""
    text: str


@router.post("/parse")
async def parse_nlp(
    req: NLPRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Parse natural language input into face parameters.
    
    Requires JWT authentication.
    """
    user_id = current_user.get("sub")
    # TODO: Call external NLP service (OpenAI) to parse text into FaceParams
    return {
        "user_id": user_id,
        "input": req.text,
        "parsed": {},  # Placeholder
    }
