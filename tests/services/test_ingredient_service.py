import pytest

from services.errors import DuplicateResourceError
from tests.factories import (
    build_generic_unit,
    build_ingredient,
    build_ingredient_service,
    build_ingredient_unit,
    build_ingredient_without_units,
    build_qualitative_ingredient_unit,
    build_qualitative_size_description,
    build_size_description,
)


def test_ingredient_service_push_ingredient_unit() -> None:
    service = build_ingredient_service()
    ingredient = build_ingredient_without_units()
    ingredient_unit = build_ingredient_unit()
    service.create_ingredient(ingredient)

    update_result = service.push_ingredient_unit(
        ingredient_id=ingredient.id,
        ingredient_unit=ingredient_unit,
    )

    assert update_result.matched_count == 1


def test_ingredient_service_add_unit_to_ingredient_returns_update_result() -> None:
    service = build_ingredient_service()
    generic_unit = build_generic_unit()
    size = build_size_description()
    service.create_ingredient(build_ingredient_without_units())

    update_result, ingredient_unit = service.add_unit_to_ingredient(
        ingredient_id="rice",
        generic_unit=generic_unit,
        size=size,
        gram_weight=2268.0,
    )

    assert update_result.matched_count == 1


def test_ingredient_service_add_unit_to_ingredient_adds_unit() -> None:
    service = build_ingredient_service()
    generic_unit = build_generic_unit()
    size = build_size_description()
    service.create_ingredient(build_ingredient_without_units())

    _, ingredient_unit = service.add_unit_to_ingredient(
        ingredient_id="rice",
        generic_unit=generic_unit,
        size=size,
        gram_weight=2268.0,
    )

    assert service.get_ingredient_by_id("rice") == build_ingredient(
        ingredient_unit=ingredient_unit,
    )


def test_ingredient_service_rejects_duplicate_unit_with_different_gram_weight() -> None:
    service = build_ingredient_service()
    existing_unit = build_ingredient_unit()
    service.create_ingredient(build_ingredient(ingredient_unit=existing_unit))

    with pytest.raises(
        DuplicateResourceError,
        match="Ingredient 'rice' already has unit '5 lb bag'.",
    ):
        service.add_unit_to_ingredient(
            ingredient_id="rice",
            generic_unit=existing_unit.generic_unit,
            size=existing_unit.size,
            gram_weight=2300.0,
        )


def test_ingredient_service_does_not_insert_duplicate_unit_with_different_gram_weight() -> None:
    service = build_ingredient_service()
    existing_unit = build_ingredient_unit()
    ingredient = build_ingredient(ingredient_unit=existing_unit)
    service.create_ingredient(ingredient)

    with pytest.raises(DuplicateResourceError):
        service.add_unit_to_ingredient(
            ingredient_id="rice",
            generic_unit=existing_unit.generic_unit,
            size=existing_unit.size,
            gram_weight=2300.0,
        )

    assert service.get_ingredient_by_id("rice") == ingredient


def test_ingredient_service_rejects_duplicate_qualitative_unit_with_different_gram_weight() -> None:
    service = build_ingredient_service()
    existing_unit = build_qualitative_ingredient_unit()
    service.create_ingredient(build_ingredient(ingredient_unit=existing_unit))

    with pytest.raises(
        DuplicateResourceError,
        match="Ingredient 'rice' already has unit 'large bag'.",
    ):
        service.add_unit_to_ingredient(
            ingredient_id="rice",
            generic_unit=existing_unit.generic_unit,
            size=build_qualitative_size_description(),
            gram_weight=305.0,
        )
