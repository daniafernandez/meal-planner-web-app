from pydantic import BaseModel, Field, computed_field

from models.generic_unit import GenericUnit


class IngredientUnit(BaseModel):
    generic_unit: GenericUnit
    size: str | None = None
    gram_weight: float = Field(gt=0)    # common conversion weight for this ingredient/unit pair

    @computed_field
    @property
    def name(self) -> str:
        if self.size:
            return f"{self.size} {self.generic_unit.name}"
        return self.generic_unit.name
