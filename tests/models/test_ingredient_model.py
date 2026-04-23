import pytest
from pydantic import ValidationError

from models.ingredient.ingredient import Ingredient


def test_ingredient_normalizes_name() -> None:
    ingredient = Ingredient(
        id="rice",
        name="  Brown   RICE  ",
        staple=True,
    )

    assert ingredient.name == "brown rice"


def test_ingredient_name_must_not_be_empty() -> None:
    with pytest.raises(ValidationError, match="name must not be empty"):
        Ingredient(
            id="empty",
            name="   ",
            staple=False,
        )
