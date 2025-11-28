from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_TITLE: str
    QDRANT_URL: str 
    COLLECTION_NAME: str 

    model_config = SettingsConfigDict(env_file=".env")

env = Settings()