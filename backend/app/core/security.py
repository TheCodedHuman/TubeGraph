# When dealing with user's passwords, we cannot store plaintext passwords in database
# so, we need certain functions that hash (no way of return to plaintext) those passwords
# and, later when user tries to login (or do something) with their plaintext password, then it matches the hashed password
# (hashed data cannot be reversed to previous form, making it incredibly secure, as the code that hashed it, is capable to validate it (dunno how))
# its a core utility on which the architecture (security part) depends on, so we should store it in core/ folder

# Imports
import bcrypt
import os       # using os module to get .env secret values
import jwt      # requires PyJWT module
from datetime import datetime, timedelta, timezone

# We use bcrypt, the industry standard hashing algorithm
# this returns an object consisting of several methods 
# (which means, when created an object out of it, it carries all the tools to deal with the data in its lifecycle)
# (maybe that's why it have naming pws_context => password-context, carrying all capabilites for the password within object)
# # bcrypt pours "salt" in the "raw" password :)


# Literals
SECRET_KEY = os.getenv("SECRET_KEY", "TheCodedHuman")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE", default=10))             # os.getenv() returns string


# Defined
def get_password_hash(password: str) -> str:
    """Scrambles a raw password into a secure hash"""
    
    password_in_bytes = password.encode('utf-8')                # cryptography requires bytes, not strings!
    salt = bcrypt.gensalt()                                     # generates a random salt
    hashed_password = bcrypt.hashpw(password_in_bytes, salt)    # hashes the password, while combining the salt

    return hashed_password.decode('utf-8')                      # gets stored in database (we can store "encoded" passwords, but our user model have String type_ in models/user.py file)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a plain password matches the scrambled hash in the database"""
   
    password_in_bytes = plain_password.encode('utf-8')
    hashed_password_in_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_in_bytes, hashed_password_in_bytes)

def create_access_token(data: dict) -> str:
    """Forges the VIP wristband (JWT) for the user"""

    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()                                     # dicts are reference objects, NOT-cloning manipulates the actual data
    to_encode.update({"exp": expire_time})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)  # actual jwt token generator, to_encode is the payload (around which token gets wrapped up)

    return encoded_jwt

