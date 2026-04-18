from models.api_models import CreateGenericUnitRequest, GenericUnitResponse
from models.generic_unit import GenericUnit
from services.generic_unit import GenericUnitService


class CreateGenericUnitOperation:
    def __init__(self, generic_unit_service: GenericUnitService | None = None):
        self.generic_unit_service = generic_unit_service or GenericUnitService()

    def execute(self, request: CreateGenericUnitRequest) -> GenericUnitResponse:
        generic_unit = GenericUnit(
            id=request.id,
            name=request.name,
            measurement_type=request.measurement_type,
        )
        created_generic_unit = self.generic_unit_service.create_generic_unit(generic_unit)
        return GenericUnitResponse(generic_unit=created_generic_unit)
