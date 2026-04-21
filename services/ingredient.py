from models.generic_unit import GenericUnit
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from models.ingredient.size_description import SizeDescription
from services.errors import DuplicateResourceError
from services.project_model import ProjectModelService, UpdateResultProtocol


class IngredientService(ProjectModelService):
    collection_name = "ingredients"

    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        self.validate_unique_field("name", ingredient.name)
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
        size: SizeDescription | None,
        gram_weight: float,
    ) -> tuple[UpdateResultProtocol, IngredientUnit]:
        ingredient_unit = IngredientUnit(
            generic_unit=generic_unit,
            size=size,
            gram_weight=gram_weight,
        )
        self.validate_ingredient_unit_is_unique(ingredient_id, ingredient_unit)
        update_result = self.push_ingredient_unit(
            ingredient_id=ingredient_id,
            ingredient_unit=ingredient_unit,
        )
        return update_result, ingredient_unit

    def validate_ingredient_unit_is_unique(
        self,
        ingredient_id: str,
        ingredient_unit: IngredientUnit,
    ) -> None:
        ingredient = self.get_ingredient_by_id(ingredient_id)
        if ingredient is None:
            return

        for existing_unit in ingredient.units:
            if (
                existing_unit.generic_unit.id == ingredient_unit.generic_unit.id
                and self.sizes_match(existing_unit.size, ingredient_unit.size)
            ):
                raise DuplicateResourceError(
                    f"Ingredient '{ingredient_id}' already has unit '{ingredient_unit.name}'.",
                )

    @staticmethod
    def sizes_match(
        existing_size: SizeDescription | None,
        new_size: SizeDescription | None,
    ) -> bool:
        if existing_size is None and new_size is None:
            return True
        if existing_size is None or new_size is None:
            return False
        return (
            existing_size.quantity == new_size.quantity
            and existing_size.generic_unit.id == new_size.generic_unit.id
        )

    def push_ingredient_unit(
        self,
        ingredient_id: str,
        ingredient_unit: IngredientUnit,
    ) -> UpdateResultProtocol:
        return self.collection.update_one(
            {"id": ingredient_id},
            {"$push": {"units": ingredient_unit.model_dump()}},
        )
