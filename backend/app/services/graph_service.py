# Imports
import os
import json
from google import genai
from google.genai import types
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi import HTTPException
# from app.utils.config import logger           # TODO: use in next version | logger.info("content")

# Literals
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)                          # Initializes and validates the connection to Google’s Generative AI services


# Defined
def get_transcript(video_id: str) -> str:
    """
    Fetches and processes the English transcript for a given YouTube video.

    This function instantiates the YouTubeTranscriptApi to retrieve the raw subtitle 
    data and concatenates it into a single continuous string for LLM consumption.

    Args:
        video_id (str): The 11-character unique YouTube video identifier.

    Returns:
        str: A single string containing the full spoken text of the video.

    Raises:
        HTTPException (400): If the video does not exist, is private, or lacks English subtitles.

    Examples:
        >>> get_transcript(egDIqKLt2L4)
        "What will be tomorrow? Every evening, [music] as we prepare to rest, we ask this question to ourselves. It is [music] perhaps the biggest mystery for all mankind..."
        >>> get_transcript(ZmjBN_SY5xo)
        400 (Bad Request) -> {"detail": "Could not retrieve transcript. The video may not exist, might be private, or has no English subtitles."}
    """
    try:
        # You were right! We MUST build the factory object first in the new version.
        ytt_api = YouTubeTranscriptApi()
        
        # Fetch returns a specific Transcript Object
        transcript_obj = ytt_api.fetch(
            video_id,
            languages=['en', 'en-US', 'en-GB', 'en-CA', 'en-AU']
        )
    except Exception as e:
        print(f"Transcript Error: {e}")
        raise HTTPException(
            status_code=400, 
            detail="Could not retrieve transcript. The video may not exist, might be private, or has no English subtitles."
        )
    else:
        raw_transcript = transcript_obj.to_raw_data()
        
        transcript: str = " ".join([snippet['text'] for snippet in raw_transcript])

        if not transcript:
            raise HTTPException(status_code=400, detail="Transcript unavailable.")
        
        return transcript


def generate_graph_data(text: str) -> dict:
    """
    Analyzes transcript text using Gemini to generate a structured Knowledge Graph.

    It prompts the Gemini Flash model to extract key concepts (nodes) and their 
    relationships (edges), while also generating a Markdown-formatted video summary.
    The response is strictly constrained to a JSON format.

    Args:
        text (str): The raw transcript text extracted from the video.

    Returns:
        dict: A parsed dictionary containing 'nodes', 'edges', and a 'summary'.

    Raises:
        HTTPException (500): If the Gemini API fails to process the request.

    Examples:
        >>> generate_graph_data("What will be tomorrow? Every evening, [music] as we prepare to rest, we ask this question to ourselves. It is [music] perhaps the biggest mystery for all mankind...")
        {
            "nodes": [
                {
                    "id": "1",
                    "label": "The Future"
                }
            ],
            "edges": [
                {
                    "source": "1",
                    "target": "2",
                    "label": "ends with"
                }
            ],
            "summary": "## Video Summary"
        }
    """
    
    prompt = f"""
    You are a Knowledge Graph and Summary generator. 
    Analyze the following video transcript.
    1. Identify key concepts (nodes) and their relationships (edges).
    2. Write a comprehensive, well-structured Markdown summary of the video.
    
    Output strictly VALID JSON with this structure:
    {{
      "nodes": [
        {{"id": "1", "label": "Main Topic"}},
        {{"id": "2", "label": "Sub Concept"}}
      ],
      "edges": [
        {{"source": "1", "target": "2", "label": "relates to"}}
      ],
      "summary": "## Video Summary\\n\\nThis video explains..."
    }}
    
    TRANSCRIPT:
    {text[:4000]}
    """                                 # TODO: create a better workaround for transcript handling (like by storing transcript in a file, and sending that file to AI)
    
    # Get response from Gemini
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

    except Exception as e:
        # Raise error as Gemini API crahsed
        print(e)
        raise HTTPException(status_code=500, detail="Gemini failed to map concepts.")
    
    else:
        # Preprocess str response to python dict (when try block ran successfully)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()        # AI responses use ```<programming language name>``` pattern to represent and format code correctly`
        return json.loads(clean_json)
