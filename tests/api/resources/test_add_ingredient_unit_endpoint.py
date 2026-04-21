from api.resources.endpoints import get_add_ingredient_unit_operation
from models.api_models import AddIngredientUnitRequest, IngredientUnitResponse
from services.errors import ResourceNotFoundError
from tests.api.resources.endpoint_helpers import FakeOperation, build_client
from tests.factories import (
    build_add_qualitative_ingredient_unit_request,
    build_add_ingredient_unit_request,
    build_add_ingredient_unit_size_type,
    build_add_qualitative_ingredient_unit_size_type,
    build_ingredient,
    build_ingredient_unit,
    build_qualitative_ingredient_unit,
)


def test_add_ingredient_unit_endpoint_success() -> None:
    request = build_add_ingredient_unit_request()
    ingredient_unit = build_ingredient_unit()
    ingredient = build_ingredient(ingredient_unit=ingredient_unit)
    operation = FakeOperation(
        result=IngredientUnitResponse(
            ingredient=ingredient,
            ingredient_unit=ingredient_unit,
        ),
    )
    captured = {}

    def override(ingredient_id: str, size_type: str, request: AddIngredientUnitRequest):
        captured["ingredient_id"] = ingredient_id
        captured["size_type"] = size_type
        captured["request"] = request
        return operation

    with build_client() as client:
        client.app.dependency_overrides[get_add_ingredient_unit_operation] = override

        response = client.post(
            "/ingredients/rice/units/quantitative",
            json=request.model_dump(mode="json"),
        )

    assert response.status_code == 201
    assert response.json() == IngredientUnitResponse(
        ingredient=ingredient,
        ingredient_unit=ingredient_unit,
    ).model_dump(mode="json")
    assert captured["ingredient_id"] == "rice"
    assert captured["size_type"] == build_add_ingredient_unit_size_type()
    assert captured["request"] == request
    assert operation.executed is True


def test_add_ingredient_unit_endpoint_translates_unexpected_errors_to_500() -> None:
    with build_client() as client:
        client.app.dependency_overrides[get_add_ingredient_unit_operation] = lambda: FakeOperation(
            error=RuntimeError("boom"),
        )

        response = client.post(
            "/ingredients/rice/units/quantitative",
            json={
                "generic_unit_id": "bag",
                "size": {
                    "quantity": 5,
                    "generic_unit_id": "lb",
                },
                "gram_weight": 2268.0,
            },
        )

    assert response.status_code == 500
    assert response.json() == {"detail": "An unexpected error occurred."}


def test_add_ingredient_unit_endpoint_translates_not_found_errors_to_404() -> None:
    detail = "Generic unit 'bag' was not found."

    with build_client() as client:
        client.app.dependency_overrides[get_add_ingredient_unit_operation] = lambda: FakeOperation(
            error=ResourceNotFoundError(detail),
        )

        response = client.post(
            "/ingredients/rice/units/quantitative",
            json={
                "generic_unit_id": "bag",
                "size": {
                    "quantity": 5,
                    "generic_unit_id": "lb",
                },
                "gram_weight": 2268.0,
            },
        )

    assert response.status_code == 404
    assert response.json() == {"detail": detail}


def test_add_ingredient_unit_endpoint_success_qualitative() -> None:
    request = build_add_qualitative_ingredient_unit_request()
    ingredient_unit = build_qualitative_ingredient_unit()
    ingredient = build_ingredient(ingredient_unit=ingredient_unit)
    operation = FakeOperation(
        result=IngredientUnitResponse(
            ingredient=ingredient,
            ingredient_unit=ingredient_unit,
        ),
    )
    captured = {}

    def override(ingredient_id: str, size_type: str, request: AddIngredientUnitRequest):
        captured["ingredient_id"] = ingredient_id
        captured["size_type"] = size_type
        captured["request"] = request
        return operation

    with build_client() as client:
        client.app.dependency_overrides[get_add_ingredient_unit_operation] = override

        response = client.post(
            "/ingredients/rice/units/qualitative",
            json=request.model_dump(mode="json"),
        )

    assert response.status_code == 201
    assert response.json() == IngredientUnitResponse(
        ingredient=ingredient,
        ingredient_unit=ingredient_unit,
    ).model_dump(mode="json")
    assert captured["ingredient_id"] == "rice"
    assert captured["size_type"] == build_add_qualitative_ingredient_unit_size_type()
    assert captured["request"] == request
