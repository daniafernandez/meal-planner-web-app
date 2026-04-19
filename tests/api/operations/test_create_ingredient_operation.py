import pytest

from api.operations import CreateIngredientOperation
from models.api_models import IngredientResponse
from models.ingredient.ingredient import Ingredient
from tests.factories import (
    build_create_ingredient_request,
    build_ingredient,
    build_ingredient_service,
)


def test_create_ingredient_build_ingredient() -> None:
    operation = CreateIngredientOperation(
        request=build_create_ingredient_request(),
        ingredient_service=build_ingredient_service(),
    )

    assert operation.build_ingredient() == Ingredient(
        id="rice",
        name="Rice",
        staple=True,
        units=[],
    )


def test_create_ingredient_delegates_to_service() -> None:
    ingredient = build_ingredient()
    ingredient_service = build_ingredient_service()
    operation = CreateIngredientOperation(
        request=build_create_ingredient_request(),
        ingredient_service=ingredient_service,
    )

    created_ingredient = operation.create_ingredient(ingredient)

    assert created_ingredient == ingredient
    assert ingredient_service.get_ingredient_by_id(ingredient.id) == ingredient


def test_create_ingredient_validate_created_ingredient_requires_created_ingredient() -> None:
    operation = CreateIngredientOperation(
        request=build_create_ingredient_request(),
        ingredient_service=build_ingredient_service(),
    )

    with pytest.raises(ValueError, match="created_ingredient must be set"):
        operation.validate_created_ingredient()


def test_create_ingredient_validate_created_ingredient() -> None:
    ingredient = build_ingredient()
    operation = CreateIngredientOperation(
        request=build_create_ingredient_request(),
        ingredient_service=build_ingredient_service(),
    )
    operation.created_ingredient = ingredient

    assert operation.validate_created_ingredient() == ingredient


def test_create_ingredient_response_property() -> None:
    ingredient = build_ingredient()
    operation = CreateIngredientOperation(
        request=build_create_ingredient_request(),
        ingredient_service=build_ingredient_service(),
    )
    operation.created_ingredient = ingredient

    assert operation.response == IngredientResponse(ingredient=ingredient)


def test_create_ingredient_execute() -> None:
    ingredient_service = build_ingredient_service()
    operation = CreateIngredientOperation(
        request=build_create_ingredient_request(),
        ingredient_service=ingredient_service,
    )

    response = operation.execute()
    created_ingredient = ingredient_service.get_ingredient_by_id("rice")

    assert response == IngredientResponse(ingredient=created_ingredient)
    assert operation.ingredient == created_ingredient
    assert operation.created_ingredient == created_ingredient
