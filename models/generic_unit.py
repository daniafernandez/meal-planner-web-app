from enum import StrEnum

from models.project_model import ProjectModel


class MeasurementType(StrEnum):
    COUNT = "COUNT"
    MASS = "MASS"
    VOLUME = "VOLUME"


class GenericUnit(ProjectModel):
    name: str
    measurement_type: MeasurementType
