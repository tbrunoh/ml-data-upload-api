import re
import cv2
from fastapi import UploadFile
import numpy as np


def extract_image_filename(image_url: str, ext:str = "png"):
    match = re.search(rf"^[^-]+-(-*\d+)\.{ext}", image_url)
    return match.group(1) if match else "unknown"


def process_image_with_face(image_file: UploadFile, output_file: UploadFile, size: int = 256):
    try:
        # Read the image from the uploaded file
        file_bytes = np.frombuffer(image_file.file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Image not found or invalid image file")
        print(f"Image shape: {image.shape}")

        # Load pre-trained face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if face_cascade.empty():
            raise RuntimeError("Failed to load Haar cascade for face detection")
        print("Haar cascade loaded successfully")

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print(f"Grayscale image shape: {gray.shape}")

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        print(f"Number of faces detected: {len(faces)}")
        if len(faces) == 0:
            raise ValueError("No face detected in the image")

        # Use the first detected face
        x, y, w, h = faces[0]
        print(f"Face coordinates: x={x}, y={y}, w={w}, h={h}")

        # Extend the region to include the neck area
        extended_y = max(0, y - int(h * 0.2))
        extended_h = min(image.shape[0], y + h + int(h * 0.2)) - extended_y
        cropped_image = image[extended_y:extended_y + extended_h, x:x + w]
        print(f"Cropped image shape: {cropped_image.shape}")

        # Validate the cropped image
        if cropped_image.size == 0:
            raise ValueError("Cropped image is empty. Check the face detection and cropping logic.")

        # Resize the cropped image to a square
        print(f"Resizing cropped image to size: {size}x{size}")
        resized_image = cv2.resize(cropped_image, (size, size))
        print(f"Resized image shape: {resized_image.shape}")

        # Save the processed image to the output file
        success, encoded_image = cv2.imencode('.png', resized_image)
        if not success:
            raise RuntimeError("Failed to encode the processed image")
        print("Image encoded successfully")

        output_file.file.write(encoded_image.tobytes())

        # Reset the file pointers of the uploaded files
        image_file.file.seek(0)
        output_file.file.seek(0)

    except Exception as e:
        print(f"Error processing image: {e}")
        raise