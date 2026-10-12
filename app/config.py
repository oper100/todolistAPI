from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///database.db"
    db_echo: bool = False


settings = Settings()
