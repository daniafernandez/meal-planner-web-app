from models.project_model import ProjectModel
from models.recipe.recipe_ingredient import RecipeIngredient


class Recipe(ProjectModel):
    name: str
    servings: str
    ingredients: list[RecipeIngredient]
