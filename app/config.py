from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_type: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    weather_api_key: str
    redis_host: str
    redis_port: str
    celery_broker_url: str
    celery_result_backend: str

    class Config:
        env_file = ".env"


settings = Settings()
