from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db:5432/mydb"
    
    class Config:
        env_file = ".env"

settings = Settings()
