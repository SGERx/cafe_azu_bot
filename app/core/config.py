from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    CLIENT_BOT_TOKEN: str
    ADMIN_TOKEN: str

    SHEET_ID: Optional[str] = None
    EMAIL: Optional[str] = None
    TYPE: Optional[str] = None
    PROJECT_ID: Optional[str] = None
    PRIVATE_KEY_ID: Optional[str] = None
    PRIVATE_KEY: Optional[str] = None
    CLIENT_EMAIL: Optional[str] = None
    CLIENT_ID: Optional[str] = None
    AUTH_URI: Optional[str] = None
    TOKEN_URI: Optional[str] = None
    AUTH_PROVIDER_X509_CERT_URL: Optional[str] = None
    CLIENT_X509_CERT_URL: Optional[str] = None
    UNIVERSE_DOMAIN: Optional[str] = None

    RESTAURANT_NAMES: List[str] = ['Ресторан 1', 'Ресторан 2']

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / '.env'
    )


settings = Settings()
