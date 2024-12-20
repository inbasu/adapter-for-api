from os import getenv

from dotenv import load_dotenv

from services.insight.connections.mars_connection import InsightMarsClient
from services.jira.connections.api_connection import JiraAPIClient

load_dotenv()


mars_client =  InsightMarsClient(
            username=getenv("NAME",''), 
            password=getenv("PWORD", ''), 
            client_id=getenv("CLIENT_ID", ''), 
            auth_token=getenv("TOKEN", ''),
            ) 



jira_api_client = JiraAPIClient(
            username=getenv("JIRA_USER_NAME",''), 
            password=getenv("JIRA_PWORD", ''), 
            )
