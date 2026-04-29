from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.database import get_session

security = HTTPBearer(auto_error=False)
settings = get_settings()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    """Extract and validate JWT token. 'sub' claim = user_id (UUID string)."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token"
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings["JWT_SECRET"],
            algorithms=[settings["JWT_ALGORITHM"]],
        )
        if "sub" not in payload:
            raise JWTError("Missing 'sub' claim")
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        ) from exc
