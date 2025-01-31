from pydantic import BaseModel, Field
from src.helper.py_object_id import PydanticObjectId


class Location(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    kota: str

class LocationDetail(BaseModel):
    id: str = Field(..., alias="_id")
    kota: str
    