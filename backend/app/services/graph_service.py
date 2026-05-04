# Imports
import os
import json
from google import genai
from google.genai import types
from youtube_transcript_api import YouTubeTranscriptApi
# from app.utils.config import logger           # TODO: use in next version | logger.info("content")

# Literals
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)                          # Initializes and validates the connection to Google’s Generative AI services


# Defined
def get_transcript(video_id: str) -> str | None:
    """Fetches the raw text transcript from a YouTube video ID"""
    try:
        ytt_api = YouTubeTranscriptApi()                        # instantiation of object which extracts transcript from YouTube
        raw_transcript = ytt_api.fetch(                         # retrieves the transcript (subtitles) of a specific YouTube video in a given language 
            video_id,
            languages=['en', 'en-US', 'en-GB', 'en-CA', 'en-AU']
        )
        processed_transcript = " ".join([snippet.text for snippet in raw_transcript])               # unifies different inconsostant sentences and paragraps
        return processed_transcript
    except Exception as e:
        print(f"Transcript Error: {e}")
        return None
        

def generate_graph_data(text: str) -> dict | None:
    """Sends transcript text to Gemini and returns a structured JSON dictionary"""
    
    prompt = f"""
    You are a Knowledge Graph generator. 
    Analyze the following video transcript.
    Identify key concepts (nodes) and their relationships (edges).
    
    Output strictly VALID JSON with this structure:
    {{
      "nodes": [
        {{"id": "1", "label": "Main Topic"}},
        {{"id": "2", "label": "Sub Concept"}}
      ],
      "edges": [
        {{"source": "1", "target": "2", "label": "relates to"}}
      ]
    }}
    
    TRANSCRIPT:
    {text[:4000]}
    """                                 # TODO: create a better workaround for transcript handling (like by storing transcript in a file, and sending that file to AI)
    
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest", 
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json" 
            )
        )
        
        # Clean and parse the string into a Python dictionary
        clean_json = response.text.replace("```json", "").replace("```", "").strip()        # AI responses use ```<programming language name>``` pattern to represent and format code correctly`
        return json.loads(clean_json)
        
    except Exception as e:
        print(f"Gemini API Error: {e}")             # TODO: use logger module here too..
        return None
