import pytest

from api.operations import (
    AddIngredientUnitOperation,
    CreateGenericUnitOperation,
    CreateIngredientOperation,
    GetIngredientOperation,
    HealthcheckOperation,
    Operation,
)
from models.api_models import GenericUnitResponse, IngredientResponse, IngredientUnitResponse
from models.generic_unit import GenericUnit
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from services.errors import ResourceNotFoundError


class StubGenericUnitService:
    def __init__(self, generic_unit: GenericUnit | None = None):
        self.generic_unit = generic_unit
        self.requested_id: str | None = None
        self.created_generic_unit: GenericUnit | None = None

    def get_generic_unit_by_id(self, generic_unit_id: str) -> GenericUnit | None:
        self.requested_id = generic_unit_id
        return self.generic_unit

    def create_generic_unit(self, generic_unit: GenericUnit) -> GenericUnit:
        self.created_generic_unit = generic_unit
        return generic_unit


class StubIngredientService:
    def __init__(
        self,
        ingredient: Ingredient | None = None,
        add_result: tuple[Ingredient, IngredientUnit] | None = None,
    ):
        self.ingredient = ingredient
        self.add_result = add_result
        self.created_ingredient: Ingredient | None = None
        self.requested_id: str | None = None
        self.add_call: dict[str, object] | None = None

    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        self.created_ingredient = ingredient
        return ingredient

    def get_ingredient_by_id(self, ingredient_id: str) -> Ingredient | None:
        self.requested_id = ingredient_id
        return self.ingredient

    def add_unit_to_ingredient(
        self,
        ingredient_id: str,
        generic_unit: GenericUnit,
        size: str | None,
        gram_weight: float,
    ) -> tuple[Ingredient, IngredientUnit]:
        self.add_call = {
            "ingredient_id": ingredient_id,
            "generic_unit": generic_unit,
            "size": size,
            "gram_weight": gram_weight,
        }
        if self.add_result is None:
            raise AssertionError("add_result must be configured for this test.")
        return self.add_result


def test_operation_base_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        Operation()


def test_healthcheck_operation_response_property() -> None:
    operation = HealthcheckOperation()

    assert operation.response == {"status": "ok"}


def test_healthcheck_operation_execute_returns_response() -> None:
    operation = HealthcheckOperation()

    assert operation.execute() == {"status": "ok"}


def test_create_generic_unit_build_generic_unit(create_generic_unit_request) -> None:
    operation = CreateGenericUnitOperation(
        request=create_generic_unit_request,
        generic_unit_service=StubGenericUnitService(),
    )

    assert operation.build_generic_unit() == GenericUnit(
        id="bag",
        name="bag",
        measurement_type=create_generic_unit_request.measurement_type,
    )


def test_create_generic_unit_delegates_to_service(generic_unit, create_generic_unit_request) -> None:
    generic_unit_service = StubGenericUnitService()
    operation = CreateGenericUnitOperation(
        request=create_generic_unit_request,
        generic_unit_service=generic_unit_service,
    )

    created_generic_unit = operation.create_generic_unit(generic_unit)

    assert created_generic_unit == generic_unit
    assert generic_unit_service.created_generic_unit == generic_unit


def test_create_generic_unit_validate_created_generic_unit_requires_created_unit(
    create_generic_unit_request,
) -> None:
    operation = CreateGenericUnitOperation(
        request=create_generic_unit_request,
        generic_unit_service=StubGenericUnitService(),
    )

    with pytest.raises(ValueError, match="created_generic_unit must be set"):
        operation.validate_created_generic_unit()


def test_create_generic_unit_validate_created_generic_unit(
    create_generic_unit_request,
    generic_unit,
) -> None:
    operation = CreateGenericUnitOperation(
        request=create_generic_unit_request,
        generic_unit_service=StubGenericUnitService(),
    )
    operation.created_generic_unit = generic_unit

    assert operation.validate_created_generic_unit() == generic_unit


