from pydantic import BaseModel, ConfigDict, Field

from typing import Optional, List, Union
from src.models.brand import Brand
from typing_extensions import Annotated
from src.helper.py_object_id import PydanticObjectId


class Merk(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    name: str
    url : Optional[str] = None

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
    current:float
    normal:float

class MerkDetail(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    url: str
    
class Product(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    name: str
    merk: PydanticObjectId
    merk_details: Optional[MerkDetail] = None 
    type: PydanticObjectId
    category: str
    location: str
    image : List[str]
    sku_code: str
    price : Optional[Price] = None
    cc: str
    year: str
    grade: str
    km_of_use: str

    # model_config = ConfigDict(populate_by_name = True)

