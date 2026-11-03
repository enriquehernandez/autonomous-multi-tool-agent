from pydantic_settings import BaseSettings, SettingsConfigDict
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

    # --- API Keys de las Tools (opcionales) ---
    EXCHANGE_RATE_API_KEY: str | None = None
    WEATHER_API_KEY: str | None = None
    GEOCODING_API_KEY: str | None = None

    # --- URLs de las APIs de las Herramientas (Configurables) ---
    CURRENCY_API_URL: str = Field(
        default="https://api.frankfurter.dev/v2/rates")
    GEOCODING_API_URL: str = Field(
        default="https://geocoding-api.open-meteo.com/v1/search")
    WEATHER_API_URL: str = Field(
        default="https://api.open-meteo.com/v1/forecast")

    # --- Configuración adicional ---
    LOG_LEVEL: str = Field(default="INFO")

    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
