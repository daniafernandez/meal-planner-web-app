from models.api_models import CreateIngredientRequest, IngredientResponse
from models.ingredient.ingredient import Ingredient
from services.ingredient import IngredientService


class CreateIngredientOperation:
    def __init__(self, ingredient_service: IngredientService | None = None):
        self.ingredient_service = ingredient_service or IngredientService()

    def execute(self, request: CreateIngredientRequest) -> IngredientResponse:
        ingredient = Ingredient(
            id=request.id,
            name=request.name,
            staple=request.staple,
        )
        created_ingredient = self.ingredient_service.create_ingredient(ingredient)
        return IngredientResponse(ingredient=created_ingredient)
