import logging
from typing import NoReturn

from fastapi import APIRouter, HTTPException, status

from api.operations import (
    AddIngredientUnitOperation,
    CreateGenericUnitOperation,
    CreateIngredientOperation,
    GetIngredientOperation,
    HealthcheckOperation,
)
from models.api_models import (
    AddIngredientUnitRequest,
    CreateGenericUnitRequest,
    IngredientResponse,
    IngredientUnitResponse,
    CreateIngredientRequest,
    GenericUnitResponse,
)
from services.errors import DuplicateResourceError, ResourceNotFoundError


router = APIRouter()
logger = logging.getLogger(__name__)


def _handle_operation_error(error: Exception) -> NoReturn:
    if isinstance(error, DuplicateResourceError):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    if isinstance(error, ResourceNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    logger.exception("Unhandled endpoint error")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred.",
    ) from error


@router.get("/health")
def healthcheck() -> dict[str, str]:
    try:
        return HealthcheckOperation().execute()
    except Exception as error:
        _handle_operation_error(error)


@router.post(
    "/generic-units",
    response_model=GenericUnitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_generic_unit(request: CreateGenericUnitRequest) -> GenericUnitResponse:
    try:
        return CreateGenericUnitOperation(request=request).execute()
    except Exception as error:
        _handle_operation_error(error)


@router.post(
    "/ingredients",
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ingredient(request: CreateIngredientRequest) -> IngredientResponse:
    try:
        return CreateIngredientOperation(request=request).execute()
    except Exception as error:
        _handle_operation_error(error)


@router.get(
    "/ingredients/{ingredient_id}",
    response_model=IngredientResponse,
)
def get_ingredient(ingredient_id: str) -> IngredientResponse:
    try:
        return GetIngredientOperation(ingredient_id=ingredient_id).execute()
    except Exception as error:
        _handle_operation_error(error)


@router.post(
    "/ingredients/{ingredient_id}/units",
    response_model=IngredientUnitResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_ingredient_unit(
    ingredient_id: str,
    request: AddIngredientUnitRequest,
) -> IngredientUnitResponse:
    try:
        return AddIngredientUnitOperation(
            ingredient_id=ingredient_id,
            request=request,
        ).execute()
    except Exception as error:
        _handle_operation_error(error)
