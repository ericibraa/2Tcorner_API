from pydantic import BaseModel, Field, ConfigDict
from pydantic.networks import EmailStr
from typing import Optional, Union
from typing_extensions import Annotated
from src.helper.py_object_id import PydanticObjectId 


class User(BaseModel): 
    id : PydanticObjectId = Field( alias="_id") 
    name:str
    email:EmailStr 
    password:Optional[str] = None
    token: Optional[str] = None

    model_config = ConfigDict(populate_by_name = True)


class UserForm(BaseModel):
    name:str
    password:str
    email:EmailStr

class LoginData(BaseModel):
    email : EmailStr
    password :str

class TokenData(BaseModel):
    email : EmailStr
    id : str

class Token(BaseModel):
    access_token :str
    token_type: str