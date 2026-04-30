import asyncio
import os
import sys
from sqlalchemy import text

sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.db.database import engine

async def m():
    async with engine.begin() as conn:
        await conn.execute(text('ALTER TABLE sessions ADD COLUMN IF NOT EXISTS description TEXT'))
        print("Column 'description' added to 'sessions' table.")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(m())
