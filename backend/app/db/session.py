# Session are "Waiter" that communicates with the DB-Chef and immediately gets fired (digitally) to prevent data leaks

# Imports
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from urllib.parse import quote_plus


# Load the .env file (one more sighting you can find of loading it "again" is in alembic/env.py file)
load_dotenv()           # this silently fails in 'containers' because services (like backend-api, db) doesn't have .env file. compose.yaml provides password to container when used os.getenv() as below

# Get the components of database url
POSTGRES_USER = os.getenv("POSTGRES_CONTAINER")                 # keeping it container because the docker container is driving the db like an user
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "db")

# Usage of @ in password is forbidden in database urls, so we have to do  URL encoding of @ to %40
raw_password = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_PASSWORD = quote_plus(raw_password)

# Cloud databases (like Neon) are highly secure and require an SSL connection (?sslmode=require) but local databases do not
ssl_mode = "?sslmode=require" if POSTGRES_SERVER != "db" else ""
SAFE_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}{ssl_mode}"       

# Create the 'connection' with the associated db
engine = create_engine(SAFE_DATABASE_URL)        

# Create session 'factory' (session will vanish after each communication)
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

# Create the Base Class (The blueprint all our future models will inherit from)
Base = declarative_base()       # its a function that creates and returns a class
