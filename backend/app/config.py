import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


_HERE = Path(__file__).resolve()
_ENV_FILES = [
    _HERE.parent / ".env",            # backend/app/.env
    _HERE.parents[1] / ".env",        # backend/.env
    _HERE.parents[2] / ".env",        # project root .env
]

for env_file in _ENV_FILES:
    if env_file.exists():
        load_dotenv(env_file, override=False)


@lru_cache(maxsize=1)
def get_settings() -> dict[str, str]:
    return {
        "DATABASE_URL": os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/forenza"),
        "JWT_SECRET": os.getenv("JWT_SECRET", "change-me"),
        "JWT_ALGORITHM": os.getenv("JWT_ALGORITHM", "HS256"),
        "ML_SERVICE_URL": os.getenv("ML_SERVICE_URL", "http://localhost:8001"),
        "R2_ACCOUNT_ID": os.getenv("R2_ACCOUNT_ID", ""),
        "R2_ACCESS_KEY_ID": os.getenv("R2_ACCESS_KEY_ID", ""),
        "R2_SECRET_ACCESS_KEY": os.getenv("R2_SECRET_ACCESS_KEY", ""),
        "R2_BUCKET": os.getenv("R2_BUCKET", "forensic-faces"),
        "AUTH_SERVICE_URL": os.getenv("AUTH_SERVICE_URL", "http://localhost:8002"),
    }
