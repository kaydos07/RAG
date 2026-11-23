from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    MODEL_API_KEY: str
    MODEL_NAME: str
    EMBEDDING_MODEL_NAME: str
    
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf8',
        extra='ignore'
    )
    
settings = Settings()