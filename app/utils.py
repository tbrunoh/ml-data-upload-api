import re

def extract_image_filename(image_url: str, ext:str = "png"):
    match = re.search(rf"^[^-]+-(-*\d+)\.{ext}", image_url)
    return match.group(1) if match else "unknown"
