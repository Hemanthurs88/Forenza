from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AuditLog, SessionRecord
from app.dependencies import get_current_user, get_db
from app.core.similarity import string_to_hash, similarity_score
from uuid import UUID

router = APIRouter(prefix="/match", tags=["matching"])

@router.get("/{session_id}")
async def match_face(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[dict]:
    """
    Search for images similar to the current session's latest image.
    Uses pHash (simple math technique) to compare against all other images in the DB.
    """
    # 1. Get current session's latest phash from AuditLog
    result = await db.execute(
        select(AuditLog)
        .where(AuditLog.session_id == UUID(session_id))
        .where(AuditLog.phash.is_not(None))
        .order_by(AuditLog.timestamp.desc())
        .limit(1)
    )
    current_log = result.scalar_one_or_none()
    
    if not current_log or not current_log.phash:
        # Fallback: maybe no image generated yet
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No generated image found for this session to match."
        )
        
    current_hash = string_to_hash(current_log.phash)
    
    # 2. Get all other images with a phash
    # We exclude the current session's images to find matches in OTHER cases/sessions
    result = await db.execute(
        select(AuditLog)
        .where(AuditLog.session_id != UUID(session_id))
        .where(AuditLog.phash.is_not(None))
    )
    all_logs = result.scalars().all()
    
    # 3. Calculate similarity scores
    matches = []
    for log in all_logs:
        db_hash = string_to_hash(log.phash)
        score = similarity_score(current_hash, db_hash)
        
        # Only include high-confidence matches (e.g. > 70%)
        if score >= 70.0:
            matches.append({
                "image_url": log.image_url,
                "score": round(score, 2),
                "action": log.action,
                "timestamp": log.timestamp.isoformat(),
                "session_id": str(log.session_id),
                "case_id": str(log.case_id) if log.case_id else None
            })
            
    # Sort by highest score
    matches.sort(key=lambda x: x["score"], reverse=True)
    
    # Limit to top 10
    return matches[:10]
