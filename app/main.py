from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import our files
from app.database import get_db, engine
from app import models
from app.schemas import Recipe, RecipeCreate, RecipeUpdate

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ================== API ENDPOINTS ==================

# 1. GET / - Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Cooked-Book API!"}

# 2. POST /recipes/ - Create a new recipe
@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    # Create Recipe object from schema
    db_recipe = models.Recipe(
        title=recipe.title,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions
    )
    
    # Add to database
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    
    return db_recipe

# 3. GET /recipes/ - Get all recipes
@app.get("/recipes/", response_model=List[Recipe])
def get_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = db.query(models.Recipe).offset(skip).limit(limit).all()
    return recipes

# 4. GET /recipes/{id} - Get one recipe by ID
@app.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return recipe

# 5. PUT /recipes/{id} - Update a recipe
@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe_update: RecipeUpdate, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Update only the fields that were provided
    update_data = recipe_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(recipe, field, value)
    
    db.commit()
    db.refresh(recipe)
    
    return recipe

# 6. DELETE /recipes/{id} - Delete a recipe
@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db.delete(recipe)
    db.commit()
    
    return {"message": "Recipe deleted successfully"}
