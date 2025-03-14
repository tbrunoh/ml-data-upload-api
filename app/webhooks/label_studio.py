
from fastapi import FastAPI, HTTPException, status,APIRouter
from label_studio_sdk import Annotation, Task
from label_studio_sdk.webhooks import WebhookRequest, WebhookAction
import logging

app = APIRouter(
    prefix="/webhooks/ls",
    tags=["Label studio webhooks"]
)

logger = logging.getLogger(__name__)

@app.post("/annotation-created")
async def receive_webhook(payload: dict):
    try:
        logger.info(f"Received webhook payload")
        
        # Convert the raw payload to Label Studio SDK models
        action = payload.get("action")
        
        if action == "ANNOTATION_CREATED":
            # Parse the annotation using the SDK model
            annotation_data = payload.get("annotation", {})
            annotation = Annotation(annotation_data)
            
            # Parse the associated task
            task_data = payload.get("task", {})
            task = Task(task_data)
            
            logger.info(f"Processing annotation {annotation.id} for task {task.id}")
            
            # Access annotation properties using the SDK model
            result = annotation.result
            lead_time = annotation.lead_time
            created_by = annotation.created_by
            
            # Access task data
            task_data = task.data
            
            # Your business logic here
            # For example: process annotations, update databases, trigger ML pipeline, etc.
            
            return {
                "status": "success",
                "message": f"Processed annotation {annotation.id} successfully",
                "annotation_id": annotation.id,
                "task_id": task.id,
                "project_id": payload.get("project", {}).get("id")
            }
        else:
            logger.warning(f"Received unsupported action: {action}")
            return {"status": "ignored", "message": f"Action {action} not supported"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process annotation webhook: {str(e)}"
        )
