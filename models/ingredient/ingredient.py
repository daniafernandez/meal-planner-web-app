from models.ingredient.ingredient_unit import IngredientUnit
from models.project_model import ProjectModel


class Ingredient(ProjectModel):
    name: str
    staple: bool    # ingredient is staple if it needs to be bought less frequently than 1x a week
    units: list[IngredientUnit]