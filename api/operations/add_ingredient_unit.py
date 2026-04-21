from api.operations.base import Operation
from models.generic_unit import GenericUnit
from models.api_models import (
    AddIngredientUnitRequest,
    IngredientUnitResponse,
    IngredientUnitSizeType,
)
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from models.ingredient.size_description import (
    QualitativeDescription,
    QuantitativeDescription,
    SizeDescription,
)
from services.errors import ResourceNotFoundError
from services.generic_unit import GenericUnitService
from services.ingredient import IngredientService
from services.project_model import UpdateResultProtocol


class AddIngredientUnitOperation(Operation):
    def __init__(
        self,
        ingredient_id: str,
        size_type: IngredientUnitSizeType,
        request: AddIngredientUnitRequest,
        ingredient_service: IngredientService | None = None,
        generic_unit_service: GenericUnitService | None = None,
    ):
        self.ingredient_id = ingredient_id
        self.size_type = size_type
        self.request = request
        self.ingredient_service = ingredient_service or IngredientService()
        self.generic_unit_service = generic_unit_service or GenericUnitService()
        self.ingredient: Ingredient | None = None
        self.ingredient_unit: IngredientUnit | None = None
        self.update_result: UpdateResultProtocol | None = None

    def validate_generic_unit_id(self) -> GenericUnit:
        return self.validate_generic_unit_exists(self.request.generic_unit_id)

    def validate_generic_unit_exists(self, generic_unit_id: str) -> GenericUnit:
        generic_unit = self.generic_unit_service.get_generic_unit_by_id(generic_unit_id)
        if generic_unit is None:
            raise ResourceNotFoundError(
                f"Generic unit '{generic_unit_id}' was not found.",
            )
        return generic_unit

    def build_size_description(self) -> SizeDescription | None:
        if self.size_type == IngredientUnitSizeType.NONE:
            return None

        if self.request.size is None:
            raise ValueError("size must be provided when size_type is not 'none'.")

        if self.size_type == IngredientUnitSizeType.QUALITATIVE:
            return QualitativeDescription(
                quality=self.request.size.quality,
            )

        return QuantitativeDescription(
            quantity=self.request.size.quantity,
            generic_unit=self.validate_generic_unit_exists(self.request.size.generic_unit_id),
        )

    def add_generic_unit_to_ingredient(
        self,
        generic_unit: GenericUnit,
    ) -> tuple[UpdateResultProtocol, IngredientUnit]:
        return self.ingredient_service.add_unit_to_ingredient(
            ingredient_id=self.ingredient_id,
            generic_unit=generic_unit,
            size=self.build_size_description(),
            gram_weight=self.request.gram_weight,
        )

    def validate_ingredient_unit_response_state(self) -> tuple[Ingredient, IngredientUnit]:
        if self.ingredient is None or self.ingredient_unit is None:
            raise ValueError(
                "ingredient and ingredient_unit must be set before building a response.",
            )
        return self.ingredient, self.ingredient_unit

    @property
    def response(self) -> IngredientUnitResponse:
        return IngredientUnitResponse(
            ingredient=self.ingredient,
            ingredient_unit=self.ingredient_unit,
        )

    def execute(self) -> IngredientUnitResponse:
        generic_unit = self.validate_generic_unit_id()
        self.update_result, self.ingredient_unit = self.add_generic_unit_to_ingredient(
            generic_unit=generic_unit,
        )
        self.ingredient = self.ingredient_service.get_ingredient_by_id(self.ingredient_id)
        self.validate_ingredient_unit_response_state()
        return self.response