def test_create_generic_unit_response_property(create_generic_unit_request, generic_unit) -> None:
    operation = CreateGenericUnitOperation(
        request=create_generic_unit_request,
        generic_unit_service=StubGenericUnitService(),
    )
    operation.created_generic_unit = generic_unit

    assert operation.response == GenericUnitResponse(generic_unit=generic_unit)


def test_create_generic_unit_execute(create_generic_unit_request) -> None:
    generic_unit_service = StubGenericUnitService()
    operation = CreateGenericUnitOperation(
        request=create_generic_unit_request,
        generic_unit_service=generic_unit_service,
    )

    response = operation.execute()

    assert response == GenericUnitResponse(generic_unit=generic_unit_service.created_generic_unit)
    assert operation.generic_unit == generic_unit_service.created_generic_unit
    assert operation.created_generic_unit == generic_unit_service.created_generic_unit


def test_create_ingredient_build_ingredient(create_ingredient_request) -> None:
    operation = CreateIngredientOperation(
        request=create_ingredient_request,
        ingredient_service=StubIngredientService(),
    )

    assert operation.build_ingredient() == Ingredient(
        id="rice",
        name="Rice",
        staple=True,
        units=[],
    )


def test_create_ingredient_delegates_to_service(ingredient, create_ingredient_request) -> None:
    ingredient_service = StubIngredientService()
    operation = CreateIngredientOperation(
        request=create_ingredient_request,
        ingredient_service=ingredient_service,
    )

    created_ingredient = operation.create_ingredient(ingredient)

    assert created_ingredient == ingredient
    assert ingredient_service.created_ingredient == ingredient


def test_create_ingredient_validate_created_ingredient_requires_created_ingredient(
    create_ingredient_request,
) -> None:
    operation = CreateIngredientOperation(
        request=create_ingredient_request,
        ingredient_service=StubIngredientService(),
    )

    with pytest.raises(ValueError, match="created_ingredient must be set"):
        operation.validate_created_ingredient()


def test_create_ingredient_validate_created_ingredient(
    create_ingredient_request,
    ingredient,
) -> None:
    operation = CreateIngredientOperation(
        request=create_ingredient_request,
        ingredient_service=StubIngredientService(),
    )
    operation.created_ingredient = ingredient

    assert operation.validate_created_ingredient() == ingredient


def test_create_ingredient_response_property(create_ingredient_request, ingredient) -> None:
    operation = CreateIngredientOperation(
        request=create_ingredient_request,
        ingredient_service=StubIngredientService(),
    )
    operation.created_ingredient = ingredient

    assert operation.response == IngredientResponse(ingredient=ingredient)


def test_create_ingredient_execute(create_ingredient_request) -> None:
    ingredient_service = StubIngredientService()
    operation = CreateIngredientOperation(
        request=create_ingredient_request,
        ingredient_service=ingredient_service,
    )

    response = operation.execute()

    assert response == IngredientResponse(ingredient=ingredient_service.created_ingredient)
    assert operation.ingredient == ingredient_service.created_ingredient
    assert operation.created_ingredient == ingredient_service.created_ingredient


def test_get_ingredient_validate_ingredient_id(ingredient) -> None:
    ingredient_service = StubIngredientService(ingredient=ingredient)
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=ingredient_service,
    )

    validated_ingredient = operation.validate_ingredient_id()

    assert validated_ingredient == ingredient
    assert ingredient_service.requested_id == "rice"


def test_get_ingredient_validate_ingredient_id_not_found() -> None:
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=StubIngredientService(ingredient=None),
    )

    with pytest.raises(ResourceNotFoundError, match="Ingredient 'rice' was not found."):
        operation.validate_ingredient_id()


def test_get_ingredient_validate_ingredient_requires_ingredient() -> None:
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=StubIngredientService(),
    )

    with pytest.raises(ValueError, match="ingredient must be set"):
        operation.validate_ingredient()


def test_get_ingredient_validate_ingredient(ingredient) -> None:
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=StubIngredientService(),
    )
    operation.ingredient = ingredient

    assert operation.validate_ingredient() == ingredient


def test_get_ingredient_response_property(ingredient) -> None:
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=StubIngredientService(),
    )
    operation.ingredient = ingredient

    assert operation.response == IngredientResponse(ingredient=ingredient)


