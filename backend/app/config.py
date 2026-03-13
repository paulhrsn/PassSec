import os
from datetime import timedelta


def _split_csv(raw_value: str) -> list[str]:
    return [v.strip() for v in raw_value.split(",") if v.strip()]


class Config:
    """Application runtime configuration loaded from environment variables."""

    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_EXPIRES_HOURS", "12")))
    JWT_ERROR_MESSAGE_KEY = "error"

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(512 * 1024)))

    raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    CORS_ORIGINS = _split_csv(raw_origins)
    CORS_SUPPORTS_CREDENTIALS = False

    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

    @classmethod
    def validate(cls) -> None:
        """Fail fast for unsafe or missing production secrets."""
        if not cls.SECRET_KEY:
            raise RuntimeError("SECRET_KEY is required.")
        if not cls.JWT_SECRET_KEY:
            raise RuntimeError("JWT_SECRET_KEY is required.")