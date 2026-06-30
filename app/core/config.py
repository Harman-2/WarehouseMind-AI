from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str

    HOST: str
    PORT: int

    DATABASE_URL: str

    LOG_LEVEL: str

    class Config:
        env_file = ".env"


settings = Settings()