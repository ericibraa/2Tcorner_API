from bson import ObjectId
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
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

    if not inserted_id:
        return {"error": "Failed to insert image into DB"}

    return {"image": file_url, "_id": inserted_id}

@router.delete("/{id}")
async def delete_image(id: str, db: AsyncIOMotorDatabase = Depends(getDB)): # type: ignore

    image = await db.images.find_one({"_id": ObjectId(id)})

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    image_url = image.get("image")

    delete_success = await spaces.delete_from_spaces(image_url)

    if not delete_success:
        raise HTTPException(status_code=500, detail="Failed to delete image from Spaces")

    await db.images.delete_one({"_id": ObjectId(id)})

    return {"message": "Image deleted successfully"}