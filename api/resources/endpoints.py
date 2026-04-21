import logging
from typing import Annotated, NoReturn

from fastapi import APIRouter, Depends, HTTPException, status

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
    IngredientUnitSizeType,
    CreateIngredientRequest,
    GenericUnitResponse,
)
from services.errors import DuplicateResourceError, ResourceNotFoundError


router = APIRouter()
logger = logging.getLogger(__name__)


def get_healthcheck_operation() -> HealthcheckOperation:
    return HealthcheckOperation()


def get_create_generic_unit_operation(
    request: CreateGenericUnitRequest,
) -> CreateGenericUnitOperation:
    return CreateGenericUnitOperation(request=request)


def get_create_ingredient_operation(
    request: CreateIngredientRequest,
) -> CreateIngredientOperation:
    return CreateIngredientOperation(request=request)


def get_get_ingredient_operation(ingredient_id: str) -> GetIngredientOperation:
    return GetIngredientOperation(ingredient_id=ingredient_id)


def get_add_ingredient_unit_operation(
    ingredient_id: str,
    size_type: IngredientUnitSizeType,
    request: AddIngredientUnitRequest,
) -> AddIngredientUnitOperation:
    return AddIngredientUnitOperation(
        ingredient_id=ingredient_id,
        size_type=size_type,
        request=request,
    )


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
def healthcheck(
    operation: Annotated[HealthcheckOperation, Depends(get_healthcheck_operation)],
) -> dict[str, str]:
    try:
        return operation.execute()
    except Exception as error:
        _handle_operation_error(error)


@router.post(
    "/generic-units",
    response_model=GenericUnitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_generic_unit(
    operation: Annotated[
        CreateGenericUnitOperation,
        Depends(get_create_generic_unit_operation),
    ],
) -> GenericUnitResponse:
    try:
        return operation.execute()
    except Exception as error:
        _handle_operation_error(error)


@router.post(
    "/ingredients",
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ingredient(
    operation: Annotated[
        CreateIngredientOperation,
        Depends(get_create_ingredient_operation),
    ],
) -> IngredientResponse:
    try:
        return operation.execute()
    except Exception as error:
        _handle_operation_error(error)


@router.get(
    "/ingredients/{ingredient_id}",
    response_model=IngredientResponse,
)
def get_ingredient(
    operation: Annotated[
        GetIngredientOperation,
        Depends(get_get_ingredient_operation),
    ],
) -> IngredientResponse:
    try:
        return operation.execute()
    except Exception as error:
        _handle_operation_error(error)


@router.post(
    "/ingredients/{ingredient_id}/units/{size_type}",
    response_model=IngredientUnitResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_ingredient_unit(
    operation: Annotated[
        AddIngredientUnitOperation,
        Depends(get_add_ingredient_unit_operation),
    ],
) -> IngredientUnitResponse:
    try:
        return operation.execute()
    except Exception as error:
        _handle_operation_error(error)
