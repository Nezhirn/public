from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base

from config import TYPE_DB, ENGINE, DB_USER, DB_PASSWORD, DB_ADDR, DB_PORT


DATABASE_URL = f"{TYPE_DB}+{ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_ADDR}:{DB_PORT}/"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



