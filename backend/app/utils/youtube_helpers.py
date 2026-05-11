# In this file we are unifying all youtube related helper or utility resources
# which could make code follow DRY principle as well as fix circular imports if they exists

# Imports
from urllib.parse import urlparse, parse_qs
from fastapi import HTTPException

# Defined
def extract_video_id(url: str) -> str:
    """
    Take ANY messy YouTube URL and return just the 11-character ID.

    Args:
        url (str): YouTube video URL

    Returns:
        str: 11-character ID

    Raises:
        HTTPException (400): If youtube.com or youtu.be isn't found in URL (basically invalid URL)

    Examples:
        >>> extract_video_url("https://youtu.be/piKJOD2s8KY?si=HAyBXRNrHfEbjmWv")
        piKJOD2s8KY
        >>> extract_video_url("https://x.com/i/status/2029656165651788225")
        400 (Bad Request) -> {"detail":"Invalid YouTube URL. Video ID must be exactly 11 characters."}
    """
    
    parsed_url = urlparse(url)                                              # splits url into individual components (eg, https, domain and port, path, etc)
    video_id = None                                                         # this value gets updated, so that str and None result gets segregated

    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:           # extended domain format
        if parse_qs(parsed_url.query).get('v', [None])[0]:                  # parses "query" string (name=Someone&age=30&age=40)
            video_id = parse_qs(parsed_url.query).get('v', [None])[0]       # parse_qs returns a dict of list object. get('v') will work fine, but [None] is a workaround to get first element
    
    elif parsed_url.hostname in ['youtu.be']:                               # consise domain format
        if parsed_url.path != "/":                                          # path can't be blank "" string, rather it comes as "/"
            video_id = parsed_url.path[1:]                                  #  /piKJOD2s8KY is the path, [1:] removes the forward slash

    if video_id == None or len(video_id) != 11:                             # guard clause
        raise HTTPException(                                                # raise error on incorrect URLs (None condition)
            status_code=400,
            detail="Invalid YouTube URL. Video ID must be exactly 11 characters."
        )      

    return video_id                                                         # return video_id (NOT none condition)
