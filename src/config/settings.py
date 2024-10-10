from datetime import timedelta

from pydantic_settings import BaseSettings
from src.config import secures


class Settings(BaseSettings):
    VERSION: str = '0.1.0'
    API_V1_STR: str = "/api/v1"
    WS_PREFIX: str = '/ws'
    ACCESS_TOKEN_EXPIRE: timedelta = timedelta(days=1)
    SERVER_NAME: str = "localhost"
    SERVER_HOST: str = secures.MAIN_SECURES.SERVER_HOST
    PROJECT_NAME: str = "FastAPI Boilerplate"
    ALGORITHM: str = "HS256"
    DEBUG: bool = True
    MEDIA_URL: str = 'media/'
    STATIC_URL: str = 'static/'
    TIME_ZONE: str = 'Asia/Tashkent'


SETTINGS = Settings()
