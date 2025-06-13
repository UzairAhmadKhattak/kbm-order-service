
from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

DATABASE_URL = (
    f"{os.environ['DRIVER']}+asyncpg://"
    f"{os.environ['USERNAME']}:{os.environ['PASSWORD']}@"
    f"{os.environ['HOST']}/{os.environ['DATABASE']}"
)

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()

# Dependency
async def get_async_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
