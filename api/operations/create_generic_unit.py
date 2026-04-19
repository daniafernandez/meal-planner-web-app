from api.operations.base import Operation
from models.api_models import CreateGenericUnitRequest, GenericUnitResponse
from models.generic_unit import GenericUnit
from services.generic_unit import GenericUnitService


class CreateGenericUnitOperation(Operation):
    def __init__(
        self,
        request: CreateGenericUnitRequest,
        generic_unit_service: GenericUnitService | None = None,
    ):
        self.request = request
        self.generic_unit_service = generic_unit_service or GenericUnitService()
        self.generic_unit: GenericUnit | None = None
        self.created_generic_unit: GenericUnit | None = None

    def build_generic_unit(self) -> GenericUnit:
        return GenericUnit(
            name=self.request.name,
            measurement_type=self.request.measurement_type,
        )

    def create_generic_unit(self, generic_unit: GenericUnit) -> GenericUnit:
        return self.generic_unit_service.create_generic_unit(generic_unit)

    def validate_created_generic_unit(self) -> GenericUnit:
        if self.created_generic_unit is None:
            raise ValueError("created_generic_unit must be set before building a response.")
        return self.created_generic_unit

    @property
    def response(self) -> GenericUnitResponse:
        return GenericUnitResponse(generic_unit=self.created_generic_unit)

    def execute(self) -> GenericUnitResponse:
        self.generic_unit = self.build_generic_unit()
        self.created_generic_unit = self.create_generic_unit(self.generic_unit)
        self.validate_created_generic_unit()
        return self.response
