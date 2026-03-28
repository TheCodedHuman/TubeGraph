# Just the similar work we did in user.py file, here we are creating a class that will be converted to relational table by ORM

# Imports
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base

# Again, usage of Base helped us to inherit it and use it like a SQL model rather than python-class
class Flowchart(Base):
    __tablename__ = "flowcharts"

    id = Column(Integer, primary_key=True, index=True)                      # field 1 => id (unlike django, sqlalchemy doesn't automatically injects id)
    video_id = Column(String, nullable=False)                               # field 2 => yt-video-id (Indexed because we will search by URL often!)
    temperature = Column(Float, nullable=False)                             # field 3 => creativity (in generating distinct JSON)
    graph_json = Column(JSON, nullable=False)                               # field 4 => the actual node-edge json data

    createdAt = Column(DateTime(timezone=True), server_default=func.now())  # field 5 => current time
