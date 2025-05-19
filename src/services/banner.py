from pydantic import TypeAdapter
from src.models.query_paramater import QueryParameter
from src.models.response_model import Pagination, PaginationResponse
from src.models.banner import Banner
from motor.motor_asyncio import AsyncIOMotorDatabase

async def getAllBanner(db: AsyncIOMotorDatabase, query : QueryParameter ) -> PaginationResponse:  # type: ignore
    match = {}
    skip = 0

    if query.page:
        skip = (query.page -1) * query.limit

    list_banner = await db.banner.find(match).limit(query.limit).skip(skip).to_list(query.limit)
    total_records = await db.banner.count_documents(match)

    res = TypeAdapter(list[Banner]).validate_python(list_banner)

    return PaginationResponse(
        message="Banner",
        status=200,
        data=res,
        pagination=Pagination(
            total_records=total_records,
            current_page=query.page,
        )
    )
