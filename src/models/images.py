from typing import Optional
from pydantic import BaseModel, Field

from src.helper.py_object_id import PydanticObjectId


class Image(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    image : Optional[str] = None

class ImagesView(BaseModel):
    id: str = Field(..., alias="_id")
    image: str