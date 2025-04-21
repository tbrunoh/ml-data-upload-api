from fastapi import APIRouter, UploadFile, File

import app.storage as storage
import app.utils as utils
# from app.models import LabelUpload

app = APIRouter(
    prefix="/mst",
    tags=["MST Data Upload"]
)


@app.post("/image/")
async def upload_image(image: UploadFile = File(...)):
    data = storage.getBlobName(image.filename ,"mst",True )
    filename = await storage.uploadImage(data["filename"], data["blob_name"], image)
    return {
        "filename":filename
    }
@app.post("/orbs/")
async def upload_image(image: UploadFile = File(...)):
    data = storage.getBlobName(image.filename ,"orbs",True )
    filename = await storage.uploadImage(data["filename"], data["blob_name"], image)
    return {
        "filename":filename
    }
@app.post("/test/")
async def upload_image(image: UploadFile = File(...)):
    data = storage.getBlobName(image.filename ,"test",False )
    filename = await storage.uploadImage(data["filename"], data["blob_name"], image)
    return {
        "filename":filename
    } 
@app.post("/faceimage/")
async def upload_face_image(image: UploadFile = File(...)):
    data = storage.getBlobName(image.filename ,"face_images",True )
    file_content = await image.read()
    bytes = utils.process_image_with_face(file_content)
    import io
    output = UploadFile(filename=image.filename, file=io.BytesIO(bytes))
    filename = await storage.uploadImage(data["filename"], data["blob_name"], output)
    
    return {
        "filename":filename
    }


# @app.post("/labels/")
# async def upload_labels(label_upload: LabelUpload):
#     _ = await storage.uploadLabels(label_upload)