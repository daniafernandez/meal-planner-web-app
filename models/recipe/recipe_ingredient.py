from pydantic import BaseModel

from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from models.recipe.recipe_ingredient_parser import RecipeIngredientParser
from models.recipe.recipe_ingredient_quantity import RecipeIngredientQuantity


class RecipeIngredient(BaseModel):
    ingredient_line_string: str

    @property
    def ingredient(self) -> Ingredient | None:
        return RecipeIngredientParser().parse(self.ingredient_line_string).ingredient

    @property
    def unit(self) -> IngredientUnit | None:
        return RecipeIngredientParser().parse(self.ingredient_line_string).unit

    @property
    def quantity(self) -> RecipeIngredientQuantity:
        return RecipeIngredientParser().parse(self.ingredient_line_string).quantity

    active: bool = True
