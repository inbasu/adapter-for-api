



from services.connection import Client


class Jira:
    
    @classmethod
    async def get_requests(cls, client: Client, jql: str):
        result = client.post(jql)
        return result
