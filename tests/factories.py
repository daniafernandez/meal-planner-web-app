from models.api_models import (
    AddIngredientUnitRequest,
    AddQualitativeIngredientUnitSizeRequest,
    AddQuantitativeIngredientUnitSizeRequest,
    CreateGenericUnitRequest,
    CreateIngredientRequest,
    IngredientUnitSizeType,
)
from models.generic_unit import GenericUnit
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from models.ingredient.size_description import (
    QualitativeDescription,
    QuantitativeDescription,
    SizeDescription,
)
from models.recipe.recipe import Recipe
from models.recipe.recipe_ingredient import RecipeIngredient
from services.generic_unit import GenericUnitService
from services.ingredient import IngredientService
from services.recipe import RecipeService
from tests.in_memory_mongo import InMemoryMongoClient, MockMongoSettings


def build_generic_unit() -> GenericUnit:
    return GenericUnit(
        id="bag",
        name="bag",
    )


def build_size_generic_unit() -> GenericUnit:
    return GenericUnit(
        id="lb",
        name="lb",
    )


def build_create_generic_unit_request() -> CreateGenericUnitRequest:
    return CreateGenericUnitRequest(
        name="bag",
    )


def build_create_ingredient_request() -> CreateIngredientRequest:
    return CreateIngredientRequest(
        name="Rice",
        staple=True,
    )


def build_add_ingredient_unit_request() -> AddIngredientUnitRequest:
    return AddIngredientUnitRequest(
        generic_unit_id="bag",
        size=AddQuantitativeIngredientUnitSizeRequest(
            quantity=5,
            generic_unit_id="lb",
        ),
        gram_weight=2268.0,
    )


def build_add_qualitative_ingredient_unit_request() -> AddIngredientUnitRequest:
    return AddIngredientUnitRequest(
        generic_unit_id="bag",
        size=AddQualitativeIngredientUnitSizeRequest(
            quality="large",
        ),
        gram_weight=300.0,
    )


def build_add_ingredient_unit_size_type() -> IngredientUnitSizeType:
    return IngredientUnitSizeType.QUANTITATIVE


def build_add_qualitative_ingredient_unit_size_type() -> IngredientUnitSizeType:
    return IngredientUnitSizeType.QUALITATIVE


def build_add_unit_without_size_type() -> IngredientUnitSizeType:
    return IngredientUnitSizeType.NONE


def build_size_description(generic_unit: GenericUnit | None = None) -> SizeDescription:
    return QuantitativeDescription(
        quantity=5,
        generic_unit=generic_unit or build_size_generic_unit(),
    )


def build_qualitative_size_description() -> SizeDescription:
    return QualitativeDescription(
        quality="large",
    )


def build_ingredient_unit(
    generic_unit: GenericUnit | None = None,
    size: SizeDescription | None = None,
) -> IngredientUnit:
    return IngredientUnit(
        generic_unit=generic_unit or build_generic_unit(),
        size=size if size is not None else build_size_description(),
        gram_weight=2268.0,
    )


def build_qualitative_ingredient_unit(
    generic_unit: GenericUnit | None = None,
) -> IngredientUnit:
    return IngredientUnit(
        generic_unit=generic_unit or build_generic_unit(),
        size=build_qualitative_size_description(),
        gram_weight=300.0,
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


def build_recipe_ingredient(
    ingredient_line_string: str = "2 medium onions, sliced",
    active: bool = True,
) -> RecipeIngredient:
    return RecipeIngredient(
        ingredient_line_string=ingredient_line_string,
        active=active,
    )


def build_recipe(recipe_ingredient: RecipeIngredient | None = None) -> Recipe:
    return Recipe(
        id="fried-rice",
        name="Fried Rice",
        servings="4",
        ingredients=[recipe_ingredient or build_recipe_ingredient()],
    )


def build_recipe_without_ingredients() -> Recipe:
    return Recipe(
        id="fried-rice",
        name="Fried Rice",
        servings="4",
        ingredients=[],
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


def build_recipe_service() -> RecipeService:
    service = RecipeService(
        settings=MockMongoSettings(),
        client=InMemoryMongoClient(),
    )
    service.collection.create_index("id", unique=True)
    service.collection.create_index("name", unique=True)
    return service
