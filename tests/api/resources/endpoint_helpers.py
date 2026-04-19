from contextlib import contextmanager
from typing import Iterator

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.resources.endpoints import router


class FakeOperation:
    def __init__(self, result=None, error: Exception | None = None):
        self.result = result
        self.error = error
        self.executed = False

    def execute(self):
        self.executed = True
        if self.error is not None:
            raise self.error
        return self.result


@contextmanager
def build_client() -> Iterator[TestClient]:
    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
