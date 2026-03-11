# Here we are fabricating entry point for the TubeGraph Backend

# Imports
from fastapi import FastAPI

# Literals
app = FastAPI(title="TubeGraph API")

# Routes
@app.get("/")
def sanity_check():
    return { "message": "tubegraph has awakened" }