# This file's only job is to gather all the different mini-routers (auth, flowcharts, users) and bundle them into one giant "Version 1" router.

# Imports
from app.api.v1.endpoints import auth, graph
from fastapi import APIRouter

# This is the master route for all version 1 api endpoints
api_router = APIRouter()

# Plug in the mini-routers - prefix could've been suffix ;) as these are going to be in last of URLs
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(graph.router, prefix="/graph", tags=["graph"])
