from pydantic import BaseModel, ConfigDict, Field

from typing import Optional, List, Union
from typing_extensions import Annotated
from src.helper.py_object_id import PydanticObjectId


class Article(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    image: List[str] = None
    title: str
    slug: Optional[str] = None
    short_desc : str
    description: str
    author: str
    status: int