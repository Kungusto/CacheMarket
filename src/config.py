from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent

class JWTConfig:
    ACCESS_TOKEN_EXP: int = 60 * 15
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 30
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"


class Settings(BaseSettings):
    """
    Режимы работы:
    - LOCAL: локальная разработка
    - TEST: выполнение тестов
    - PROD: запуск на боевом сервере
    """

    MODE: Literal["LOCAL", "TEST", "PROD"]

    # Базы данных
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int

    JWT_ALGORITHM: str

    # JWT
    jwt: JWTConfig = JWTConfig()

    # Асинхронное подключение
    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # URL подключения к Redis
    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(env_file=BASE_DIR.parent / ".env")

settings = Settings() # type: ignore