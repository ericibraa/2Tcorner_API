from typing import Union
from bson import ObjectId

class QueryParameter :
    limit : Union[int, None]
    page : Union[int, None]
    search : Union[str, None]
    machine: Union[str, None]
    cc: Union[str, None]
    years: Union[str, None]
    grade: Union[str, None]
    # type: Union[str, None]
    type: Union[ObjectId, None]

    def __init__(self, search = "", limit = 10, page = 1, machine = "", cc = "", years = "", grade = "", type = None) :
        self.limit = limit if limit else 10
        self.page = page if page else 1
        self.search = search if search else ""
        self.machine = machine if machine else ""
        self.cc = cc if cc else ""
        self.years = years if years else ""
        self.grade = grade if grade else ""
        # self.type = type if type else ""
        self.type = ObjectId(type) if type else None

