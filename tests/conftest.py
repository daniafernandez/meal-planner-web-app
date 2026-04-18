import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.resources.endpoints import router
from models.api_models import (
    AddIngredientUnitRequest,
    CreateGenericUnitRequest,
    CreateIngredientRequest,
)
from models.generic_unit import GenericUnit, MeasurementType
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit


@pytest.fixture
def generic_unit() -> GenericUnit:
    return GenericUnit(
        id="bag",
        name="bag",
        measurement_type=MeasurementType.COUNT,
    )


@pytest.fixture
def create_generic_unit_request() -> CreateGenericUnitRequest:
    return CreateGenericUnitRequest(
        id="bag",
        name="bag",
        measurement_type=MeasurementType.COUNT,
    )


@pytest.fixture
def create_ingredient_request() -> CreateIngredientRequest:
    return CreateIngredientRequest(
        id="rice",
        name="Rice",
        staple=True,
    )


@pytest.fixture
def add_ingredient_unit_request() -> AddIngredientUnitRequest:
    return AddIngredientUnitRequest(
        generic_unit_id="bag",
        size="5lb",
        gram_weight=2268.0,
    )


@pytest.fixture
def ingredient_unit(generic_unit: GenericUnit) -> IngredientUnit:
    return IngredientUnit(
        generic_unit=generic_unit,
        size="5lb",
        gram_weight=2268.0,
    )


@pytest.fixture
def ingredient(ingredient_unit: IngredientUnit) -> Ingredient:
    return Ingredient(
        id="rice",
        name="Rice",
        staple=True,
        units=[ingredient_unit],
    )


@pytest.fixture
def endpoint_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(endpoint_app: FastAPI) -> TestClient:
    with TestClient(endpoint_app) as test_client:
        yield test_client
    endpoint_app.dependency_overrides.clear()
