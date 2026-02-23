from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
import uuid

from model.food_detection import MODEL_VERSION, classifier, detect_food
from model.ingredients_detection import INGREDIENTS_MODEL_VERSION, ingredients_model, detect_ingredients
from gen_recipe import generate_recipe, generate_dish_suggestions

app = FastAPI(
    title="Food Recipe & Dish Suggestion API",
    description="Detect food or ingredients from images and generate recipes/suggestions",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Food Recipe & Dish Suggestion API is running"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "food_model": {
            "version": MODEL_VERSION,
            "loaded": classifier is not None
        },
        "ingredients_model": {
            "version": INGREDIENTS_MODEL_VERSION,
            "loaded": ingredients_model is not None
        }
    }


def save_temp_file(file: UploadFile) -> str:
    """Save to project folder temporarily - works everywhere"""
    file_path = f"temp_upload_{uuid.uuid4()}_{file.filename.replace(' ', '_')}"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")


@app.post("/api/v1/generate-recipe")
async def generate_recipe_from_food(file: UploadFile = File(...)):
    """
    Endpoint for single food item detection + recipe generation
    """
    try:
        file_path = save_temp_file(file)
        
        try:
            food = detect_food(file_path)
            recipe = generate_recipe(food)
            
            return {
                "success": True,
                "mode": "recipe",
                "detected_food": food,
                "recipe": recipe
            }
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/suggest-dishes")
async def suggest_dishes_from_ingredients(file: UploadFile = File(...)):
    """
    Endpoint for fruits/vegetables detection + dish suggestions
    """
    try:
        file_path = save_temp_file(file)
        
        try:
            ingredients = detect_ingredients(file_path)
            suggestions = generate_dish_suggestions(ingredients)
            
            return {
                "success": True,
                "mode": "suggestions",
                "detected_ingredients": ingredients,
                "suggestions": suggestions
            }
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))