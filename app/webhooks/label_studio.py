
from fastapi import FastAPI, HTTPException, status,APIRouter, Request
from label_studio_sdk import Annotation, Task
import logging
import app.utils as utils
import requests
import os

app = APIRouter(
    prefix="/webhooks/ls",
    tags=["Label studio webhooks"]
)

logger = logging.getLogger(__name__)

@app.post("/task-created")
async def receive_task_created(request: Request):
    try:
        logger.info("Received task created webhook payload")
       
        data = await request.json()
        
        logger.info(data)
        
        task_id = data["id"]
        image_url = data["data"]["image"]
        
        logger.info(f"taskId; {task_id}, image : {image_url}")
        
        if not task_id or not image_url:
            logger.error("Invalid payload format")
            return {"error": "Invalid payload"}, 400
        
        image_name = utils.extract_image_filename(image_url)
        LABEL_STUDIO_URL = os.getenv("LABEL_STUDIO_API_URL")
        API_TOKEN = os.getenv("LABEL_STUDIO_API_TOKEN")
        if not LABEL_STUDIO_URL:
            raise ValueError("LABEL_STUDIO_URL environment variable is not set")

        update_url = f"{LABEL_STUDIO_URL}/api/tasks/{task_id}"
        headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}
        payload = {"data": {"case_id": image_name}}

        response = requests.patch(update_url, json=payload, headers=headers)
        logger.info(response)
        
        if response.status_code == 200:
            return {"success": f"Task {task_id} updated with image_name"}
        else:
            return {"error": response.text}, response.status_code
        
        
    except Exception as e:
        logger.error(f"Error processing task created webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process task created webhook: {str(e)}"
        )


@app.post("/annotation-created")
async def receive_webhook(payload: dict):
    try:
        logger.info(f"Received webhook payload")
        
        # Convert the raw payload to Label Studio SDK models
        action = payload.get("action")
        
        if action == "ANNOTATION_CREATED":
            # Parse the annotation using the SDK model
            annotation_data = payload.get("annotation", {})
            logger.info(annotation_data)
            annotation = Annotation(annotation_data)
            
            logger.info(f"Processing annotationV1 {annotation.id}")
            
            # Parse the associated task
            task_data = payload.get("task", {})
            task = Task(task_data)
            
            logger.info(f"Processing annotation {annotation.id} for task {task.id}")
            
            # Access annotation properties using the SDK model
            result = annotation.result
            lead_time = annotation.lead_time
            created_by = annotation.created_username
            
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
