# Imports
import re
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db_session
from app.core.security import get_current_user
from app.models.user import User
from app.models.flowchart import Flowchart
from app.models.userlibrary import UserLibrary
from app.services.graph_service import get_transcript, generate_graph_data


# Mini-router which connects to api.py file, making all these routes modularly accessible
router = APIRouter()


# Defined
def extract_video_id(url: str):
    """Extracts the 11-character video ID from a YouTube URL"""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else url


# Routes
@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_and_save_graph(
    youtube_url: str, 
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)):

    video_id = extract_video_id(youtube_url)                    # 1. Parse the URL
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    transcript_text = get_transcript(video_id)                  # 2. Fetch Transcript
    if not transcript_text:
        raise HTTPException(status_code=400, detail="Could not fetch transcript for this video.")


    graph_json = generate_graph_data(transcript_text)           # 3. Generate Graph via Gemini
    if not graph_json:
        raise HTTPException(status_code=500, detail="Gemini failed to generate the graph.")

    # Flowchart table updation
    new_flowchart = Flowchart(                                  # 4. Save to Flowcharts Table
        video_id=video_id,
        temperature=0.7,        # TODO: Default for now, handle variability in v2
        graph_json=graph_json
    )
    db.add(new_flowchart)
    db.commit()
    db.refresh(new_flowchart)   # Grabs the newly created ID by reloading the state of that ORM object from the database


    # UserLibrary table updation
    new_library_entry = UserLibrary(                            # 5. Link it to the User in the Library Table
        user_id=current_user.id,
        flowchart_id=new_flowchart.id
    )
    db.add(new_library_entry)
    db.commit()

    return {                                                    # 6. Return the raw graph data to the frontend for rendering
        "message": "Graph successfully generated and saved to your library!",
        "flowchart_id": new_flowchart.id,
        "graph_data": graph_json
    }
