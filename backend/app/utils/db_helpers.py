# imports
from sqlalchemy.orm import Session
from app.models.flowchart import Flowchart
from app.models.userlibrary import UserLibrary
from sqlalchemy import select

# NOTE: Depends(get_db_session) won't work here, as whole db 'context' changes here. Have to pass separately in 'api' calls

# Internal Utility
def push_to_db(obj, db: Session):
    """Unified single liner method to do all three following processes at once"""
    db.add(obj)
    db.commit()
    db.refresh(obj)

    
# Defined
def get_existing_flowchart(
        video_id: str,
        temperature: float,
        db: Session
    ) -> Flowchart | None:
    """
    Queries the database for an existing flowchart matching the video ID and temperature.

    Args:
        db (Session): The active SQLAlchemy database session.
        video_id (str): The 11-character unique YouTube video identifier.
        temperature (float): The LLM creativity parameter used during generation (0.0 to 1.0).

    Returns:
        Flowchart | None: The Flowchart ORM object if a match exists, otherwise None.
    
    Examples:
        >>> get_existing_flowchart("piKJOD2s8KY", 0.7, db)
        <Flowchart(id=5, video_id='piKJOD2s8KY', temperature=0.7)>
        >>> get_existing_flowchart("invalid_id", 0.5, db)
        None
    """

    stmt = select(Flowchart).where(
        Flowchart.video_id == video_id,
        Flowchart.temperature == temperature    
    )

    flowchart_row = db.execute(stmt).scalars().first()

    return flowchart_row


def save_flowchart(
        video_id: str, 
        temperature: float, 
        graph_json: dict,
        db: Session
    ) -> Flowchart:
    """
    Saves the LLM-generated JSON to populate the global cache for future requests.

    Args:
        db (Session): The active SQLAlchemy database session.
        video_id (str): The 11-character unique YouTube video identifier.
        temperature (float): The LLM creativity parameter used during generation (0.0 to 1.0).
        graph_json (JSON): The LLM JSON output.

    Returns:
        Flowchart: The newly created Flowchart ORM object (containing its new primary key ID).
    
    Examples:
        >>> save_flowchart(db, "piKJOD2s8KY", 0.7, gemini_response)
        <Flowchart(id=5, video_id='piKJOD2s8KY', temperature=0.7)>
    """

    new_flowchart = Flowchart(
        video_id = video_id,
        temperature = temperature,
        graph_json = graph_json
    )

    push_to_db(new_flowchart, db)
    return new_flowchart


def update_userlib(
        user_id: int, 
        flowchart_id: int,
        db: Session
    ) -> UserLibrary:
    """
    If relationship (junction table entry) doesn't exists already, it links a saved flowchart to a specific user's account in the junction table.\n
    *man, even a daym function got "if relationship doesn't exists already" flex :(*

    Args:
        db (Session): The active SQLAlchemy database session.
        user_id (int): The primary key ID of the currently logged-in user.
        flowchart_id (int): The primary key ID of the target Flowchart.

    Returns:
        UserLibrary: The junction table ORM object representing the link.
    """

    stmt = select(UserLibrary).where(       # 1. Check if the link already exists!
        UserLibrary.user_id == user_id,
        UserLibrary.flowchart_id == flowchart_id
    )
    existing_link = db.execute(stmt).scalars().first()

    if existing_link:           # They already own it, just return it
        return existing_link    # just return it...

    new_link = UserLibrary(                 # 2. If not, create the new link
        user_id=user_id,
        flowchart_id=flowchart_id
    )
    
    push_to_db(new_link, db)
    return new_link
