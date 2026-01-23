from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    _BACKEND_DIR = Path(__file__).resolve().parents[2]
    model_config = SettingsConfigDict(
        env_file=str(_BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
    )

    DATABASE_URL: str
    FRONTEND_ORIGIN: str = "http://localhost:8080"

    # Public base URL used for static assets (uploads)
    STATIC_BASE_URL: str = "http://localhost:8000"

    # Auth / JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
