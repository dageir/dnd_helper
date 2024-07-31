from typing import Generator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.models import engine

new_seseion = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> Generator:
    try:
        session: AsyncSession = new_seseion()
        yield session
    finally:
        await session.close()