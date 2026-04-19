from pydantic import BaseModel, Field

from models.generic_unit import GenericUnit, MeasurementType
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit


class CreateGenericUnitRequest(BaseModel):
    id: str
    name: str
    measurement_type: MeasurementType


class GenericUnitResponse(BaseModel):
    generic_unit: GenericUnit


class CreateIngredientRequest(BaseModel):
    id: str
    name: str
    staple: bool = False


class AddIngredientUnitSizeRequest(BaseModel):
    quantity: int = Field(gt=0)
    generic_unit_id: str


class AddIngredientUnitRequest(BaseModel):
    generic_unit_id: str
    size: AddIngredientUnitSizeRequest | None = None
    gram_weight: float = Field(gt=0)


class IngredientResponse(BaseModel):
    ingredient: Ingredient


class IngredientUnitResponse(BaseModel):
    ingredient: Ingredient
    ingredient_unit: IngredientUnit
