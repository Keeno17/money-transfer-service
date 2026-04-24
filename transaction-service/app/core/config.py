import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SERVICE_API_KEY = os.getenv("SERVICE_API_KEY")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


class Settings:
    APP_NAME = "Money Transfer"


settings = Settings()
