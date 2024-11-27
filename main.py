from fastapi import FastAPI
from sqlalchemy.orm import Session

from database.repository import Entity
from services.insight import Insight
from services.schemas import SearchRequest

app = FastAPI()
session = Session()

@app.post("/iql/run")
async def search(data: SearchRequest):
    if isinstance(data.item_type, str): # при запросах в инсайт, мы используем номер схемы
        item = Entity.get_id_with_name(session, name=data.item_type, scheme=data.scheme)
        if item is None:
            return [{}] # Bad reuest
        data.item_type = item.type_id
    return await Insight.read(client=None, data=data) 






@app.get("add/{scheme}/{type_id}")
async def add_entity(scheme: int, type_id: int):
    pass
