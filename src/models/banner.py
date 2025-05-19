from typing import Optional
from pydantic import BaseModel, Field
from src.helper.py_object_id import PydanticObjectId

class Banner(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    image: Optional[str] = None

class CreateBannerRequest(BaseModel):
    image: Optional[str]