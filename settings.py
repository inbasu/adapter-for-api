from os import getenv

from dotenv import load_dotenv

from services.insight.connections.mars_connection import InsightMarsClient

load_dotenv()


mars_client =  InsightMarsClient(
            username=getenv("NAME",''), 
            password=getenv("PWORD", ''), 
            client_id=getenv("CLIENT_ID", ''), 
            auth_token=getenv("TOKEN", ''),
            ) 


