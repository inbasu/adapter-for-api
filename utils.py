import asyncio
import sys

from database.connection import async_engine
from database.models import Base


class Database:
    @staticmethod
    async def create_table():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

if __name__== "__main__":
    
    command = sys.argv[1] if len(sys.argv) == 2 else ""

    match command:
        case "create_table":
            asyncio.run(Database.create_table())
