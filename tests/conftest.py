import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


@pytest.fixture  # Para objetos repetidos o pytest tem esta opção
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    # Banco em memoria apenas para teste (duração do teste)- Apenas Para SQLite
    # Para criar a tabela a partir dos metadados , através da engine
    table_registry.metadata.create_all(engine)
    # Cria uma sessão temporária, que é automaticamente fechada no fim do bloco
    with Session(engine) as session:
        yield session
        # yield - Entrega essa sessão para quem chamar a função
    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(username='Teste', email='teste@test.com', password='testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
