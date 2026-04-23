import pytest

from models.generic_unit import GenericUnit
from models.ingredient.ingredient_unit import IngredientUnit
from models.ingredient.size_description import QualitativeDescription, QuantitativeDescription
from models.recipe.recipe_ingredient import RecipeIngredient
from models.recipe.recipe_ingredient_quantity import RecipeIngredientQuantity


class TestUnit:
    def test_unit_returns_correct_count_type_generic_unit(self):
        recipe_ingredient = RecipeIngredient(ingredient_line_string="50 medium onions, sliced")
        actual = recipe_ingredient.unit.generic_unit.name
        expected = IngredientUnit(generic_unit=GenericUnit(name="count"),
                                  size=QualitativeDescription(quality="medium"),
                                  gram_weight=100).generic_unit.name
        assert actual == expected

    def test_unit_returns_correct_volume_type_generic_unit(self):
        recipe_ingredient = RecipeIngredient(ingredient_line_string="1 1/2 cups milk")
        actual = recipe_ingredient.unit.generic_unit.name
        expected = IngredientUnit(generic_unit=GenericUnit(name="cups"),
                                  gram_weight=365).generic_unit.name
        assert actual == expected

    def test_unit_returns_correct_qualitative_size(self):
        recipe_ingredient = RecipeIngredient(ingredient_line_string="50 medium onions, sliced")
        actual = recipe_ingredient.unit.size.quality
        expected = IngredientUnit(generic_unit=GenericUnit(name="count"),
                                  size=QualitativeDescription(quality="medium"),
                                  gram_weight=100).size.quality
        assert actual == expected

    def test_unit_returns_correct_quantitative_size(self):
        recipe_ingredient = RecipeIngredient(ingredient_line_string="2 8oz beef filets")
        actual = recipe_ingredient.unit.size.quantity
        expected = IngredientUnit(generic_unit=GenericUnit(name="count"),
                                  size=QuantitativeDescription(quantity=8, generic_unit=GenericUnit(name="oz")),
                                  gram_weight=226).size.quantity
        assert actual == expected

    def test_unit_returns_correct_grams(self):
        recipe_ingredient = RecipeIngredient(ingredient_line_string="50 medium onions, sliced")
        actual = recipe_ingredient.unit.gram_weight
        expected = IngredientUnit(generic_unit=GenericUnit(name="count"),
                                  size=QualitativeDescription(quality="medium"),
                                  gram_weight=100).gram_weight
        assert actual == expected

class TestQuantity:
    def test_quantity_computed_for_numeric_quantity(self):
        recipe_ingredient = RecipeIngredient(ingredient_line_string="50 medium onions, sliced")
        actual = recipe_ingredient.quantity.numeric_quantity
        expected = 50
        assert actual == expected

    def test_quantity_computed_for_numeric_quantity_expressed_as_word(self):
        recipe_ingredient = RecipeIngredient(
            ingredient_line_string="three garlic cloves, finely chopped",
        )
        actual = recipe_ingredient.quantity.numeric_quantity
        expected = 3
        assert actual == expected

    def test_quantity_computed_for_alpha_quantity(self):
        recipe_ingredient = RecipeIngredient(
            ingredient_line_string="dozen garlic cloves, finely chopped",
        )
        actual = recipe_ingredient.quantity.alpha_quantity
        expected = "dozen"
        assert actual == expected

    @pytest.mark.parametrize(
        ("ingredient_line_string", "expected_numeric_quantity"),
        [
            ("a couple of garlic cloves, finely chopped", 2),
            ("a pair of garlic cloves, finely chopped", 2),
            ("both garlic cloves, finely chopped", 2),
            ("a few garlic cloves, finely chopped", 3),
            ("several garlic cloves, finely chopped", 4),
            ("some garlic cloves, finely chopped", 1),
            ("a handful of garlic cloves, finely chopped", 1),
            ("a dozen garlic cloves, finely chopped", 12),
            ("dozen garlic cloves, finely chopped", 12),
            ("half a dozen garlic cloves, finely chopped", 6),
            ("half dozen garlic cloves, finely chopped", 6),
        ],
    )
    def test_numeric_quantity_computed_for_alpha_quantity_aliases(
        self,
        ingredient_line_string: str,
        expected_numeric_quantity: float,
    ):
        recipe_ingredient = RecipeIngredient(
            ingredient_line_string=ingredient_line_string,
        )
        actual = recipe_ingredient.quantity.numeric_quantity
        expected = expected_numeric_quantity
        assert actual == expected

    @pytest.mark.parametrize(
        "ingredient_line_string",
        [
            "",
            "medium onion",
            "salt to taste",
        ],
    )
    def test_quantity_defaults_to_one_when_quantity_cannot_be_confidently_inferred(
        self,
        ingredient_line_string: str,
    ):
        recipe_ingredient = RecipeIngredient(
            ingredient_line_string=ingredient_line_string,
        )
        actual = recipe_ingredient.quantity.numeric_quantity
        expected = 1
        assert actual == expected

    def test_quantity_returns_correct_value_for_fraction(self):
        recipe_ingredient = RecipeIngredient(ingredient_line_string="1 1/2 cups milk")
        actual = recipe_ingredient.quantity.precise_quantity
        expected = RecipeIngredientQuantity(numeric_quantity=1.5).precise_quantity
        assert actual == expected