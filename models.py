
from pydantic import BaseModel


class LabelUpload(BaseModel):
    image_name: str
    labels: dict