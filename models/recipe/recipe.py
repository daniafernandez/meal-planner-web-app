from pydantic.v1 import BaseModel

from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from models.project_model import ProjectModel

class RecipeIngredient(BaseModel):
    ingredient: Ingredient
    units: IngredientUnit
    quantity: float

class Recipe(ProjectModel):
    name: str
    servings: str
    ingredients: list[RecipeIngredient]