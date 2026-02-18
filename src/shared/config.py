"""
Configuration managment module
code uses pydantic settings to safely load and validate your .env file
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Application settings schema
    Attributes:
    Openai_api_key : key for ai models
    openai_model_name : model identifier
    firecrawl api key :  key for firecrawl
    langchain_api_key : langsmith tracing 
    """

    openai_api_key : str = Field(..., description = "Open AI API Key for llm agents")
    openai_model_name : str = Field("gpt-4o, " ,description = "The openai model name")
    firecrawl_api_key : str = Field(..., description = "API key for firecrawl scrapping data")
    LANGSMITH_API_KEY : Optional[str] = Field(..., description = "langsmith api key")
    database_url: str = Field(..., env="DATABASE_URL", description="Azure Postgres connection string")
    azure_blob_storage_connection_string : Optional[str] = Field(None, description = "azure blob connection str")


    # pydantic config : 
    model_config = SettingsConfigDict(env_file = ".env",
                                      env_file_encoding = "utf-8",
                                      extra = "ignore")

@lru_cache()
def get_settings() -> Settings:
    """
    creates and cache the settings object.
    """
    return Settings()
settings = get_settings()

