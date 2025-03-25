import logging
import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Load environment variables
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(root_dir, '.env'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.api as api
import app.scin as scin
from app.webhooks import label_studio

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),  # Set the logging level to INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Melanin Luxe Training Data APIs",
    description="APIs for managing training data",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.app)
app.include_router(label_studio.app)
app.include_router(scin.app)


@app.get("/health", include_in_schema=False)
def health():
    return {'status': 'Healthy'}