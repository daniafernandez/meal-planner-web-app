from typing import ClassVar

from pydantic import BaseModel


class RecipeIngredientQuantity(BaseModel):
    ALPHA_QUANTITY_ESTIMATES: ClassVar[dict[str, float]] = {
        "a couple": 2,
        "a couple of": 2,
        "couple": 2,
        "couple of": 2,
        "a pair": 2,
        "a pair of": 2,
        "pair": 2,
        "pair of": 2,
        "both": 2,
        "a few": 3,
        "few": 3,
        "several": 4,
        "some": 1,
        "a handful": 1,
        "a handful of": 1,
        "handful": 1,
        "handful of": 1,
        "a dozen": 12,
        "a dozen of": 12,
        "dozen": 12,
        "dozen of": 12,
        "half dozen": 6,
        "half a dozen": 6,
        "half dozen of": 6,
        "half a dozen of": 6,
    }

    numeric_quantity: float | None = None
    alpha_quantity: str | None = None

    @property
    def precise_quantity(self) -> float:
        if self.numeric_quantity is not None:
            return self.numeric_quantity
        if self.alpha_quantity is not None:
            return self.ALPHA_QUANTITY_ESTIMATES.get(self.alpha_quantity, 1)
        return 1
