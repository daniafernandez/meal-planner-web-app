from api.operations.base import Operation
from models.api_models import CreateIngredientRequest, IngredientResponse
from models.ingredient.ingredient import Ingredient
from services.ingredient import IngredientService


class CreateIngredientOperation(Operation):
    def __init__(
        self,
        request: CreateIngredientRequest,
        ingredient_service: IngredientService | None = None,
    ):
        self.request = request
        self.ingredient_service = ingredient_service or IngredientService()
        self.ingredient: Ingredient | None = None
        self.created_ingredient: Ingredient | None = None

    def build_ingredient(self) -> Ingredient:
        return Ingredient(
            id=self.request.id,
            name=self.request.name,
            staple=self.request.staple,
        )

    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        return self.ingredient_service.create_ingredient(ingredient)

    @property
    def response(self) -> IngredientResponse:
        if self.created_ingredient is None:
            raise ValueError("created_ingredient must be set before building a response.")
        return IngredientResponse(ingredient=self.created_ingredient)

    def execute(self) -> IngredientResponse:
        self.ingredient = self.build_ingredient()
        self.created_ingredient = self.create_ingredient(self.ingredient)
        return self.response
