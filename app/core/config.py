from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv()

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL")
    API_V1_STR: str = os.getenv("API_ENDPOINT_VERSION")

    class Config:
        case_sensitive = True

settings = Settings()
