import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the path to the .env file relative to this file
ENV_PATH = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH if ENV_PATH.exists() else ".env", 
        extra="ignore"
    )
    
    GROQ_API_KEY: str
    DATABASE_URL: str = "mysql+aiomysql://root:password@localhost/hcp_crm"
    # GROQ_MODEL_PRIMARY: str = "gemma2-9b-it"
    GROQ_MODEL_PRIMARY: str = "llama-3.3-70b-versatile"
    GROQ_MODEL_CONTEXT: str = "llama-3.3-70b-versatile"

settings = Settings()
