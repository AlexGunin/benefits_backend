import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    CORS_ALLOWED_ORIGINS: List[str] = []
    CORS_ALLOWED_ORIGIN_REGEX: str = "http://localhost:.*"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=f".env.{os.getenv('ENVIRONMENT', 'development')}")


settings = Settings()
