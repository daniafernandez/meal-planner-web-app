from tests.factories import (
    build_recipe,
    build_recipe_ingredient,
    build_recipe_service,
    build_recipe_without_ingredients,
)


def test_recipe_service_push_recipe_ingredient() -> None:
    service = build_recipe_service()
    recipe = build_recipe_without_ingredients()
    recipe_ingredient = build_recipe_ingredient()
    service.create_recipe(recipe)

    update_result = service.push_recipe_ingredient(
        recipe_id=recipe.id,
        recipe_ingredient=recipe_ingredient,
    )

    assert update_result.matched_count == 1


def test_recipe_service_add_ingredient_to_recipe_returns_update_result() -> None:
    service = build_recipe_service()
    recipe = build_recipe_without_ingredients()
    recipe_ingredient = build_recipe_ingredient()
    service.create_recipe(recipe)

    update_result, added_recipe_ingredient = service.add_ingredient_to_recipe(
        recipe_id=recipe.id,
        recipe_ingredient=recipe_ingredient,
    )

    assert update_result.matched_count == 1
    assert added_recipe_ingredient == recipe_ingredient


def test_recipe_service_add_ingredient_to_recipe_adds_recipe_ingredient() -> None:
    service = build_recipe_service()
    recipe = build_recipe_without_ingredients()
    recipe_ingredient = build_recipe_ingredient()
    service.create_recipe(recipe)

    _, added_recipe_ingredient = service.add_ingredient_to_recipe(
        recipe_id=recipe.id,
        recipe_ingredient=recipe_ingredient,
    )

    assert service.get_recipe_by_id("fried-rice") == build_recipe(
        recipe_ingredient=added_recipe_ingredient,
    )
