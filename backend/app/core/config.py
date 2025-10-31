from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Google Cloud
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # MongoDB
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "kesu_ai"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Email Processing
    MAX_EMAILS_PER_FETCH: int = 100
    EMAIL_FETCH_INTERVAL_MINUTES: int = 60
    PRIORITY_REMINDER_TIMES: str = "09:00,14:00,17:00"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
