from abc import ABC

from pydantic import Field, BaseModel

from models.generic_unit import GenericUnit


class SizeDescription(BaseModel, ABC):

    @property
    def description_string(self) -> str:
        raise NotImplementedError


class QuantitativeDescription(SizeDescription):
    quantity: int = Field(gt=0)
    generic_unit: GenericUnit

    @property
    def description_string(self) -> str:
        return f"{self.quantity} {self.generic_unit.name}"

class QualitativeDescription(SizeDescription):
    quality: str

    @property
    def description_string(self) -> str:
        return f"{self.quality}"