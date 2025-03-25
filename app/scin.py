from fastapi import APIRouter, UploadFile, File

import app.storage as storage
# from app.models import LabelUpload

app = APIRouter(
    prefix="/scin",
    tags=["Scin Data Upload"]
)


@app.post("/image/")
async def upload_image(image: UploadFile = File(...)):
    data = storage.getBlobName(image.filename ,"scin",True )
    filename = await storage.uploadImage(data["filename"], data["blob_name"], image)
    return {
        "filename":filename
    }
    
# @app.post("/labels/")
# async def upload_labels(label_upload: LabelUpload):
#     _ = await storage.uploadLabels(label_upload)