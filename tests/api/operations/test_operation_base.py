import pytest

from api.operations import Operation


def test_operation_base_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        Operation()
