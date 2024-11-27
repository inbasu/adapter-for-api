from database.connection import async_engine
from database.models import Base


async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__== "__main__":
    import asyncio

    asyncio.run(create_table())
