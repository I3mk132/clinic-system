"""
Central application configuration.

Everything that might change between environments (dev / staging / production)
or between deployments (different clinic, different database, different domain)
lives here and is read from environment variables (see .env.example).

This is the ONLY file that should read os.environ directly - every other
module should import `settings` from here.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- General ---
    APP_NAME: str = "Clinic Booking System"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    # --- Security ---
    SECRET_KEY: str = "insecure-dev-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # --- Database ---
    # Swap this single value to move from SQLite -> PostgreSQL / MySQL later.
    DATABASE_URL: str = "sqlite:///./clinic.db"

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:5500,http://127.0.0.1:5500"

    # --- Default admin (created by seed script) ---
    FIRST_ADMIN_EMAIL: str = "admin@myclinic.com"
    FIRST_ADMIN_PASSWORD: str = "Admin@12345"
    FIRST_ADMIN_NAME: str = "Clinic Administrator"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance - import this everywhere instead of re-reading env vars."""
    return Settings()


settings = get_settings()
