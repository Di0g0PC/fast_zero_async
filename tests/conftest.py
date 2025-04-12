import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture  # Para objetos repetidos o pytest tem esta opção
def client():
    return TestClient(app)  # Arrange (Organização)
