from typing import Optional
from pydantic import BaseModel, Field

from src.helper.py_object_id import PydanticObjectId


class Image(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    image : Optional[str] = None