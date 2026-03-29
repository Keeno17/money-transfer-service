import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class Settings:
    APP_NAME = "Money Transfer"

settings = Settings()