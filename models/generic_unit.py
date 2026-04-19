from enum import StrEnum

from pydantic import computed_field, field_validator

from models.project_model import ProjectModel


class MeasurementType(StrEnum):
    COUNT = "COUNT"
    MASS = "MASS"
    VOLUME = "VOLUME"
    INFORMAL = "INFORMAL"   # imprecise measurements like pinch, dollop, etc.


MEASUREMENT_TYPE_NAMES = {
    MeasurementType.COUNT: {
        "bag",
        "box",
        "bunch",
        "can",
        "clove",
        "container",
        "count",
        "ct",
        "each",
        "ea",
        "item",
        "jar",
        "package",
        "pack",
        "piece",
        "slice",
    },
    MeasurementType.MASS: {
        "gram",
        "grams",
        "g",
        "kilogram",
        "kilograms",
        "kg",
        "ounce",
        "ounces",
        "oz",
        "pound",
        "pounds",
        "lb",
        "lbs",
    },
    MeasurementType.VOLUME: {
        "cup",
        "cups",
        "fluid ounce",
        "fluid ounces",
        "fl oz",
        "liter",
        "liters",
        "l",
        "milliliter",
        "milliliters",
        "ml",
        "pint",
        "pints",
        "tablespoon",
        "tablespoons",
        "tbsp",
        "teaspoon",
        "teaspoons",
        "tsp",
    },
    MeasurementType.INFORMAL: {
        "dash",
        "dollop",
        "handful",
        "pinch",
        "splash",
    },
}


GENERIC_UNIT_NAME_EQUIVALENCES = (
    frozenset({"gram", "grams", "g"}),
    frozenset({"kilogram", "kilograms", "kg"}),
    frozenset({"ounce", "ounces", "oz"}),
    frozenset({"pound", "pounds", "lb", "lbs"}),
    frozenset({"cup", "cups"}),
    frozenset({"fluid ounce", "fluid ounces", "fl oz"}),
    frozenset({"liter", "liters", "l"}),
    frozenset({"milliliter", "milliliters", "ml"}),
    frozenset({"pint", "pints"}),
    frozenset({"tablespoon", "tablespoons", "tbsp"}),
    frozenset({"teaspoon", "teaspoons", "tsp"}),
    frozenset({"each", "ea"}),
    frozenset({"package", "pack"}),
)


def get_equivalent_generic_unit_names(name: str) -> frozenset[str]:
    normalized_name = GenericUnit.normalize_name(name)
    for equivalent_names in GENERIC_UNIT_NAME_EQUIVALENCES:
        if normalized_name in equivalent_names:
            return equivalent_names
    return frozenset({normalized_name})


class GenericUnit(ProjectModel):
    name: str

    @field_validator("name")
    @classmethod
    def normalize_name(cls, name: str) -> str:
        normalized_name = " ".join(name.casefold().split())
        if not normalized_name:
            raise ValueError("name must not be empty.")
        return normalized_name

    @computed_field
    @property
    def measurement_type(self) -> MeasurementType:
        for measurement_type, names in MEASUREMENT_TYPE_NAMES.items():
            if self.name in names:
                return measurement_type
        raise ValueError(f"Unable to infer measurement type from name '{self.name}'.")
