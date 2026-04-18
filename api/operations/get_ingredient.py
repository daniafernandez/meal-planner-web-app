from models.api_models import IngredientResponse
from services.errors import ResourceNotFoundError
from services.ingredient import IngredientService


class GetIngredientOperation:
    def __init__(self, ingredient_service: IngredientService | None = None):
        self.ingredient_service = ingredient_service or IngredientService()

    def execute(self, ingredient_id: str) -> IngredientResponse:
        ingredient = self.ingredient_service.get_ingredient_by_id(ingredient_id)
        if ingredient is None:
            raise ResourceNotFoundError(f"Ingredient '{ingredient_id}' was not found.")

        return IngredientResponse(ingredient=ingredient)
