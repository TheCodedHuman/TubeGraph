# Here we are fabricating entry point for the TubeGraph Backend

# Imports
from fastapi import FastAPI
from app.api.v1.api import api_router

# Literals
app = FastAPI(title="TubeGraph API", version="1.0.0")

# plugs the entire v1 api mechanism into the application
app.include_router(api_router, prefix="/api/v1")

# Routes
@app.get("/")
def sanity_check():
    return { "message": "tubegraph has awakened" }