from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    ENCRYPTION_KEY: str
    ALCHEMY_RPC_URL: str
    INFURA_RPC_URL: str
    COINGECKO_API_KEY: str
    CAPSOLVER_API_KEY: str
    BRIGHTDATA_PROXY_URL: str
    TELEGRAM_BOT_TOKEN: str
    WALLET_CONNECT_PROJECT_ID: str
    REDIS_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
