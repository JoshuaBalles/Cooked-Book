from sqlalchemy import Column, Integer, String
from app.database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    
    # Primary key - unique ID for each recipe
    id = Column(Integer, primary_key=True, index=True)
    
    # Recipe details
    title = Column(String, index=True)
    ingredients = Column(String)
    instructions = Column(String)
