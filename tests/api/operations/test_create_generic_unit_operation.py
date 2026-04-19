import pytest

from api.operations import CreateGenericUnitOperation
from models.api_models import GenericUnitResponse
from models.generic_unit import GenericUnit
from tests.factories import (
    build_create_generic_unit_request,
    build_generic_unit,
    build_generic_unit_service,
)


def test_create_generic_unit_build_generic_unit() -> None:
    request = build_create_generic_unit_request()
    operation = CreateGenericUnitOperation(
        request=request,
        generic_unit_service=build_generic_unit_service(),
    )

    assert operation.build_generic_unit() == GenericUnit(
        id="bag",
        name="bag",
        measurement_type=request.measurement_type,
    )


def test_create_generic_unit_delegates_to_service() -> None:
    generic_unit = build_generic_unit()
    generic_unit_service = build_generic_unit_service()
    operation = CreateGenericUnitOperation(
        request=build_create_generic_unit_request(),
        generic_unit_service=generic_unit_service,
    )

    created_generic_unit = operation.create_generic_unit(generic_unit)

    assert created_generic_unit == generic_unit
    assert generic_unit_service.get_generic_unit_by_id(generic_unit.id) == generic_unit


def test_create_generic_unit_validate_created_generic_unit_requires_created_unit() -> None:
    operation = CreateGenericUnitOperation(
        request=build_create_generic_unit_request(),
        generic_unit_service=build_generic_unit_service(),
    )

    with pytest.raises(ValueError, match="created_generic_unit must be set"):
        operation.validate_created_generic_unit()


def test_create_generic_unit_validate_created_generic_unit() -> None:
    generic_unit = build_generic_unit()
    operation = CreateGenericUnitOperation(
        request=build_create_generic_unit_request(),
        generic_unit_service=build_generic_unit_service(),
    )
    operation.created_generic_unit = generic_unit

    assert operation.validate_created_generic_unit() == generic_unit


def test_create_generic_unit_response_property() -> None:
    generic_unit = build_generic_unit()
    operation = CreateGenericUnitOperation(
        request=build_create_generic_unit_request(),
        generic_unit_service=build_generic_unit_service(),
    )
    operation.created_generic_unit = generic_unit

    assert operation.response == GenericUnitResponse(generic_unit=generic_unit)


def test_create_generic_unit_execute() -> None:
    generic_unit_service = build_generic_unit_service()
    operation = CreateGenericUnitOperation(
        request=build_create_generic_unit_request(),
        generic_unit_service=generic_unit_service,
    )

    response = operation.execute()
    created_generic_unit = generic_unit_service.get_generic_unit_by_id("bag")

    assert response == GenericUnitResponse(generic_unit=created_generic_unit)
    assert operation.generic_unit == created_generic_unit
    assert operation.created_generic_unit == created_generic_unit
