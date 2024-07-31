import uuid

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ARRAY, JSON, UUID, Boolean

from config import DB_NAME, DB_HOST, DB_PORT, DB_LOGIN, DB_PASSWORD



engine = create_async_engine(f'postgresql+asyncpg://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}', future=True, echo=True)


class Model(DeclarativeBase):
    pass

class GameCharactersOrm(Model):
    __tablename__ = 'characters'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    race= Column(String, nullable=False)
    class_= Column(String, nullable=False)
    description = Column(String, nullable=True, default=None)
    armor_class = Column(Integer, nullable=False)
    max_health = Column(Integer, nullable=False, default=0)
    now_health = Column(Integer, nullable=False, default=0)
    equipment = Column(ARRAY(JSON), nullable=True)
    stats = Column(JSON, nullable=False)
    abilities = Column(ARRAY(JSON), nullable=True)
    is_bot = Column(Boolean, nullable=False)

async def create_tables():
    async with engine.begin() as conn:
        print(DB_NAME, 'Дарова')
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
