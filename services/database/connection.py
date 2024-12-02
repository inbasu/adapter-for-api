from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

ENGINE = ""

engine = create_async_engine(ENGINE)


async_session = async_sessionmaker(engine)

# Dependency
async def get_sesion():
    async with async_session() as session:
        yield session