def test_get_ingredient_execute(ingredient) -> None:
    operation = GetIngredientOperation(
        ingredient_id="rice",
        ingredient_service=StubIngredientService(ingredient=ingredient),
    )

    response = operation.execute()

    assert response == IngredientResponse(ingredient=ingredient)
    assert operation.ingredient == ingredient


def test_add_ingredient_unit_validate_generic_unit_id(generic_unit, add_ingredient_unit_request) -> None:
    generic_unit_service = StubGenericUnitService(generic_unit=generic_unit)
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        request=add_ingredient_unit_request,
        ingredient_service=StubIngredientService(),
        generic_unit_service=generic_unit_service,
    )

    validated_generic_unit = operation.validate_generic_unit_id()

    assert validated_generic_unit == generic_unit
    assert generic_unit_service.requested_id == "bag"


def test_add_ingredient_unit_validate_generic_unit_id_not_found(add_ingredient_unit_request) -> None:
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        request=add_ingredient_unit_request,
        ingredient_service=StubIngredientService(),
        generic_unit_service=StubGenericUnitService(generic_unit=None),
    )

    with pytest.raises(ResourceNotFoundError, match="Generic unit 'bag' was not found."):
        operation.validate_generic_unit_id()


def test_add_ingredient_unit_delegates_to_service(
    ingredient,
    ingredient_unit,
    generic_unit,
    add_ingredient_unit_request,
) -> None:
    ingredient_service = StubIngredientService(add_result=(ingredient, ingredient_unit))
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        request=add_ingredient_unit_request,
        ingredient_service=ingredient_service,
        generic_unit_service=StubGenericUnitService(generic_unit=generic_unit),
    )

    result = operation.add_generic_unit_to_ingredient(generic_unit)

    assert result == (ingredient, ingredient_unit)
    assert ingredient_service.add_call == {
        "ingredient_id": "rice",
        "generic_unit": generic_unit,
        "size": "5lb",
        "gram_weight": 2268.0,
    }


def test_add_ingredient_unit_validate_response_state_requires_state(
    add_ingredient_unit_request,
) -> None:
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        request=add_ingredient_unit_request,
        ingredient_service=StubIngredientService(),
        generic_unit_service=StubGenericUnitService(),
    )

    with pytest.raises(ValueError, match="ingredient and ingredient_unit must be set"):
        operation.validate_ingredient_unit_response_state()


def test_add_ingredient_unit_validate_response_state(
    ingredient,
    ingredient_unit,
    add_ingredient_unit_request,
) -> None:
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        request=add_ingredient_unit_request,
        ingredient_service=StubIngredientService(),
        generic_unit_service=StubGenericUnitService(),
    )
    operation.ingredient = ingredient
    operation.ingredient_unit = ingredient_unit

    assert operation.validate_ingredient_unit_response_state() == (ingredient, ingredient_unit)


def test_add_ingredient_unit_response_property(
    ingredient,
    ingredient_unit,
    add_ingredient_unit_request,
) -> None:
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        request=add_ingredient_unit_request,
        ingredient_service=StubIngredientService(),
        generic_unit_service=StubGenericUnitService(),
    )
    operation.ingredient = ingredient
    operation.ingredient_unit = ingredient_unit

    assert operation.response == IngredientUnitResponse(
        ingredient=ingredient,
        ingredient_unit=ingredient_unit,
    )


def test_add_ingredient_unit_execute(
    ingredient,
    ingredient_unit,
    generic_unit,
    add_ingredient_unit_request,
) -> None:
    operation = AddIngredientUnitOperation(
        ingredient_id="rice",
        request=add_ingredient_unit_request,
        ingredient_service=StubIngredientService(add_result=(ingredient, ingredient_unit)),
        generic_unit_service=StubGenericUnitService(generic_unit=generic_unit),
    )

    response = operation.execute()

    assert response == IngredientUnitResponse(
        ingredient=ingredient,
        ingredient_unit=ingredient_unit,
    )
    assert operation.ingredient == ingredient
    assert operation.ingredient_unit == ingredient_unit
