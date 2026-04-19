from api.operations import HealthcheckOperation


def test_healthcheck_operation_response_property() -> None:
    operation = HealthcheckOperation()

    assert operation.response == {"status": "ok"}


def test_healthcheck_operation_execute_returns_response() -> None:
    operation = HealthcheckOperation()

    assert operation.execute() == {"status": "ok"}
