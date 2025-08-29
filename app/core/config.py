# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "FELCO FastAPI"
    APP_VERSION: str = "1.0.0"

    # Environment
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 3306

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Logging
    LOG_LEVEL: str = "INFO"

    # Dynamically choose which .env file to load
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENVIRONMENT', 'development')}", case_sensitive=True
    )

    # ---------- helper methods stay the same ----------
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() in ["development", "dev", "local"]

    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() in ["production", "prod"]

    def is_staging(self) -> bool:
        return self.ENVIRONMENT.lower() in ["staging", "stage"]

    @property
    def debug_mode(self) -> bool:
        return self.is_development()

    @property
    def database_echo(self) -> bool:
        return self.is_development()

    @property
    def include_stack_trace(self) -> bool:
        return self.is_development()

    @property
    def show_docs(self) -> bool:
        return not self.is_production()

    # ---------- PROPER CONFIGURATION ----------

    @property
    def cors_origins(self) -> List[str]:
        if self.is_development():
            return [
                "http://localhost:3000",
                "http://localhost:3001",
                "http://localhost:8080",
                "http://localhost:8000",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8080",
                "http://127.0.0.1:8000",
            ]
        elif self.is_staging():
            return ["https://staging.salesreturn.com"]
        else:
            return ["https://salesreturn.com"]

    # ---------- TEST CONFIGURATION ----------

    # @property
    # def cors_origins(self) -> List[str]:
    #     if self.is_development():
    #         return [
    #             "http://localhost:3000",
    #             "http://localhost:3001",
    #             "http://localhost:8080",
    #             "http://localhost:8000",
    #             "http://127.0.0.1:3000",
    #             "http://127.0.0.1:8080",
    #             "http://127.0.0.1:8000",
    #         ]
    #     elif self.is_staging():
    #         return [
    #             "http://localhost:3000",
    #             "http://localhost:3001",
    #             "http://localhost:8080",
    #             "http://localhost:8000",
    #             "http://127.0.0.1:3000",
    #             "http://127.0.0.1:8080",
    #             "http://127.0.0.1:8000",
    #         ]
    #     else:
    #         return [
    #             "http://localhost:3000",
    #             "http://localhost:3001",
    #             "http://localhost:8080",
    #             "http://localhost:8000",
    #             "http://127.0.0.1:3000",
    #             "http://127.0.0.1:8080",
    #             "http://127.0.0.1:8000",
    #         ]

    def get_log_level(self) -> str:
        if self.is_development():
            return "DEBUG"
        elif self.is_staging():
            return "INFO"
        return "WARNING"

    def get_log_format(self) -> str:
        if self.is_development():
            return "%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s | [%(filename)s:%(lineno)d] | %(message)s"
        return "%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s | %(message)s"

    def get_openapi_url(self) -> Optional[str]:
        return "/api/v1/openapi.json" if self.show_docs else None

    def get_docs_url(self) -> Optional[str]:
        return "/docs" if self.show_docs else None

    def get_redoc_url(self) -> Optional[str]:
        return "/redoc" if self.show_docs else None


@lru_cache()
def get_settings() -> Settings:
    return Settings()
