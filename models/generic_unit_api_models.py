from pydantic import BaseModel

from models.generic_unit import GenericUnit, MeasurementType


class CreateGenericUnitRequest(BaseModel):
    id: str
    name: str
    measurement_type: MeasurementType


class GenericUnitResponse(BaseModel):
    generic_unit: GenericUnit
