from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.insight import insight_router
from routers.jira import jira_router

app = FastAPI(root_path='/api')
# Config
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"])

# Routers
app.include_router(insight_router, prefix="/insight")
app.include_router(jira_router, prefix="/jira")


