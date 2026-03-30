from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:hbxt9688@172.31.136.83:5432/news_app"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

# Compatible with SQLAlchemy 1.4
AsyncSession_Local = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSession_Local() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
