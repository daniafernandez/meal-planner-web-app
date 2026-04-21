from pydantic import BaseModel, Field, computed_field

from models.generic_unit import GenericUnit
from models.ingredient.size_description import QuantitativeDescription, QualitativeDescription


class IngredientUnit(BaseModel):
    generic_unit: GenericUnit
    size: QuantitativeDescription | QualitativeDescription | None = None # TODO: see if abstract class can be used as type here
    gram_weight: float = Field(gt=0)    # common conversion weight for this ingredient/unit pair

    @computed_field
    @property
    def name(self) -> str:
        if self.size:
            return f"{self.size.description_string} {self.generic_unit.name}"
        return self.generic_unit.name
