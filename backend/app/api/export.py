from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session_manager import get_session
from app.dependencies import get_current_user, get_db

router = APIRouter(prefix="/sessions", tags=["export"])


@router.get("/{session_id}/export")
async def export_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Export session data with full audit trail.
    
    Returns parameters, z_vector, and complete history of changes.
    """
    session = await get_session(db, session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    user_id = current_user.get("sub")
    if str(session.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    # Fetch all audit logs for this session
    from app.db.models import AuditLog
    from sqlalchemy import select
    from app.schemas.audit import AuditLogRead

    result = await db.execute(
        select(AuditLog)
        .where(AuditLog.session_id == session.id)
        .order_by(AuditLog.timestamp.asc())
    )
    logs = result.scalars().all()

    return {
        "session_id": session_id,
        "case_id": str(session.case_id) if session.case_id else None,
        "parameters": session.parameters,
        "z_current": session.z_current,
        "preset": session.preset,
        "created_at": session.created_at.isoformat(),
        "updated_at": session.updated_at.isoformat(),
        "history": [AuditLogRead.from_orm(log).model_dump() for log in logs],
    }
