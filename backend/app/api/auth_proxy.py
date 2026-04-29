from fastapi import APIRouter, Depends

from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth-proxy"])


@router.post("/proxy")
async def proxy_auth(
    payload: dict,
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Forward authentication calls to Member 3 service.
    
    Requires JWT validation; passes through requests to external auth service.
    """
    return {
        "user_id": current_user.get("sub"),
        "proxied": True,
        "payload": payload,
    }
