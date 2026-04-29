from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class FaceParams(BaseModel):
    """Face parameter set with [0,1] normalized values."""
    jaw_width: float = Field(default=0.5, ge=0.0, le=1.0)
    chin_length: float = Field(default=0.5, ge=0.0, le=1.0)
    face_length: float = Field(default=0.5, ge=0.0, le=1.0)
    eye_size: float = Field(default=0.5, ge=0.0, le=1.0)
    eye_spacing: float = Field(default=0.5, ge=0.0, le=1.0)
    eye_angle: float = Field(default=0.5, ge=0.0, le=1.0)
    nose_length: float = Field(default=0.5, ge=0.0, le=1.0)
    nose_width: float = Field(default=0.5, ge=0.0, le=1.0)
    lip_thickness: float = Field(default=0.5, ge=0.0, le=1.0)
    mouth_width: float = Field(default=0.5, ge=0.0, le=1.0)

    @field_validator('*')
    def validate_range(cls, v):
        if not isinstance(v, (int, float)) or v < 0.0 or v > 1.0:
            raise ValueError('FaceParams must be in range [0, 1]')
        return float(v)


class SessionStateRead(BaseModel):
    """Session state for API responses."""
    id: str
    user_id: str
    parameters: dict = Field(default_factory=dict)
    preset: str | None = None
    z_current: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SessionStateCreate(BaseModel):
    """Session creation request."""
    parameters: FaceParams = Field(default_factory=FaceParams)
    preset: str | None = None
