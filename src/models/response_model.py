
from pydantic import BaseModel, ConfigDict, Field

from typing import Any, Union
from src.models.brand import Brand
from typing_extensions import Annotated
from src.helper.py_object_id import PydanticObjectId

class Pagination(BaseModel):
    total_records : int
    current_page :int
    next_page:Union[int, None] = None
    prev_page:Union[int, None] = None

    # def __init__(self, total_records = 0, current_page = 1, next_page = None, prev_page= None ) :
    #     self.total_records = total_records
    #     self.current_page = current_page
    #     self.next_page = next_page
    #     self.prev_page = prev_page
    

class PaginationResponse(BaseModel):
    message :str
    status : int
    data : Any
    pagination : Union[Pagination, None] = None

    # def __init__(self, message="", status=200, data=[], pagination = None ) :
    #     self.message = message
    #     self.status = status
    #     self.data = data
    #     self.pagination = pagination


class LoginResponse(BaseModel):
    access_token :str
    token_type:str