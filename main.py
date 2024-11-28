import os

from dotenv import load_dotenv
from fastapi import FastAPI

from services.connection import Client
from services.insight import Insight
from services.schemas import SearchRequest

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





@app.get("add/{scheme}/{type_id}")
async def add_entity(scheme: int, type_id: int):
    pass
