from src.models.images import Image
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

async def addImageToDB(db: AsyncIOMotorDatabase, data: Image): # type: ignore
    try:
        data_dict = jsonable_encoder(data)
        
        data_dict["_id"] = ObjectId()

        res = await db.images.insert_one(data_dict)

        return str(res.inserted_id)
    except Exception as e:
        print(e)
        return {"error": str(e)}
