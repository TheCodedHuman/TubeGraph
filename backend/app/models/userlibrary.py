# Here also we creating another model similar to user.py, flowchart.py; but using primary keys of both tables and storing them by foreignkeys in this 

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base

# Again, usage of Base helped us to inherit it and use it like a SQL model rather than python-class
class UserLibrary(Base):
    __tablename__ = "user_libraries"

    id = Column(Integer, primary_key=True, index=True)                                                  # field 1 => id (unlike django, sqlalchemy doesn't automatically injects id)

    # ForeignKey links this column directly to the 'id' column in the 'users' table
    # ondelete="CASCADE" means if the User deletes their account, their library items get automatically deleted too (recursive effect)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)               # field 2 => user_id (there could be multiple rows of same user in this column)

    # ForeignKey links this column directly to the 'id' column in the 'flowcharts' table
    flowchart_id = Column(Integer, ForeignKey("flowcharts.id", ondelete="CASCADE"), nullable=False)    # field 3 => flowchart_id (there could be multiple rows of same flowcharts in this colum)
    
    createdAt = Column(DateTime(timezone=True), server_default=func.now())                              # field 4 => current time (of server, irrespective of timezon)
