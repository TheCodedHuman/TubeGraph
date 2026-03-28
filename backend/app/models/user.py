# Models are such python-classes which tells ORM to create a relational table with fields and constraints given to them in parenthesis

# Imports
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

# if we did not have imported Base, then the User class would've function just like any other 'python' class
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)                          # field 1 => id
    username = Column(String, unique=True, index=True, nullable=False)          # field 2 => user_name
    email = Column(String, unique=True, index=True, nullable=False)             # field 3 => email
    password_hash = Column(String, nullable=False)                              # field 4 => hashed_password

    # func.now() tells postgres to automatically stamp the exact time it was created (processed by db, and not by server)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())      # field 5 => current_time
