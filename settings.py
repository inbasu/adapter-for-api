from os import getenv

from dotenv import load_dotenv

from services.connections.jira_api_connection import JiraAPIClient
from services.connections.mars_connection import MarsClient

load_dotenv()


insight_mars_client =  MarsClient(
            username=getenv("INSIGHT_MARS_USERNAME",''), 
            password=getenv("INSIGHT_MARS_PASSWORD", ''), 
            client_id=getenv("INSIGHT_MARS_CLIENT_ID", ''), 
            auth_token=getenv("INSIGHT_MARS_TOKEN", ''),
            ) 



jira_mars_client = MarsClient(
            username=getenv("JIRA_MARS_USERNAME",''), 
            password=getenv("JIRA_MARS_PASSWORD", ''), 
            client_id=getenv("JIRA_MARS_CLIENT_ID", ''), 
            auth_token=getenv("JIRA_MARS_TOKEN", ''),
        )

jira_api_client = JiraAPIClient(
            username=getenv("JIRA_USER_NAME",''), 
            password=getenv("JIRA_PWORD", ''), 
            )
