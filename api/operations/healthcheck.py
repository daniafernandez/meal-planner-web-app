class HealthcheckOperation:
    def execute(self) -> dict[str, str]:
        return {"status": "ok"}
