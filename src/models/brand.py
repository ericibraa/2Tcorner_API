from pydantic import BaseModel, Field, ConfigDict
from pydantic.networks import EmailStr
from typing import Optional, List
from src.helper.py_object_id import PydanticObjectId 
from beanie import Document, PydanticObjectId

class Brand(BaseModel):
     name:str
     slug:str
     logo: Optional[List[str]] =[]
     
