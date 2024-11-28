from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import InsightEntity, InsightField
from services.schemas import Field


class EntityUOW: # UoW не репозиторий
    @classmethod
    async def get_id_with_name(cls, session: AsyncSession, name: str, scheme: int) -> InsightEntity | None:
        querry = select(InsightEntity).filter(and_(InsightEntity.name==name, InsightEntity.scheme==scheme,))
        result = await session.execute(querry)
        return result.scalar()
    

    @classmethod
    async def load_entity(cls, session: AsyncSession, data: dict, fields: list[Field]) -> InsightEntity:
        new = InsightEntity(*data)
        for field in fields:
            session.add(InsightField(name=field.name, id=field.id, rel_to=new.pk))
        await session.commit()
        return new
    


