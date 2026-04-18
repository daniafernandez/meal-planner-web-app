from fastapi import APIRouter, HTTPException, status

from models.api_models import (
    AddIngredientUnitRequest,
    CreateGenericUnitRequest,
    CreateIngredientRequest,
    GenericUnitResponse,
    IngredientResponse,
    IngredientUnitResponse,
)
from models.generic_unit import GenericUnit
from models.ingredient.ingredient import Ingredient
from services.errors import DuplicateResourceError
from services.generic_unit import GenericUnitService
from services.ingredient import IngredientService


router = APIRouter()

ingredient_service = IngredientService()
generic_unit_service = GenericUnitService()


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/generic-units",
    response_model=GenericUnitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_generic_unit(request: CreateGenericUnitRequest) -> GenericUnitResponse:
    generic_unit = GenericUnit(
        id=request.id,
        name=request.name,
        measurement_type=request.measurement_type,
    )
    try:
        created_generic_unit = generic_unit_service.create_generic_unit(generic_unit)
    except DuplicateResourceError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return GenericUnitResponse(generic_unit=created_generic_unit)


@router.post(
    "/ingredients",
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ingredient(request: CreateIngredientRequest) -> IngredientResponse:
    ingredient = Ingredient(
        id=request.id,
        name=request.name,
        staple=request.staple,
    )
    try:
        created_ingredient = ingredient_service.create_ingredient(ingredient)
    except DuplicateResourceError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return IngredientResponse(ingredient=created_ingredient)


@router.get(
    "/ingredients/{ingredient_id}",
    response_model=IngredientResponse,
)
def get_ingredient(ingredient_id: str) -> IngredientResponse:
    ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient '{ingredient_id}' was not found.",
        )

    return IngredientResponse(ingredient=ingredient)


@router.post(
    "/ingredients/{ingredient_id}/units",
    response_model=IngredientUnitResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_ingredient_unit(
    ingredient_id: str,
    request: AddIngredientUnitRequest,
) -> IngredientUnitResponse:
    generic_unit = generic_unit_service.get_generic_unit_by_id(request.generic_unit_id)
    if generic_unit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Generic unit '{request.generic_unit_id}' was not found.",
        )

    try:
        ingredient, ingredient_unit = ingredient_service.add_unit_to_ingredient(
            ingredient_id=ingredient_id,
            generic_unit=generic_unit,
            size=request.size,
            gram_weight=request.gram_weight,
        )
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return IngredientUnitResponse(
        ingredient=ingredient,
        ingredient_unit=ingredient_unit,
    )
