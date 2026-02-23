from transformers import pipeline
from PIL import Image

MODEL_VERSION = '1.0.0'

# Load model once at module level
try:
    classifier = pipeline("image-classification", model="nateraw/food")
except Exception as e:
    classifier = None
    print(f"Error loading food classification model: {e}")


def detect_food(image_path: str) -> str:
    """
    Detect the main food item in the given image.
    Returns the top predicted food label.
    """
    if classifier is None:
        raise ValueError("Food classification model failed to load.")
    
    image = Image.open(image_path)
    results = classifier(image)
    top_label = results[0]['label']
    return top_label