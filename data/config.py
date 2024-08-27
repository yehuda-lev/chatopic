from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    tg_api_id: int
    tg_api_hash: str
    tg_bot_token: str
    admins: list[int]
    msg_welcome: str
    default_language: str


@lru_cache
def get_settings():
    return Settings()