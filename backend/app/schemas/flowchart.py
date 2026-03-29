# Just like user.py file is validating data what user inputs and server responds back, here is the demonstration

# Imports
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# As similar done in user.py file, here we too will have shared property in request and response
class FlowchartBase(BaseModel):
    video_id: str
    temperature: float

# Eventhough flowchart base already covered the incoming traffic of video_id and temperature, its recommended to create FlowchartCreate class
# it helps in future to map out the logic like "is_public" which user can select, but for now, we can give it "pass" keyword
class FlowchartCreate(FlowchartBase):
    pass

# we use these naming standars due to the CRUD operation naming and use them as suffix
# like, UserCreate, UserUpdate, FlowchartCreate, FlowchartResponse

# We have to send node-edge json back to frontend response
class FlowchartResponse(FlowchartBase):
    id: int
    graph_json: dict            # orm sends us clean dict rather than json
    createdAt: datetime         # the timestamp of flowchart creation stored in db

    # actually, python dictionaries use brackets to point to data, eg -> user_data["email"]
    # but, sqlalchemy use dots, eg -> userdata.email
    # that's where this model_config acts as a configuration bridge between both paradigms
    model_config = ConfigDict(from_attributes=True)

