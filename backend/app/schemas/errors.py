from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response format per system spec."""
    error: str
    code: str
    detail: str | None = None
