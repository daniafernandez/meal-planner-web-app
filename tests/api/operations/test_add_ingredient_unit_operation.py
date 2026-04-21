import pytest

from api.operations import AddIngredientUnitOperation
from models.api_models import AddIngredientUnitRequest, IngredientUnitResponse, IngredientUnitSizeType
from models.ingredient.size_description import QualitativeDescription
from services.errors import ResourceNotFoundError
from tests.factories import (
    build_add_qualitative_ingredient_unit_request,
    build_add_ingredient_unit_request,
    build_add_ingredient_unit_size_type,
    build_add_qualitative_ingredient_unit_size_type,
    build_add_unit_without_size_type,
    build_generic_unit,
    build_generic_unit_service,
    build_ingredient,
    build_ingredient_service,
    build_ingredient_unit,
    build_ingredient_without_units,
    build_qualitative_ingredient_unit,
    build_size_generic_unit,
)


def test_add_ingredient_unit_validate_generic_unit_id() -> None:
    generic_unit = build_generic_unit()
    generic_unit_service = build_generic_unit_service()
    generic_unit_service.create_generic_unit(generic_unit)
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_ingredient_unit_size_type(),
        request=build_add_ingredient_unit_request(),
        ingredient_service=build_ingredient_service(),
        generic_unit_service=generic_unit_service,
    )

    validated_generic_unit = operation.validate_generic_unit_id()

    assert validated_generic_unit == generic_unit


def test_add_ingredient_unit_validate_generic_unit_id_not_found() -> None:
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_ingredient_unit_size_type(),
        request=build_add_ingredient_unit_request(),
        ingredient_service=build_ingredient_service(),
        generic_unit_service=build_generic_unit_service(),
    )

    with pytest.raises(ResourceNotFoundError, match="Generic unit 'bag' was not found."):
        operation.validate_generic_unit_id()


def test_add_ingredient_unit_build_size_description_requires_size_generic_unit() -> None:
    generic_unit_service = build_generic_unit_service()
    generic_unit_service.create_generic_unit(build_generic_unit())
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_ingredient_unit_size_type(),
        request=build_add_ingredient_unit_request(),
        ingredient_service=build_ingredient_service(),
        generic_unit_service=generic_unit_service,
    )

    with pytest.raises(ResourceNotFoundError, match="Generic unit 'lb' was not found."):
        operation.build_size_description()


def test_add_ingredient_unit_build_size_description_qualitative() -> None:
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_qualitative_ingredient_unit_size_type(),
        request=build_add_qualitative_ingredient_unit_request(),
        ingredient_service=build_ingredient_service(),
        generic_unit_service=build_generic_unit_service(),
    )

    assert operation.build_size_description() == QualitativeDescription(quality="large")


def test_add_ingredient_unit_build_size_description_none() -> None:
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_unit_without_size_type(),
        request=AddIngredientUnitRequest(generic_unit_id="bag", gram_weight=300.0),
        ingredient_service=build_ingredient_service(),
        generic_unit_service=build_generic_unit_service(),
    )

    assert operation.build_size_description() is None


def test_add_ingredient_unit_delegates_to_service() -> None:
    generic_unit = build_generic_unit()
    ingredient_unit = build_ingredient_unit(generic_unit=generic_unit)
    ingredient = build_ingredient(ingredient_unit=ingredient_unit)
    ingredient_service = build_ingredient_service()
    generic_unit_service = build_generic_unit_service()
    ingredient_service.create_ingredient(build_ingredient_without_units())
    generic_unit_service.create_generic_unit(generic_unit)
    generic_unit_service.create_generic_unit(build_size_generic_unit())
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_ingredient_unit_size_type(),
        request=build_add_ingredient_unit_request(),
        ingredient_service=ingredient_service,
        generic_unit_service=generic_unit_service,
    )

    update_result, added_ingredient_unit = operation.add_generic_unit_to_ingredient(
        generic_unit,
    )

    assert update_result.matched_count == 1
    assert added_ingredient_unit == ingredient_unit
    assert ingredient_service.get_ingredient_by_id("rice") == ingredient


def test_add_ingredient_unit_validate_response_state_requires_state() -> None:
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_ingredient_unit_size_type(),
        request=build_add_ingredient_unit_request(),
        ingredient_service=build_ingredient_service(),
        generic_unit_service=build_generic_unit_service(),
    )

    with pytest.raises(ValueError, match="ingredient and ingredient_unit must be set"):
        operation.validate_ingredient_unit_response_state()


def test_add_ingredient_unit_validate_response_state() -> None:
    ingredient = build_ingredient()
    ingredient_unit = build_ingredient_unit()
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_ingredient_unit_size_type(),
        request=build_add_ingredient_unit_request(),
        ingredient_service=build_ingredient_service(),
        generic_unit_service=build_generic_unit_service(),
    )
    operation.ingredient = ingredient
    operation.ingredient_unit = ingredient_unit

    assert operation.validate_ingredient_unit_response_state() == (ingredient, ingredient_unit)


def test_add_ingredient_unit_response_property() -> None:
    ingredient = build_ingredient()
    ingredient_unit = build_ingredient_unit()
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_ingredient_unit_size_type(),
        request=build_add_ingredient_unit_request(),
        ingredient_service=build_ingredient_service(),
        generic_unit_service=build_generic_unit_service(),
    )
    operation.ingredient = ingredient
    operation.ingredient_unit = ingredient_unit

    assert operation.response == IngredientUnitResponse(
        ingredient=ingredient,
        ingredient_unit=ingredient_unit,
    )


def test_add_ingredient_unit_execute() -> None:
    generic_unit = build_generic_unit()
    ingredient_unit = build_ingredient_unit(generic_unit=generic_unit)
    ingredient = build_ingredient(ingredient_unit=ingredient_unit)
    ingredient_service = build_ingredient_service()
    generic_unit_service = build_generic_unit_service()
    ingredient_service.create_ingredient(build_ingredient_without_units())
    generic_unit_service.create_generic_unit(generic_unit)
    generic_unit_service.create_generic_unit(build_size_generic_unit())
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_ingredient_unit_size_type(),
        request=build_add_ingredient_unit_request(),
        ingredient_service=ingredient_service,
        generic_unit_service=generic_unit_service,
    )

    response = operation.execute()

    assert response == IngredientUnitResponse(
        ingredient=ingredient,
        ingredient_unit=ingredient_unit,
    )
    assert operation.ingredient == ingredient
    assert operation.ingredient_unit == ingredient_unit
    assert operation.update_result is not None
    assert operation.update_result.matched_count == 1


def test_add_ingredient_unit_execute_qualitative() -> None:
    generic_unit = build_generic_unit()
    ingredient_unit = build_qualitative_ingredient_unit(generic_unit=generic_unit)
    ingredient = build_ingredient(ingredient_unit=ingredient_unit)
    ingredient_service = build_ingredient_service()
    generic_unit_service = build_generic_unit_service()
    ingredient_service.create_ingredient(build_ingredient_without_units())
    generic_unit_service.create_generic_unit(generic_unit)
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        size_type=build_add_qualitative_ingredient_unit_size_type(),
        request=build_add_qualitative_ingredient_unit_request(),
        ingredient_service=ingredient_service,
        generic_unit_service=generic_unit_service,
    )

    response = operation.execute()

    assert response == IngredientUnitResponse(
        ingredient=ingredient,
        ingredient_unit=ingredient_unit,
    )
