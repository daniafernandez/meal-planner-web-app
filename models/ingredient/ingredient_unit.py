from pydantic import BaseModel

from models.generic_unit import GenericUnit


class IngredientUnit(BaseModel):
    generic_unit: GenericUnit
    gram_weight: str    # to be used as common unit for converting between IngredientUnits
