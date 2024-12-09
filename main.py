from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.main import main_router
from services.connection import Client

# Create dependency
load_dotenv()
client = Client.new(
            username=getenv("NAME",''), 
            password=getenv("PWORD", ''), 
            url=getenv("URL", ''),
            client_id=getenv("CLIENT_ID", ''), 
            auth_token=getenv("TOKEN", ''),
            )



app = FastAPI()
# Config
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"])

# Routers
app.include_router(main_router)


