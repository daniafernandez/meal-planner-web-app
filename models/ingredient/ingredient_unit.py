from pydantic import BaseModel, Field, computed_field

from models.generic_unit import GenericUnit


class SizeDescription(BaseModel):
    quantity: int = Field(gt=0)
    generic_unit: GenericUnit

    @property
    def description_string(self) -> str:
        return f"{self.quantity} {self.generic_unit.name}"


class IngredientUnit(BaseModel):
    generic_unit: GenericUnit
    size: SizeDescription | None = None
    gram_weight: float = Field(gt=0)    # common conversion weight for this ingredient/unit pair

    @computed_field
    @property
    def name(self) -> str:
        if self.size:
            return f"{self.size.description_string} {self.generic_unit.name}"
        return self.generic_unit.name
