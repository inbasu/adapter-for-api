from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

async_engine = create_async_engine("sqlite+aiosqlite:///database.db")

AsyncSession = async_sessionmaker(async_engine)


if __name__ == "__main__":
    from database.models import Base

    async def create_table():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

