from api.operations.base import Operation
from models.generic_unit import GenericUnit
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from models.api_models import AddIngredientUnitRequest, IngredientUnitResponse
from services.errors import ResourceNotFoundError
from services.generic_unit import GenericUnitService
from services.ingredient import IngredientService


class AddIngredientUnitOperation(Operation):
    def __init__(
        self,
        ingredient_id: str,
        request: AddIngredientUnitRequest,
        ingredient_service: IngredientService | None = None,
        generic_unit_service: GenericUnitService | None = None,
    ):
        self.ingredient_id = ingredient_id
        self.request = request
        self.ingredient_service = ingredient_service or IngredientService()
        self.generic_unit_service = generic_unit_service or GenericUnitService()
        self.ingredient: Ingredient | None = None
        self.ingredient_unit: IngredientUnit | None = None

    def validate_generic_unit_id(self) -> GenericUnit:
        generic_unit = self.generic_unit_service.get_generic_unit_by_id(self.request.generic_unit_id)
        if generic_unit is None:
            raise ResourceNotFoundError(
                f"Generic unit '{self.request.generic_unit_id}' was not found.",
            )
        return generic_unit

    def add_generic_unit_to_ingredient(
        self,
        generic_unit: GenericUnit,
    ) -> tuple[Ingredient, IngredientUnit]:
        return self.ingredient_service.add_unit_to_ingredient(
            ingredient_id=self.ingredient_id,
            generic_unit=generic_unit,
            size=self.request.size,
            gram_weight=self.request.gram_weight,
        )

    @property
    def response(self) -> IngredientUnitResponse:
        if self.ingredient is None or self.ingredient_unit is None:
            raise ValueError(
                "ingredient and ingredient_unit must be set before building a response.",
            )
        return IngredientUnitResponse(
            ingredient=self.ingredient,
            ingredient_unit=self.ingredient_unit,
        )

    def execute(self) -> IngredientUnitResponse:
        generic_unit = self.validate_generic_unit_id()
        self.ingredient, self.ingredient_unit = self.add_generic_unit_to_ingredient(
            generic_unit=generic_unit,
        )
        return self.response
