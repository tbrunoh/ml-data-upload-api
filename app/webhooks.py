from fastapi import APIRouter, UploadFile, File


app = APIRouter(
    prefix="/webhook",
    tags=["webhook"]
)


@app.post("/label-studio")
async def receive_webhook(file: UploadFile = File(...)):
    content = await file.read()
    print(content.decode("utf-8"))
    return {"message": "Webhook received"}