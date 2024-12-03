from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.connection import Client
from services.insight import Insight
from services.schemas import GetIQLData, GetObjectData

load_dotenv()

app = FastAPI()
client = Client(
            username=getenv("NAME",''), 
            password=getenv("PWORD", ''), 
            url=getenv("URL", ''),
            client_id=getenv("CLIENT_ID", ''), 
            auth_token=getenv("TOKEN", ''),
            )



app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"])




@app.post('/get')
async def get_object(data: GetObjectData):
    return await Insight.get_object(client, data)

@app.post('/iql')
async def iql_run(data: GetIQLData):
    return await Insight.get_objects(client, data)

