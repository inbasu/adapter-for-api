from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

async_engine = create_async_engine("sqlite+aiosqlite:///database.db")

async_session = async_sessionmaker(async_engine)


async def get_session():
    async with async_session() as session:
        yield session

if __name__ == "__main__":
    from database.models import Base

    async def create_table():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

