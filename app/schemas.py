from pydantic import BaseModel

# Schema for creating a new recipe
class RecipeCreate(BaseModel):
    title: str
    ingredients: str
    instructions: str

# Schema for updating a recipe (all fields optional)
class RecipeUpdate(BaseModel):
    title: str | None = None
    ingredients: str | None = None
    instructions: str | None = None

# Schema for reading recipe data (includes ID)
class Recipe(BaseModel):
    id: int
    title: str
    ingredients: str
    instructions: str
    
    # Tell Pydantic to read this as a model
    class Config:
        from_attributes = True
