from enum import StrEnum

from models.project_model import ProjectModel


class GenericUnit(ProjectModel):
    name: str
    measurement_type: StrEnum