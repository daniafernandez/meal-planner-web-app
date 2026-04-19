import pytest

from api.operations import GetIngredientOperation
from models.api_models import IngredientResponse
from services.errors import ResourceNotFoundError
from tests.factories import build_ingredient, build_ingredient_service


def test_get_ingredient_validate_ingredient_id() -> None:
    ingredient = build_ingredient()
    ingredient_service = build_ingredient_service()
    ingredient_service.create_ingredient(ingredient)
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=ingredient_service,
    )

    validated_ingredient = operation.validate_ingredient_id()

    assert validated_ingredient == ingredient


def test_get_ingredient_validate_ingredient_id_not_found() -> None:
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=build_ingredient_service(),
    )

    with pytest.raises(ResourceNotFoundError, match="Ingredient 'rice' was not found."):
        operation.validate_ingredient_id()


def test_get_ingredient_validate_ingredient_requires_ingredient() -> None:
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=build_ingredient_service(),
    )

    with pytest.raises(ValueError, match="ingredient must be set"):
        operation.validate_ingredient()


def test_get_ingredient_validate_ingredient() -> None:
    ingredient = build_ingredient()
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=build_ingredient_service(),
    )
    operation.ingredient = ingredient

    assert operation.validate_ingredient() == ingredient


def test_get_ingredient_response_property() -> None:
    ingredient = build_ingredient()
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=build_ingredient_service(),
    )
    operation.ingredient = ingredient

    assert operation.response == IngredientResponse(ingredient=ingredient)


def test_get_ingredient_execute() -> None:
    ingredient = build_ingredient()
    ingredient_service = build_ingredient_service()
    ingredient_service.create_ingredient(ingredient)
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=ingredient_service,
    )

    response = operation.execute()

    assert response == IngredientResponse(ingredient=ingredient)
    assert operation.ingredient == ingredient
