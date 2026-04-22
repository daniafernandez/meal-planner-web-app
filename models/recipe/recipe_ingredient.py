from pydantic import BaseModel

from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit


class RecipeIngredient(BaseModel):
    ingredient: Ingredient
    units: IngredientUnit
    quantity: float
    active: bool = True
    prep_descriptor: str | None = None  # prep descriptor/instructions for the ingredient, like chopped, thawed, etc.
