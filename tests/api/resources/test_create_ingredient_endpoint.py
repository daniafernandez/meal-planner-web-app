from api.resources.endpoints import get_create_ingredient_operation
from models.api_models import CreateIngredientRequest, IngredientResponse
from services.errors import DuplicateResourceError
from tests.api.resources.endpoint_helpers import FakeOperation, build_client
from tests.factories import build_create_ingredient_request, build_ingredient


def test_create_ingredient_endpoint_success() -> None:
    request = build_create_ingredient_request()
    ingredient = build_ingredient()
    operation = FakeOperation(result=IngredientResponse(ingredient=ingredient))
    captured = {}

    def override(request: CreateIngredientRequest):
        captured["request"] = request
        return operation

    with build_client() as client:
        client.app.dependency_overrides[get_create_ingredient_operation] = override

        response = client.post("/ingredients", json=request.model_dump(mode="json"))

    assert response.status_code == 201
    assert response.json() == IngredientResponse(ingredient=ingredient).model_dump(mode="json")
    assert captured["request"] == request
    assert operation.executed is True


def test_create_ingredient_endpoint_translates_unexpected_errors_to_500() -> None:
    with build_client() as client:
        client.app.dependency_overrides[get_create_ingredient_operation] = lambda: FakeOperation(
            error=RuntimeError("boom"),
        )

        response = client.post(
            "/ingredients",
            json={"name": "Rice", "staple": True},
        )

    assert response.status_code == 500
    assert response.json() == {"detail": "An unexpected error occurred."}


def test_create_ingredient_endpoint_translates_duplicate_resource_errors_to_409() -> None:
    with build_client() as client:
        client.app.dependency_overrides[get_create_ingredient_operation] = lambda: FakeOperation(
            error=DuplicateResourceError("duplicate"),
        )

        response = client.post(
            "/ingredients",
            json={"name": "Rice", "staple": True},
        )

    assert response.status_code == 409
    assert response.json() == {"detail": "duplicate"}
