from pydantic import BaseModel, ConfigDict, Field

from typing import Optional, List, Union
from src.models.location import LocationDetail
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
    image : Optional[str] = None

class Price(BaseModel):
    current:float
    normal:float

class MerkDetail(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    url: str

class TypeDetail(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    
class Product(BaseModel):
    id : PydanticObjectId = Field(default=False,alias="_id")
    name: str
    slug: str
    merk: PydanticObjectId
    merk_details: Optional[MerkDetail] = None 
    type: PydanticObjectId
    type_details: Optional[TypeDetail] = None
    category: str
    location: PydanticObjectId
    location_details: Optional[LocationDetail] = None
    image : List[str]
    sku_code: str
    price : Optional[Price] = None
    cc: str
    year: str
    grade: str
    km_of_use: str
    description: Optional[str] = None
    variant: str
    status: int
    instagram: Optional[str] = None
    youtube: Optional[str] = None

class ProductForm(BaseModel):
    name: str
    slug: Optional[str] = None
    merk: str
    type: str
    category: str
    location: str
    image : List[str]
    sku_code: Optional[str] = None
    price : Optional[Price] = None
    cc: str
    year: str
    grade: str
    km_of_use: str
    description: str
    variant: str
    status: Optional[int] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None

    # model_config = ConfigDict(populate_by_name = True)

