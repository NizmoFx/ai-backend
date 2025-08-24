from pydantic import BaseModel
import os

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/app")
    secret_key: str = os.getenv("SECRET_KEY", "devsecret")
    storage_dir: str = os.getenv("STORAGE_DIR", "/app/storage")
    ai_provider: str = os.getenv("AI_PROVIDER", "dummy")
    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@mq:5672//")
    openai_key: str | None = os.getenv("OPENAI_API_KEY")
    gemini_key: str | None = os.getenv("GEMINI_API_KEY")

settings = Settings()
os.makedirs(settings.storage_dir, exist_ok=True)
