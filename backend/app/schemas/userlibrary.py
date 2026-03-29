# Just like user.py and flowchart.py here we are again creating request, response and CRUD validations
# but due to the linking of both models (foreignkey in orm models) in this, this slightly changes the game

# Imports
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# As the foreign keys are the core parameters needs to be there, we can simply put that in the shared property
# in backend, it will help in caching but still based on the user and other users
# in frontend, it will provide data in response payload which flowchart belongs to whom
class UserLibraryBase(BaseModel):
    user_id: int
    flowchart_id: int

# The creation schema inherits the IDs but, it requires nothing extra for now
class UserLibraryCreate(UserLibraryBase):
    pass

# The response schema sent back after a user saves a flowchart
class UserLibrayResponse(UserLibraryBase):
    id: int
    createdAt: datetime

    model_config = ConfigDict(from_attributes=True)