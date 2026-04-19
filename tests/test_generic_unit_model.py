import pytest
from pydantic import ValidationError

from models.generic_unit import GenericUnit, MeasurementType


def test_generic_unit_normalizes_name() -> None:
    generic_unit = GenericUnit(
        id="fluid-ounce",
        name="  FLUID   OUNCE  ",
        measurement_type=MeasurementType.VOLUME,
    )

    assert generic_unit.name == "fluid ounce"


def test_generic_unit_name_must_not_be_empty() -> None:
    with pytest.raises(ValidationError, match="name must not be empty"):
        GenericUnit(
            id="empty",
            name="   ",
            measurement_type=MeasurementType.COUNT,
        )
