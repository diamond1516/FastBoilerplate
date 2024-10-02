from dotenv import load_dotenv
from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings

load_dotenv()


class DbSecureSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    ECHO: bool

    @computed_field
    @property
    def DB_URL(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme='postgresql+asyncpg',
            host=self.DB_HOST,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    class Config:
        env_file = "../.env"


class MainSecureSettings(BaseSettings):
    SERVER_HOST: str


DB_SECURES = DbSecureSettings()
MAIN_SECURES = MainSecureSettings()

