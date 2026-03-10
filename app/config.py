from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATA_DIR: str
    OUTPUT_DIR: str
    FRONTEND_DIR: str
    IMG_MODEL: str
    LLM_MODEL: str

    model_config = ConfigDict(env_file=".env")

settings = Settings()
