import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict



BASE_DIR = Path(__file__).parent.parent
load_dotenv()

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    prefix1: str = "/jwt"

class DatabaseConfig(BaseModel):
    url: str = os.environ.get("DB_URL")
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class DatabaseTestConfig(BaseModel):
    url: str = os.environ.get("DB_TEST_URL")
    echo: bool = False
    echo_pool: bool = False



class SMTPConfig(BaseModel):
    host: str = os.environ.get("SMTP_HOST")
    port: str = os.environ.get("SMTP_PORT")
    user: str = os.environ.get("SMTP_USER")
    password: str = os.environ.get("SMTP_PASSWORD")


class AuthenticationJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "keys_jwt" / "private.pem"
    public_key_path: Path = BASE_DIR / "keys_jwt" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    # access_token_expire_minutes: int = 3

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()
    db_test: DatabaseTestConfig = DatabaseTestConfig()
    auth_jwt: AuthenticationJWT = AuthenticationJWT()
    smtp: SMTPConfig = SMTPConfig()


settings = Settings()


