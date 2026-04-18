from models.api_models import AddIngredientUnitRequest, IngredientUnitResponse
from services.errors import ResourceNotFoundError
from services.generic_unit import GenericUnitService
from services.ingredient import IngredientService


class AddIngredientUnitOperation:
    def __init__(
        self,
        ingredient_service: IngredientService | None = None,
        generic_unit_service: GenericUnitService | None = None,
    ):
        self.ingredient_service = ingredient_service or IngredientService()
        self.generic_unit_service = generic_unit_service or GenericUnitService()

    def execute(
        self,
        ingredient_id: str,
        request: AddIngredientUnitRequest,
    ) -> IngredientUnitResponse:
        generic_unit = self.generic_unit_service.get_generic_unit_by_id(request.generic_unit_id)
        if generic_unit is None:
            raise ResourceNotFoundError(
                f"Generic unit '{request.generic_unit_id}' was not found.",
            )

        ingredient, ingredient_unit = self.ingredient_service.add_unit_to_ingredient(
            ingredient_id=ingredient_id,
            generic_unit=generic_unit,
            size=request.size,
            gram_weight=request.gram_weight,
        )
        return IngredientUnitResponse(
            ingredient=ingredient,
            ingredient_unit=ingredient_unit,
        )
