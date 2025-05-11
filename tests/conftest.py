import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture  # Para objetos repetidos o pytest tem esta opção
def client():
    return TestClient(app)  # Arrange (Organização)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    # Banco em memoria apenas para teste (duração do teste)- Apenas Para SQLite
    # Para criar a tabela a partir dos metadados , através da engine
    table_registry.metadata.create_all(engine)
    # Cria uma sessão temporária, que é automaticamente fechada no fim do bloco
    with Session(engine) as session:
        yield session
        # yield - Entrega essa sessão para quem chamar a função
    table_registry.metadata.drop_all(engine)
