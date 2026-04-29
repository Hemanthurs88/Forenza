from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SessionRecord
from app.schemas.session import SessionStateCreate


async def create_session(
    db: AsyncSession,
    user_id: str,
    preset: str | None = None,
    parameters: dict | None = None,
) -> SessionRecord:
    """Create a new session for a user."""
    record = SessionRecord(
        user_id=user_id,
        parameters=parameters or {},
        preset=preset,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_session(db: AsyncSession, session_id: str) -> SessionRecord | None:
    """Retrieve a session by ID."""
    result = await db.execute(select(SessionRecord).where(SessionRecord.id == session_id))
    return result.scalar_one_or_none()


async def list_sessions(db: AsyncSession, user_id: str) -> list[SessionRecord]:
    """List all sessions for a user, ordered by recency."""
    result = await db.execute(
        select(SessionRecord)
        .where(SessionRecord.user_id == user_id)
        .order_by(SessionRecord.updated_at.desc())
    )
    return list(result.scalars().all())


async def save_session(db: AsyncSession, session: SessionRecord) -> SessionRecord:
    """Save session changes (merge/update)."""
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session
