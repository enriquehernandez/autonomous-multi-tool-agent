from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    LLM_PROVIDER: str = Field(default="OPENAI")
    LLM_MODEL: str = Field(default="gpt-4o")  # Necesitamos modelo con Vision

    OPENAI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None

    # APIs externas para las Tools
    EXCHANGE_RATE_API_KEY: str | None = None
    WEATHER_API_KEY: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
