from .db import engine, Base, async_session
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session