import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic import  AnyHttpUrl
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    # TITLE: str = "ID30 API"
    # ENV: str = "dev"
    # BASE_URL: str = "/api/v1"
    # VERSION: str = "0.0.1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:8001", 
        "http://localhost:81", 
        "http://127.0.0.1:8001",
        "http://localhost:3000", 
        "http://localhost:3001"
    ]

    # API_URL: str
    # API_BASE_URL: str
    

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER_NAME: str
    DB_PASSWORD: str
    
    GITLAB_APP_ID : str
    GITLAB_APP_SECRET :str
    GITLAB_REDIRECT_URI :str
    
    GITHUB_APP_ID :str
    GITHUB_APP_SECRET: str
    GITHUB_REDIRECT_URI:str
    
    FACEBOOK_APP_ID : str
    FACEBOOK_APP_SECRET :str
    FACEBOOK_REDIRECT_URI :str
    FACEBOOK_API_VERSION :str
    
    LINKEDIN_CLIENT_ID :str
    LINKEDIN_CLIENT_SECRET :str
    LINKEDIN_REDIRECT_URI:str 


 
    ALGORITHM :str
    JWT_SECRET_KEY:str
    JWT_REFRESH_SECRET_KEY:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRE_MINUTES:str  # 1 month

    # SECRET_KEY: str
    
    def get_database_url(self, is_async: bool = False) -> str:
        if is_async:
            return (
                "postgresql+asyncpg://"f"{self.DB_USER_NAME}:{self.DB_PASSWORD}@"f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        else:
            return (
                "postgresql://"f"{self.DB_USER_NAME}:{self.DB_PASSWORD}@"f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )

    


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()