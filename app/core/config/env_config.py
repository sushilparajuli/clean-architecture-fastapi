from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_port: int
    db_host: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore',
    )