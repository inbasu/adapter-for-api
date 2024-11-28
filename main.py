import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
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


@app.post("/iql/run")
async def search(data: SearchRequest):
    items = await Insight.read(client, data)
    return items





@app.post("/objects/run")
async def add_entity(entity: EntityScheme, session: AsyncSession=Depends(get_session)):
    fields = await Insight.objects(client, entity)
    await EntityUOW.create_entity(session ,entity, fields)
    return fields


