# Imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db_session
from app.core.security import get_current_user
from app.models.user import User
from app.models.flowchart import Flowchart
from app.services.graph_service import get_transcript, generate_graph_data
from app.utils.youtube_helpers import extract_video_id
from app.utils.db_helpers import get_existing_flowchart, save_flowchart, update_userlib

# Mini-router which connects to api.py file, making all these routes modularly accessible
router = APIRouter()


# Routes
@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_and_save_graph(
    youtube_url: str, 
    temperature: float = 0.7,                   # Added default value (would add to .env soon in future)
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)):
    """
    Generate either a new graph and save it in db, or fetch existing graph from cache (db).

    Args:
        youtube_url (str): YouTube video URL
        temperature (float): creatvity value within range 0 (rigid with transcript) and 1 (more context included)

    Returns:
        dict: FastAPI serialize it to JSON response

    Raises:
        HTTPException (400): raise 400 HTTP error for invalid YouTube URL

    Examples:
        >>> generate_and_save_graph("https://youtu.be/piKJOD2s8KY?si=HAyBXRNrHfEbjmWv", 0.5)
        {
            "message": "Graph successfully processed",
            "flowchart_id": 69,
            "nodes": [
                {
                    "id": "1",
                    "label": "node-content"
                }
            ],
            "edges": [
                {
                    "source": "1",
                    "target": "2",
                    "label": "is defined as"
                }
            ],
            "summary": "## Video Summary"
        }
            ...
    """

    # Clean Data
    video_id: str = extract_video_id(youtube_url)

    # Check Cache
    existing_flowchart: Flowchart = get_existing_flowchart(video_id, temperature, db)

    # Handle Cache Miss
    if not existing_flowchart:
        transcript_text = get_transcript(video_id)
        graph_json = generate_graph_data(transcript_text)
        existing_flowchart = save_flowchart(video_id, temperature, graph_json, db)
    
    # Link to junction table
    update_userlib(current_user.id, existing_flowchart.id, db)

    # Unified json response
    return {                                                    # 6. Return the raw graph data to the frontend for rendering
        "message": "Graph successfully processed",
        "flowchart_id": existing_flowchart.id,
        "graph_data": existing_flowchart.graph_json
    }
