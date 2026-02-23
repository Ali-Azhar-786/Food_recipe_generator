from dotenv import load_dotenv
import os
from typing import List, Union

from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    """Create and return configured Groq LLM instance"""
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=1200,
        api_key=os.getenv("GROQ_API_KEY"),
    )


def generate_recipe(food: str) -> str:
    """Generate a complete recipe for a detected single food item"""
    llm = get_llm()
    
    prompt = f"""You are an experienced home cook.
Generate a clear, delicious, realistic recipe for **{food}**.

Include the following sections:
1. Dish name
2. Number of servings (default 2-4)
3. Preparation + cooking time
4. Ingredients list with quantities
5. Step-by-step instructions
6. Optional: quick tips or serving suggestions

Use friendly, easy-to-follow language."""
    
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"Error generating recipe: {str(e)}"


def generate_dish_suggestions(ingredients: List[str]) -> str:
    """Generate dish suggestions from list of detected fruits/vegetables"""
    if not ingredients:
        return "No ingredients were detected in the image."
    
    ingred_list = ", ".join(ingredients)
    llm = get_llm()
    
    prompt = f"""You are a creative yet practical chef.
Here are the main ingredients available: **{ingred_list}**

Suggest **3 different tasty dishes** that can be made primarily using these ingredients.
Minimal additional common pantry items are allowed (oil, salt, spices, garlic, onion, etc.).

For each suggestion include:
• Dish name
• Main ingredients (highlight the ones from the provided list)
• Approximate preparation + cooking time
• Number of servings (2-4 people)
• Clear step-by-step instructions

Make suggestions varied (e.g. breakfast/salad/main dish/dessert) and appealing!"""
    
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"Error generating suggestions: {str(e)}"