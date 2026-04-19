from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "CrowdFlow AI"
    # Future integrations
    FIREBASE_PROJECT_ID: str | None = None
    VERTEX_AI_PROJECT: str | None = None
    VERTEX_AI_LOCATION: str | None = "us-central1"
    GOOGLE_MAPS_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# We instantiate settings here as it's safe to be a global constant (read-only configuration)
settings = Settings()
