# This file's only job is to gather all the different mini-routers (auth, flowcharts, users) and bundle them into one giant "Version 1" router.

# Imports
from app.api.v1.endpoints import auth
from fastapi import APIRouter

# This is the master route for all version 1 api endpoints
api_router = APIRouter()


# Now... this router gets plugged with the master (auth) router
# the prefix="/auth" means all routes inside auth.py will start with /api/v1/auth (/api/v1 is coming from main.py)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
