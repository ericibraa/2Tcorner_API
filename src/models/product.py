from pydantic import BaseModel, ConfigDict, Field

from typing import Optional, List, Union
from src.models.brand import Brand
from typing_extensions import Annotated
from src.helper.py_object_id import PydanticObjectId


class Merk(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    name: str

class Category(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    name: str

class Type(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    name: str

class Location(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    name: str

class Price(BaseModel):
    discount:Optional[float] = 0
    current:float
    normal:float

    
class Product(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    name: str
    merk: PydanticObjectId
    type: PydanticObjectId
    category: PydanticObjectId
    location: PydanticObjectId
    image : List[str]
    sku: str
    price : Optional[Price] =None
    engine: str
    capacity: str
    year: str
    grade: str
    km_of_use: str

    model_config = ConfigDict(populate_by_name = True)

