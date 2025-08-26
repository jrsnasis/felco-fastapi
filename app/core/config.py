# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "FELCO FastAPI"
    APP_VERSION: str = "1.0.0"
    
    # Environment - this determines all other behaviors
    ENVIRONMENT: str = "production"  # production, development, staging
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    # Environment detection methods
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() in ["development", "dev", "local"]
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() in ["production", "prod"]
    
    def is_staging(self) -> bool:
        """Check if running in staging environment"""
        return self.ENVIRONMENT.lower() in ["staging", "stage"]
    
    # Dynamic properties based on environment
    @property
    def debug_mode(self) -> bool:
        """Enable debug mode in development"""
        return self.is_development()
    
    @property
    def database_echo(self) -> bool:
        """Enable SQL logging in development"""
        return self.is_development()
    
    @property
    def include_stack_trace(self) -> bool:
        """Include stack traces in error responses in development"""
        return self.is_development()
    
    @property
    def show_docs(self) -> bool:
        """Show API docs in non-production environments"""
        return not self.is_production()
    
    @property
    def cors_origins(self) -> List[str]:
        """Environment-specific CORS origins"""
        if self.is_development():
            return [
                "http://localhost:3000",
                "http://localhost:3001", 
                "http://localhost:8080",
                "http://localhost:8000",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8080",
                "http://127.0.0.1:8000"
            ]
        elif self.is_staging():
            # Add your staging URLs here
            return ["https://staging.yourapp.com"]
        else:  # production
            # Add your production URLs here
            return ["https://yourapp.com"]
    
    def get_log_level(self) -> str:
        """Get appropriate log level for environment"""
        if self.is_development():
            return "DEBUG"
        elif self.is_staging():
            return "INFO"
        else:  # production
            return "WARNING"
    
    def get_log_format(self) -> str:
        """Get log format based on environment"""
        if self.is_development():
            return "%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s | [%(filename)s:%(lineno)d] | %(message)s"
        else:
            return "%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s | %(message)s"
    
    def get_openapi_url(self) -> Optional[str]:
        """Get OpenAPI URL - only available in non-production"""
        return "/api/v1/openapi.json" if self.show_docs else None
    
    def get_docs_url(self) -> Optional[str]:
        """Get docs URL - only available in non-production"""
        return "/docs" if self.show_docs else None
    
    def get_redoc_url(self) -> Optional[str]:
        """Get ReDoc URL - only available in non-production"""  
        return "/redoc" if self.show_docs else None


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()