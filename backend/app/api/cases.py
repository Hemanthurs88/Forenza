from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.db.database import get_session
from app.db.models import Case
from app.dependencies import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/cases", tags=["cases"])

class CaseSchema(BaseModel):
    id: UUID
    case_number: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class CaseCreate(BaseModel):
    case_number: str
    description: str | None = None

@router.post("", response_model=CaseSchema, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_in: CaseCreate,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    # Check if case number already exists
    result = await db.execute(select(Case).where(Case.case_number == case_in.case_number))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Case number already exists")
    
    new_case = Case(
        case_number=case_in.case_number,
        description=case_in.description
    )
    db.add(new_case)
    await db.commit()
    await db.refresh(new_case)
    return new_case

@router.get("", response_model=list[CaseSchema])
async def list_cases(
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    result = await db.execute(select(Case).order_by(Case.created_at.desc()))
    return result.scalars().all()

@router.get("/{case_id}", response_model=CaseSchema)
async def get_case(
    case_id: UUID,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
