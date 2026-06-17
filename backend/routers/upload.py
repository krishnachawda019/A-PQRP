import os 
import shutil
from fastapi import APIRouter, UploadFile, File
from backend.schemas.upload_schema import UploadResponse
from backend.services.upload_service import process_file

router = APIRouter()
UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
@router.post("/upload", response_model = UploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER , file.filename)
    with open(file_path, "wb") as buffer :
        shutil.copyfileobj(file.file , buffer)
    return process_file(file_path)
