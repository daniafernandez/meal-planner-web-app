from api.resources.endpoints import get_create_generic_unit_operation
from models.api_models import CreateGenericUnitRequest, GenericUnitResponse
from services.errors import DuplicateResourceError
from tests.api.resources.endpoint_helpers import FakeOperation, build_client
from tests.factories import build_create_generic_unit_request, build_generic_unit


def test_create_generic_unit_endpoint_success() -> None:
    request = build_create_generic_unit_request()
    generic_unit = build_generic_unit()
    operation = FakeOperation(result=GenericUnitResponse(generic_unit=generic_unit))
    captured = {}

    def override(request: CreateGenericUnitRequest):
        captured["request"] = request
        return operation

    with build_client() as client:
        client.app.dependency_overrides[get_create_generic_unit_operation] = override

        response = client.post("/generic-units", json=request.model_dump(mode="json"))

    assert response.status_code == 201
    assert response.json() == GenericUnitResponse(generic_unit=generic_unit).model_dump(mode="json")
    assert captured["request"] == request
    assert operation.executed is True


def test_create_generic_unit_endpoint_translates_unexpected_errors_to_500() -> None:
    with build_client() as client:
        client.app.dependency_overrides[get_create_generic_unit_operation] = lambda: FakeOperation(
            error=RuntimeError("boom"),
        )

        response = client.post(
            "/generic-units",
            json={"name": "bag", "measurement_type": "COUNT"},
        )

    assert response.status_code == 500
    assert response.json() == {"detail": "An unexpected error occurred."}


def test_create_generic_unit_endpoint_translates_duplicate_resource_errors_to_409() -> None:
    with build_client() as client:
        client.app.dependency_overrides[get_create_generic_unit_operation] = lambda: FakeOperation(
            error=DuplicateResourceError("duplicate"),
        )

        response = client.post(
            "/generic-units",
            json={"name": "bag", "measurement_type": "COUNT"},
        )

    assert response.status_code == 409
    assert response.json() == {"detail": "duplicate"}
