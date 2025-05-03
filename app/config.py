from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Завантажує .env файл

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"  # Pydantic сам завантажить .env

settings = Settings()