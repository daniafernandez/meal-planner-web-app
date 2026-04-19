import pytest
from pydantic import ValidationError

from models.generic_unit import (
    GenericUnit,
    MeasurementType,
    get_equivalent_generic_unit_names,
)


def test_generic_unit_normalizes_name() -> None:
    generic_unit = GenericUnit(
        id="fluid-ounce",
        name="  FLUID   OUNCE  ",
    )

    assert generic_unit.name == "fluid ounce"
    assert generic_unit.measurement_type == MeasurementType.VOLUME


def test_generic_unit_name_must_not_be_empty() -> None:
    with pytest.raises(ValidationError, match="name must not be empty"):
        GenericUnit(
            id="empty",
            name="   ",
        )


@pytest.mark.parametrize(
    ("name", "measurement_type"),
    [
        ("bag", MeasurementType.COUNT),
        ("lb", MeasurementType.MASS),
        ("tablespoon", MeasurementType.VOLUME),
        ("pinch", MeasurementType.INFORMAL),
    ],
)
def test_generic_unit_infers_measurement_type(
    name: str,
    measurement_type: MeasurementType,
) -> None:
    generic_unit = GenericUnit(
        id=name,
        name=name,
    )

    assert generic_unit.measurement_type == measurement_type


def test_generic_unit_raises_when_measurement_type_cannot_be_inferred() -> None:
    generic_unit = GenericUnit(
        id="mystery",
        name="mystery",
    )

    with pytest.raises(ValueError, match="Unable to infer measurement type"):
        generic_unit.measurement_type


def test_get_equivalent_generic_unit_names_normalizes_name() -> None:
    assert get_equivalent_generic_unit_names("  POUNDS ") == frozenset(
        {"pound", "pounds", "lb", "lbs"},
    )
