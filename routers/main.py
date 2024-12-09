
from fastapi import APIRouter

from main import client
from services.insight import Insight
from services.schemas import GetIQLData, GetJoinedData, GetObjectData

main_router = APIRouter()

@main_router.post('/get')
async def get_object(data: GetObjectData):
    return await Insight.get_object(client=client, data=data)


@main_router.post('/iql')
async def get_objects(data: GetIQLData):
    return await Insight.get_objects(client=client, data=data)

@main_router.post('/')
async def get_joined(data: GetJoinedData):
    result = await Insight.get_joined(client=client, data=data)
    for item in result:
        item.joined = [max(item.joined, key=lambda i: i.id)]
    return result
