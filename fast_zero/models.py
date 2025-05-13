from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'  # Nome da tabela no banco de dados
    # Estes Atributos são as colunas da
    # Autoencremento do primary_key=True & deixa de ser necessário colocar id
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    # User unico
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    # Email único
    email: Mapped[str] = mapped_column(unique=True)
    # O banco de dados cria o datetime do registo
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    # updated_at: Mapped[datetime] = mapped_column(
    #     init=False,
    #     onupdate=func.now(),
    # )
