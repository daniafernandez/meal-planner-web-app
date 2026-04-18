from models.generic_unit import GenericUnit
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from services.errors import ResourceNotFoundError
from services.project_model import ProjectModelService


class IngredientService(ProjectModelService):
    collection_name = "ingredients"

    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        self.insert_one_item(ingredient)
        return ingredient

    def get_ingredient_by_id(self, ingredient_id: str) -> Ingredient | None:
        item = self.collection.find_one({"id": ingredient_id})
        if item is None:
            return None
        return Ingredient(**item)

    def add_unit_to_ingredient(
        self,
        ingredient_id: str,
        generic_unit: GenericUnit,
        size: str | None,
        gram_weight: float,
    ) -> tuple[Ingredient, IngredientUnit]:
        ingredient_unit = IngredientUnit(
            generic_unit=generic_unit,
            size=size,
            gram_weight=gram_weight,
        )
        result = self.collection.update_one(
            {"id": ingredient_id},
            {"$push": {"units": ingredient_unit.model_dump()}},
        )
        if result.matched_count == 0:
            raise ResourceNotFoundError(f"Ingredient '{ingredient_id}' was not found.")

        updated_ingredient = self.get_ingredient_by_id(ingredient_id)
        if updated_ingredient is None:
            raise ResourceNotFoundError(
                f"Ingredient '{ingredient_id}' was not found after update.",
            )

        return updated_ingredient, ingredient_unit
