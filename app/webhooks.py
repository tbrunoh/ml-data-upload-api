from fastapi import APIRouter, UploadFile, File


app = APIRouter(
    prefix="/webhook",
    tags=["webhook"]
)


@app.post("/label-studio")
async def receive_webhook(payload: dict):
    print(payload)
    return {"message": "Webhook received"}
