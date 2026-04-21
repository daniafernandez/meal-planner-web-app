from pydantic import Field, field_validator

from models.ingredient.ingredient_unit import IngredientUnit
from models.project_model import ProjectModel


class Ingredient(ProjectModel):
    name: str
    staple: bool    # ingredient is staple if it needs to be bought less frequently than 1x a week
    units: list[IngredientUnit] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, name: str) -> str:
        normalized_name = " ".join(name.casefold().split())
        if not normalized_name:
            raise ValueError("name must not be empty.")
        return normalized_name
