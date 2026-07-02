from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "WarehouseMind AI"
    VERSION: str = "1.0.0"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./warehouse.db"
    LOG_LEVEL: str = "INFO"

    GOOGLE_API_KEY: str = ""

    JWT_SECRET: str = "warehousemind-dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    CORS_ORIGINS: str = "*"
    UPLOAD_DIR: str = "uploads/documents"

    class Config:
        env_file = ".env"


settings = Settings()
