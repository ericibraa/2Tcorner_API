from pydantic import BaseModel, ConfigDict, Field

from typing import Optional, List, Union
from src.models.brand import Brand
from typing_extensions import Annotated
from src.helper.py_object_id import PydanticObjectId


class Price(BaseModel):
    discount:Optional[float] = 0
    current:float
    normal:float

    
class Product(BaseModel):
    id : PydanticObjectId = Field(alias="_id")
    name: str
    sap_code: str
    brand: PydanticObjectId
    image : List[str]
    price : Optional[Price] =None
    brand_detail: Optional[Brand] =None

    model_config = ConfigDict(populate_by_name = True)

