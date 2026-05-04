# Imports
import bcrypt
import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, get_db_session
from app.models.user import User

# Literals
SECRET_KEY = os.getenv("SECRET_KEY", "TheCodedHuman")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE", default=10))             # os.getenv() returns string
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

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


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db_session)):
    """Decodes the JWT and finds the user in the database"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])         # 1. Decode the wristband using our secret key
        email: str = payload.get("sub")                                         # 2. Extract the email ("sub") we put in there during login
        if email is None:
            raise credentials_exception
            
    except jwt.PyJWTError:              # Catches expired or tampered tokens
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()                   # 3. Look up the user in the database to make sure they haven't been deleted
    if user is None:
        raise credentials_exception
        
    return user                                                                 # 4. Hand the verified user object to the route
