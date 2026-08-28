from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_port: int
    db_host: str
    jwt_secret_key: str = "secret-key-user-mgmt-very-secure-random-12345"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    bcrypt_rounds: int = 12

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore',
    )