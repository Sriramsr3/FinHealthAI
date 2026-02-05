from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List, Any
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API Settings
    APP_NAME: str = "   Financial Health Asses  nt Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./  _finhealth.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ENCRYPTION_KEY: bytes = os.getenv("ENCRYPTION_KEY", "dev-encryption-key-32-bytes!!").encode()[:32]
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-5.2"
    OPENAI_ENABLED: bool = bool(os.getenv("OPENAI_API_KEY"))
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod

    def parse_allowed_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".csv", ".xlsx", ".xls", ".pdf"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
