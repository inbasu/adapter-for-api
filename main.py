from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.main import main_router

app = FastAPI()
# Config
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"])

# Routers
app.include_router(main_router)


