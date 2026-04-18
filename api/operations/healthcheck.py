from api.operations.base import Operation


class HealthcheckOperation(Operation):
    @property
    def response(self) -> dict[str, str]:
        return {"status": "ok"}

    def execute(self) -> dict[str, str]:
        return self.response
