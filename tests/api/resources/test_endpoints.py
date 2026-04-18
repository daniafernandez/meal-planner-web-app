import pytest

from api.resources.endpoints import (
    get_add_ingredient_unit_operation,
    get_create_generic_unit_operation,
    get_create_ingredient_operation,
    get_get_ingredient_operation,
    get_healthcheck_operation,
)
from models.api_models import AddIngredientUnitRequest, CreateGenericUnitRequest, CreateIngredientRequest
from models.api_models import GenericUnitResponse, IngredientResponse, IngredientUnitResponse
from services.errors import DuplicateResourceError, ResourceNotFoundError


class FakeOperation:
    def __init__(self, result=None, error: Exception | None = None):
        self.result = result
        self.error = error
        self.executed = False

    def execute(self):
        self.executed = True
        if self.error is not None:
            raise self.error
        return self.result


def call_endpoint(client, method: str, path: str, payload: dict | None = None):
    if payload is None:
        return getattr(client, method)(path)
    return getattr(client, method)(path, json=payload)


def test_healthcheck_endpoint_success(client) -> None:
    operation = FakeOperation(result={"status": "ok"})

    client.app.dependency_overrides[get_healthcheck_operation] = lambda: operation

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert operation.executed is True


def test_create_generic_unit_endpoint_success(client, create_generic_unit_request, generic_unit) -> None:
    operation = FakeOperation(result=GenericUnitResponse(generic_unit=generic_unit))
    captured = {}

    def override(request: CreateGenericUnitRequest):
        captured["request"] = request
        return operation

    client.app.dependency_overrides[get_create_generic_unit_operation] = override

    response = client.post("/generic-units", json=create_generic_unit_request.model_dump(mode="json"))

    assert response.status_code == 201
    assert response.json() == GenericUnitResponse(generic_unit=generic_unit).model_dump(mode="json")
    assert captured["request"] == create_generic_unit_request
    assert operation.executed is True


def test_create_ingredient_endpoint_success(client, create_ingredient_request, ingredient) -> None:
    operation = FakeOperation(result=IngredientResponse(ingredient=ingredient))
    captured = {}

    def override(request: CreateIngredientRequest):
        captured["request"] = request
        return operation

    client.app.dependency_overrides[get_create_ingredient_operation] = override

    response = client.post("/ingredients", json=create_ingredient_request.model_dump(mode="json"))

    assert response.status_code == 201
    assert response.json() == IngredientResponse(ingredient=ingredient).model_dump(mode="json")
    assert captured["request"] == create_ingredient_request
    assert operation.executed is True


def test_get_ingredient_endpoint_success(client, ingredient) -> None:
    operation = FakeOperation(result=IngredientResponse(ingredient=ingredient))
    captured = {}

    def override(ingredient_id: str):
        captured["ingredient_id"] = ingredient_id
        return operation

    client.app.dependency_overrides[get_get_ingredient_operation] = override

    response = client.get("/ingredients/rice")

    assert response.status_code == 200
    assert response.json() == IngredientResponse(ingredient=ingredient).model_dump(mode="json")
    assert captured["ingredient_id"] == "rice"
    assert operation.executed is True


def test_add_ingredient_unit_endpoint_success(
    client,
    add_ingredient_unit_request,
    ingredient,
    ingredient_unit,
) -> None:
    operation = FakeOperation(
        result=IngredientUnitResponse(
            ingredient=ingredient,
            ingredient_unit=ingredient_unit,
        ),
    )
    captured = {}

    def override(ingredient_id: str, request: AddIngredientUnitRequest):
        captured["ingredient_id"] = ingredient_id
        captured["request"] = request
        return operation

    client.app.dependency_overrides[get_add_ingredient_unit_operation] = override

    response = client.post(
        "/ingredients/rice/units",
        json=add_ingredient_unit_request.model_dump(mode="json"),
    )

    assert response.status_code == 201
    assert response.json() == IngredientUnitResponse(
        ingredient=ingredient,
        ingredient_unit=ingredient_unit,
    ).model_dump(mode="json")
    assert captured["ingredient_id"] == "rice"
    assert captured["request"] == add_ingredient_unit_request
    assert operation.executed is True


@pytest.mark.parametrize(
    ("provider", "method", "path", "payload"),
    [
        (get_healthcheck_operation, "get", "/health", None),
        (
            get_create_generic_unit_operation,
            "post",
            "/generic-units",
            {"id": "bag", "name": "bag", "measurement_type": "COUNT"},
        ),
        (
            get_create_ingredient_operation,
            "post",
            "/ingredients",
            {"id": "rice", "name": "Rice", "staple": True},
        ),
        (get_get_ingredient_operation, "get", "/ingredients/rice", None),
        (
            get_add_ingredient_unit_operation,
            "post",
            "/ingredients/rice/units",
            {"generic_unit_id": "bag", "size": "5lb", "gram_weight": 2268.0},
        ),
    ],
)
def test_endpoints_translate_unexpected_errors_to_500(
    client,
    provider,
    method: str,
    path: str,
    payload: dict | None,
) -> None:
    client.app.dependency_overrides[provider] = lambda: FakeOperation(error=RuntimeError("boom"))

    response = call_endpoint(client, method, path, payload)

    assert response.status_code == 500
    assert response.json() == {"detail": "An unexpected error occurred."}


@pytest.mark.parametrize(
    ("provider", "method", "path", "payload"),
    [
        (
            get_create_generic_unit_operation,
            "post",
            "/generic-units",
            {"id": "bag", "name": "bag", "measurement_type": "COUNT"},
        ),
        (
            get_create_ingredient_operation,
            "post",
            "/ingredients",
            {"id": "rice", "name": "Rice", "staple": True},
        ),
    ],
)
def test_endpoints_translate_duplicate_resource_errors_to_409(
    client,
    provider,
    method: str,
    path: str,
    payload: dict,
) -> None:
    client.app.dependency_overrides[provider] = lambda: FakeOperation(
        error=DuplicateResourceError("duplicate"),
    )

    response = call_endpoint(client, method, path, payload)

    assert response.status_code == 409
    assert response.json() == {"detail": "duplicate"}


@pytest.mark.parametrize(
    ("provider", "method", "path", "payload", "detail"),
    [
        (
            get_get_ingredient_operation,
            "get",
            "/ingredients/rice",
            None,
            "Ingredient 'rice' was not found.",
        ),
        (
            get_add_ingredient_unit_operation,
            "post",
            "/ingredients/rice/units",
            {"generic_unit_id": "bag", "size": "5lb", "gram_weight": 2268.0},
            "Generic unit 'bag' was not found.",
        ),
    ],
)
def test_endpoints_translate_not_found_errors_to_404(
    client,
    provider,
    method: str,
    path: str,
    payload: dict | None,
    detail: str,
) -> None:
    client.app.dependency_overrides[provider] = lambda: FakeOperation(
        error=ResourceNotFoundError(detail),
    )

    response = call_endpoint(client, method, path, payload)

    assert response.status_code == 404
    assert response.json() == {"detail": detail}
