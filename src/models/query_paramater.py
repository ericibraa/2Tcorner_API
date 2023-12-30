from typing import Union

class QueryParameter :
    limit : Union[int, None]
    page : Union[int, None]
    search : Union[str, None]

    def __init__(self, search = "", limit = 10, page = 1 ) :
        self.limit = limit if limit else 10
        self.page = page if page else 1
        self.search = search if search else ""