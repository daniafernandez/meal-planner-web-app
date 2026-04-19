from enum import StrEnum

from pydantic import field_validator

from models.project_model import ProjectModel


class MeasurementType(StrEnum):
    COUNT = "COUNT"
    MASS = "MASS"
    VOLUME = "VOLUME"
    INFORMAL = "INFORMAL"   # imprecise measurements like pinch, dollop, etc.


class GenericUnit(ProjectModel):
    name: str
    measurement_type: MeasurementType

    @field_validator("name")
    @classmethod
    def normalize_name(cls, name: str) -> str:
        normalized_name = " ".join(name.casefold().split())
        if not normalized_name:
            raise ValueError("name must not be empty.")
        return normalized_name
