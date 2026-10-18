from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    deepseek_model: str = "deepseek-flash"
    deepseek_api_key: SecretStr = Field(min_length=1)
    deepseek_base_url: str = "https://api.deepseek.com"
