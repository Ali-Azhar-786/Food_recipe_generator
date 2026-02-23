from ultralytics import YOLO
from typing import List
import os

INGREDIENTS_MODEL_VERSION = 'v3.0'

# Path to your downloaded YOLO model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "yolo_fruits_and_vegetables_v3.pt")


# Load model once at module level
try:
    ingredients_model = YOLO(MODEL_PATH)
except Exception as e:
    ingredients_model = None
    print(f"Error loading YOLO ingredients model: {e}")


def detect_ingredients(image_path: str) -> List[str]:
    """
    Detect fruits and vegetables in the image using YOLO.
    Returns list of unique detected class names.
    """
    if ingredients_model is None:
        raise ValueError("YOLO ingredients detection model failed to load.")
    
    results = ingredients_model(image_path, verbose=False)
    
    # Get all detected class names
    detected_classes = []
    for result in results:
        for cls_id in result.boxes.cls:
            class_name = result.names[int(cls_id)]
            detected_classes.append(class_name)
    
    # Return unique ingredients sorted alphabetically
    return sorted(list(set(detected_classes)))