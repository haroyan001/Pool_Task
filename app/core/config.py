from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "pool_1"
    POSTGRES_PORT: str = "5432"
    
    @property
    def DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    INSTRUCTOR_MIN_HOURS_PER_WEEK: int = 20
    INSTRUCTOR_MAX_HOURS_PER_WEEK: int = 40
    
    class Config:
        case_sensitive = True


settings = Settings()
