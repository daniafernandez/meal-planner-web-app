from models.recipe.recipe import Recipe, RecipeIngredient
from services.project_model import ProjectModelService, UpdateResultProtocol


class RecipeService(ProjectModelService):
    collection_name = "recipes"

    def create_recipe(self, recipe: Recipe) -> Recipe:
        self.validate_unique_field("name", recipe.name)
        self.insert_one_item(recipe)
        return recipe

    def get_recipe_by_id(self, recipe_id: str) -> Recipe | None:
        item = self.collection.find_one({"id": recipe_id})
        if item is None:
            return None
        return Recipe(**item)

    def add_ingredient_to_recipe(
        self,
        recipe_id: str,
        recipe_ingredient: RecipeIngredient,
    ) -> tuple[UpdateResultProtocol, RecipeIngredient]:
        update_result = self.push_recipe_ingredient(
            recipe_id=recipe_id,
            recipe_ingredient=recipe_ingredient,
        )
        return update_result, recipe_ingredient

    def push_recipe_ingredient(
        self,
        recipe_id: str,
        recipe_ingredient: RecipeIngredient,
    ) -> UpdateResultProtocol:
        return self.collection.update_one(
            {"id": recipe_id},
            {"$push": {"ingredients": recipe_ingredient.model_dump()}},
        )
