from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import InsightEntity, InsightField
from services.schemas import EntityScheme, Field


class EntityUOW: # UoW не репозиторий
    @classmethod
    async def get_id_with_name(cls, session: AsyncSession, name: str, scheme: int) -> int | None:
        querry = select(InsightEntity).filter(and_(InsightEntity.name==name, InsightEntity.scheme==scheme,))
        result = await session.execute(querry)
        if item := result.scalar():
            return item.type_id
        return None
    

    @classmethod
    async def create_entity(cls, session, entity: EntityScheme, fields: list[Field]) -> None:
        new = InsightEntity(type_id=entity.item_type, name=entity.name, scheme=entity.scheme)
        session.add(new)
        session.add_all([InsightField(name=field.name, id=field.id, rel_to=new) for field in fields])
        await session.commit() 



