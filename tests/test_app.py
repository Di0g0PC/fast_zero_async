from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_eola_mundo():
    client = TestClient(app)  # Arrange (Organização)
    response = client.get('/')  # ACT (ação) - chama o endpoint '/'
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Hello World'}  # Assert
