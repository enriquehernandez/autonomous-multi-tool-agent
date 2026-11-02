from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # --- Configuración del LLM ---
    LLM_PROVIDER: str = Field(default="OPENROUTER")
    OPENROUTER_MODEL: str = Field(default="google/gemini-2.5-flash")
    OPENAI_MODEL: str = Field(default="gpt-4o")
    GOOGLE_MODEL: str = Field(default="gemini-1.5-pro")
    GROQ_MODEL: str = Field(default="llama-3.3-70b-versatile")

    # --- API Keys ---
    OPENROUTER_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None

    # --- API Keys de las Tools (opcionales, por defecto vacías) ---
    EXCHANGE_RATE_API_KEY: str | None = None
    WEATHER_API_KEY: str | None = None

    # --- Configuración adicional ---
    LOG_LEVEL: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
