from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "mydatabase"
    GCP_CREDENTIALS_PATH: str = "/path/to/credentials.json"

    class Config:
        env_file = ".env"
