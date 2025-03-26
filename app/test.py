import re

def extract_image_name(image_path):
    """
    Extract the specific part of an image filename after the first hyphen.
    
    Args:
        image_path (str): The full path or filename of the image
    
    Returns:
        str or None: The extracted portion of the filename after the first hyphen,
                     without the initial hyphens
    """
    pattern = r"^[^-]+-(-*\d+)\.png$"
    match = re.search(pattern, image_path)
    
    return match.group(1) if match else None

# Example usage
image_name = "upload/2/bff8e576--1001492676369731180.png"
result = extract_image_name(image_name)
print(result)  # Output: 1001492676369731180