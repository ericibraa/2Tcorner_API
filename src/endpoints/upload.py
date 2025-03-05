from fastapi import APIRouter, UploadFile, File, Form, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.database.mongo import getDB
import src.services.spaces as spaces
import src.services.images as images
from src.models.images import Image

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_and_save(
    file: UploadFile = File(...),
    db: AsyncIOMotorDatabase = Depends(getDB) # type: ignore
):
    file_url = await spaces.upload_to_spaces(file, file.filename)
    
    if not file_url:
        return {"error": "Failed to upload file"}

    image = Image(image=file_url)

    inserted_id = await images.addImageToDB(db=db, data=image)

    return {"url": file_url, "id": inserted_id}
