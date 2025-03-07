from fastapi import FastAPI,APIRouter, UploadFile, File, HTTPException
import storage
from models import LabelUpload
app = APIRouter(
    prefix="/uploads",
    tags=["generic"]
)


@app.post("/upload_image/")
async def upload_image(image: UploadFile = File(...)):
    data = await storage.getBlobName()
    _ = await storage.uploadImage(data.filename,data.blob_name,image)
    
@app.post("/upload_labels/")
async def upload_labels(label_upload: LabelUpload):
    _ = await storage.uploadLabels(label_upload)