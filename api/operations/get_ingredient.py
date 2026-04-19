from models.ingredient.ingredient import Ingredient
from api.operations.base import Operation
from models.api_models import IngredientResponse
from services.errors import ResourceNotFoundError
from services.ingredient import IngredientService


class GetIngredientOperation(Operation):
    def __init__(
        self,
        ingredient_id: str,
        ingredient_service: IngredientService | None = None,
    ):
        self.ingredient_id = ingredient_id
        self.ingredient_service = ingredient_service or IngredientService()
        self.ingredient: Ingredient | None = None

    def validate_ingredient_id(self) -> Ingredient:
        ingredient = self.ingredient_service.get_ingredient_by_id(self.ingredient_id)
        if ingredient is None:
            raise ResourceNotFoundError(f"Ingredient '{self.ingredient_id}' was not found.")
        return ingredient

    def validate_ingredient(self) -> Ingredient:
        if self.ingredient is None:
            raise ValueError("ingredient must be set before building a response.")
        return self.ingredient

    @property
    def response(self) -> IngredientResponse:
        return IngredientResponse(ingredient=self.ingredient)

    def execute(self) -> IngredientResponse:
        self.ingredient = self.validate_ingredient_id()
        self.validate_ingredient()
        return self.response
