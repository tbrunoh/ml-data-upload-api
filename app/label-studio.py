from fastapi import APIRouter

app = APIRouter(
    prefix="/webhooks/label-studio",
    tags=["Label studio webhooks"]
)


@app.post("/label-created")
async def receive_webhook(payload: dict):
    print(payload)
    return payload
