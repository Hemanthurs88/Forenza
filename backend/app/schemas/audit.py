from datetime import datetime

from pydantic import BaseModel, Field


class AuditLogEntry(BaseModel):
    """Audit log entry for writing to database."""
    session_id: str
    user_id: str
    action: str
    params_before: dict = Field(default_factory=dict)
    params_after: dict = Field(default_factory=dict)
    image_url: str | None = None


class AuditLogRead(BaseModel):
    """Audit log entry for API responses."""
    id: str
    session_id: str
    user_id: str
    action: str
    params_before: dict
    params_after: dict
    image_url: str | None = None
    timestamp: datetime

    class Config:
        from_attributes = True
