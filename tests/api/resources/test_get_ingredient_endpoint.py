from api.resources.endpoints import get_get_ingredient_operation
from models.api_models import IngredientResponse
from services.errors import ResourceNotFoundError
from tests.api.resources.endpoint_helpers import FakeOperation, build_client
from tests.factories import build_ingredient


def test_get_ingredient_endpoint_success() -> None:
    ingredient = build_ingredient()
    operation = FakeOperation(result=IngredientResponse(ingredient=ingredient))
    captured = {}

    def override(ingredient_id: str):
        captured["ingredient_id"] = ingredient_id
        return operation

    with build_client() as client:
        client.app.dependency_overrides[get_get_ingredient_operation] = override

        response = client.get("/ingredients/rice")

    assert response.status_code == 200
    assert response.json() == IngredientResponse(ingredient=ingredient).model_dump(mode="json")
    assert captured["ingredient_id"] == "rice"
    assert operation.executed is True


def test_get_ingredient_endpoint_translates_unexpected_errors_to_500() -> None:
    with build_client() as client:
        client.app.dependency_overrides[get_get_ingredient_operation] = lambda: FakeOperation(
            error=RuntimeError("boom"),
        )

        response = client.get("/ingredients/rice")

    assert response.status_code == 500
    assert response.json() == {"detail": "An unexpected error occurred."}


def test_get_ingredient_endpoint_translates_not_found_errors_to_404() -> None:
    detail = "Ingredient 'rice' was not found."

    with build_client() as client:
        client.app.dependency_overrides[get_get_ingredient_operation] = lambda: FakeOperation(
            error=ResourceNotFoundError(detail),
        )

        response = client.get("/ingredients/rice")

    assert response.status_code == 404
    assert response.json() == {"detail": detail}
