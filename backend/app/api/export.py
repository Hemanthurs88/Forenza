from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
import httpx
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

@router.get("/download-image")
async def download_image_proxy(
    url: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    """Proxy image download to bypass CORS blocks in browser."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Get filename from URL or default
            filename = url.split("/")[-1].split("?")[0] or "forensic-sketch.png"
            if not filename.endswith((".png", ".jpg", ".jpeg")):
                filename += ".png"

            return StreamingResponse(
                iter([response.content]),
                media_type=response.headers.get("content-type", "image/png"),
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch image: {str(e)}"
        )
