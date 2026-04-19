from models.api_models import (
    AddIngredientUnitRequest,
    CreateGenericUnitRequest,
    CreateIngredientRequest,
)
from models.generic_unit import GenericUnit, MeasurementType
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from services.generic_unit import GenericUnitService
from services.ingredient import IngredientService
from tests.in_memory_mongo import InMemoryMongoClient, MockMongoSettings


def build_generic_unit() -> GenericUnit:
    return GenericUnit(
        id="bag",
        name="bag",
        measurement_type=MeasurementType.COUNT,
    )


def build_create_generic_unit_request() -> CreateGenericUnitRequest:
    return CreateGenericUnitRequest(
        name="bag",
        measurement_type=MeasurementType.COUNT,
    )


def build_create_ingredient_request() -> CreateIngredientRequest:
    return CreateIngredientRequest(
        name="Rice",
        staple=True,
    )


def build_add_ingredient_unit_request() -> AddIngredientUnitRequest:
    return AddIngredientUnitRequest(
        generic_unit_id="bag",
        size="5lb",
        gram_weight=2268.0,
    )


def build_ingredient_unit(generic_unit: GenericUnit | None = None) -> IngredientUnit:
    return IngredientUnit(
        generic_unit=generic_unit or build_generic_unit(),
        size="5lb",
        gram_weight=2268.0,
    )


def build_ingredient(ingredient_unit: IngredientUnit | None = None) -> Ingredient:
    return Ingredient(
        id="rice",
        name="Rice",
        staple=True,
        units=[ingredient_unit or build_ingredient_unit()],
    )


def build_ingredient_without_units() -> Ingredient:
    return Ingredient(
        id="rice",
        name="Rice",
        staple=True,
        units=[],
    )


def build_generic_unit_service() -> GenericUnitService:
    service = GenericUnitService(
        settings=MockMongoSettings(),
        client=InMemoryMongoClient(),
    )
    service.collection.create_index("id", unique=True)
    service.collection.create_index("name", unique=True)
    return service


def build_ingredient_service() -> IngredientService:
    service = IngredientService(
        settings=MockMongoSettings(),
        client=InMemoryMongoClient(),
    )
    service.collection.create_index("id", unique=True)
    service.collection.create_index("name", unique=True)
    return service
