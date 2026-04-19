from api.resources.endpoints import get_healthcheck_operation
from tests.api.resources.endpoint_helpers import FakeOperation, build_client


def test_healthcheck_endpoint_success() -> None:
    operation = FakeOperation(result={"status": "ok"})

    with build_client() as client:
        client.app.dependency_overrides[get_healthcheck_operation] = lambda: operation

        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert operation.executed is True


def test_healthcheck_endpoint_translates_unexpected_errors_to_500() -> None:
    with build_client() as client:
        client.app.dependency_overrides[get_healthcheck_operation] = lambda: FakeOperation(
            error=RuntimeError("boom"),
        )

        response = client.get("/health")

    assert response.status_code == 500
    assert response.json() == {"detail": "An unexpected error occurred."}
