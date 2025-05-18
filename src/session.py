
from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker
from sqlalchemy.orm import declarative_base

env = dotenv_values('.env')

DATABASE_URL = f"{env['DRIVER']}+asyncpg://{env['USERNAME']}:{env['PASSWORD']}@{env['HOST']}/{env['DATABASE']}"

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()

# Dependency
async def get_async_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
