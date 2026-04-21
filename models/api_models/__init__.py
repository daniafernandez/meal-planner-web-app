from pydantic import BaseModel, Field

from models.generic_unit import GenericUnit
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from models.ingredient.size_description import SizeDescription


class CreateGenericUnitRequest(BaseModel):
    name: str


class GenericUnitResponse(BaseModel):
    generic_unit: GenericUnit


class CreateIngredientRequest(BaseModel):
    name: str
    staple: bool = False

class AddIngredientUnitRequest(IngredientUnit):
    generic_unit_id: str
    size: SizeDescription | None = None
    gram_weight: float = Field(gt=0)


class IngredientResponse(BaseModel):
    ingredient: Ingredient


class IngredientUnitResponse(BaseModel):
    ingredient: Ingredient
    ingredient_unit: IngredientUnit
