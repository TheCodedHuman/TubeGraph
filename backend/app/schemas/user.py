# Schemas are such files/components of backend architecture, which validates the incoming and outgoing data like a bouncer

# Imports
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# BaseModel creates an "in-memory data-structure" which we can use by inheriting in python classes
class UserBase(BaseModel):              # shared property for both incoming request and outgoing response
    email: EmailStr                     # pydantic's  email validator
    username: str

# Inherting UserBase into UserCreate makes the email and username part available
class UserCreate(UserBase):
    password: str                       # this is raw password rather than hashed one

# Properties that will be shared to the frontend as a response
class UserResponse(UserBase):
    id: int                             # we didn't included the password as we do not share it back in frontend to the user in the JSON payload
    createdAt: datetime                 # the current time the response is sent, also being sent in type of datetime representation
    
    # this tells pydantic to read data from a sqlalchemy ORM model
    model_config = ConfigDict(from_attributes=True)
    
