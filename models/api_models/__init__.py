from enum import StrEnum

from pydantic import BaseModel, Field

from models.generic_unit import GenericUnit
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit


class CreateGenericUnitRequest(BaseModel):
    name: str


class GenericUnitResponse(BaseModel):
    generic_unit: GenericUnit


class CreateIngredientRequest(BaseModel):
    name: str
    staple: bool = False


class IngredientUnitSizeType(StrEnum):
    NONE = "none"
    QUALITATIVE = "qualitative"
    QUANTITATIVE = "quantitative"


class AddQuantitativeIngredientUnitSizeRequest(BaseModel):
    quantity: int = Field(gt=0)
    generic_unit_id: str


class AddQualitativeIngredientUnitSizeRequest(BaseModel):
    quality: str


class AddIngredientUnitRequest(BaseModel):
    generic_unit_id: str
    size: AddQuantitativeIngredientUnitSizeRequest | AddQualitativeIngredientUnitSizeRequest | None = None
    gram_weight: float = Field(gt=0)


class IngredientResponse(BaseModel):
    ingredient: Ingredient


class IngredientUnitResponse(BaseModel):
    ingredient: Ingredient
    ingredient_unit: IngredientUnit
