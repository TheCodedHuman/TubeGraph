# Session are "Waiter" that communicates with the DB-Chef and immediately gets fired (digitally) to prevent data leaks

# Imports
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Fetch db-url from .env file
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")        

# Create the 'connection' with the associated db
engine = create_engine(SQLALCHEMY_DATABASE_URL)        

# Create session 'factory' (session will vanish after each communication)
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

# Create the Base Class (The blueprint all our future models will inherit from)
Base = declarative_base()       # its a function that creates and returns a class
