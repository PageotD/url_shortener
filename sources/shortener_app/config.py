"""
This module contains the configuration settings for the shortener application.
It uses the Pydantic library to manage settings and environment variables.
"""

# pydantic is automatically installed with FastAPI
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Settings class to store application configuration using Pydantic BaseSettings.
    
    Attributes:
        env_name (str): The name of the environment (default is "Local").
        base_url (str): The base URL for the application (default is "http://localhost:8000").
        db_url (str): The database URL for the application (default is "sqlite:///./shortener.db").
    """
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    """
    Function to get the current settings for the application.
    
    Returns:
        Settings: The current settings for the application.
    """
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
