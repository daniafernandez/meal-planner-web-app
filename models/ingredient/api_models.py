from pydantic import BaseModel, Field

from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit


class CreateIngredientRequest(BaseModel):
    id: str
    name: str
    staple: bool = False


class AddIngredientUnitRequest(BaseModel):
    generic_unit_id: str
    size: str | None = None
    gram_weight: float = Field(gt=0)


class IngredientResponse(BaseModel):
    ingredient: Ingredient


class IngredientUnitResponse(BaseModel):
    ingredient: Ingredient
    ingredient_unit: IngredientUnit
