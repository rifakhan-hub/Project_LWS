# settings

import os
from dotenv import load_dotenv
from pydantic import Basemodel

class Settings(Basemodel):
    database_url: str = "sqlite:///./bloodbank.db"
    secret_key: str = "bloodbankmanagmentsystem"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

settings = Settings(
    database_url=os.getenv("BB_DATABASE_URL", "sqlite:///./bloodbank.db"),
    secret_key=os.getenv("BB_SECRET_KEY", "bloodbankmanagmentsystem"),
    algorithm=os.getenv("BB_ALGORITHM", "HS256"),
    access_token_expire_minutes=os.getenv("BB_ACCESS_TOKEN_EXPIRE_MINUTES", 60),
)

# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     database_url: str = "sqlite:///./bloodbank.db"
#     secret_key: str = "bloodbankmanagmentsystem"
#     algorithm: str = "HS256"
#     access_token_expire_minutes: int = 60
    
#     model_config = SettingsConfigDict(
#         env_file=".env",   
#         env_prefix="BB_",
#     )
# settings = Settings()