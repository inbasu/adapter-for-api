from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from database.models import InsightEntity


class Entity:
    @classmethod
    def get_id_with_name(cls, session: Session, name: str, scheme: int) -> InsightEntity | None:
        querry = select(InsightEntity).filter(and_(InsightEntity.name==name, InsightEntity.scheme==scheme,))
        return session.scalars(querry).first()
    

