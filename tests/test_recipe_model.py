from uuid import UUID

from models.recipe.recipe import Recipe


def test_recipe_generates_id() -> None:
    recipe = Recipe(
        name="Fried Rice",
        servings="4",
        ingredients=[],
    )

    UUID(recipe.id)
