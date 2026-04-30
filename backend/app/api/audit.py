from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_session
from app.db.models import AuditLog
from app.dependencies import get_current_user

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("/global")
async def get_global_audit_log(
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    # Fetch last 100 entries
    result = await db.execute(
        select(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .limit(100)
    )
    logs = result.scalars().all()
    
    return [
        {
            "id": str(log.id),
            "action": log.action,
            "user_id": str(log.user_id) if log.user_id else None,
            "case_id": str(log.case_id) if log.case_id else None,
            "timestamp": log.timestamp.isoformat(),
            "summary": f"{log.action.upper()} - {str(log.case_id)[:8] if log.case_id else 'No Case'}"
        }
        for log in logs
    ]
