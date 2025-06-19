from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',  # Ignorar outras variaveis que não sao importadas
    )
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # def __init__(self, **kwargs):
    #     # Inicia o modelo Pydantic
    #     super().__init__(**kwargs)
    #     # Limpar o caractere de escape, caso apareça
    #     self.DATABASE_URL = self.DATABASE_URL.replace(r'\x3a', ':')
