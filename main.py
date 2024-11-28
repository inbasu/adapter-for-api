import os

from dotenv import load_dotenv
from fastapi import FastAPI

from database.connection import AsyncSession
from database.repository import EntityUOW
from services.connection import Client
from services.insight import Insight
from services.schemas import EntityScheme, SearchRequest

load_dotenv()


app = FastAPI()
client = Client(
            username=os.getenv("NAME"), 
            password=os.getenv("PWORD"), 
            url=os.getenv("URL"),
            client_id=os.getenv("CLIENT_ID"), 
            auth_token=os.getenv("TOKEN"),
            )
session = AsyncSession()


@app.post("/iql/run")
async def search(data: SearchRequest):
    if isinstance(data.item_type, str):
        entity = await EntityUOW.get_id_with_name(session=session, name=data.item_type, scheme=data.scheme)
        data.item_type = entity.type_id
    items = await Insight.read(client, data)
    return items





@app.post("/objects/run")
async def add_entity(entity: EntityScheme):
    fields = await Insight.objects(client, entity)
    await EntityUOW.create_entity(session ,entity, fields)
    return fields


