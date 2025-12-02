"""Configuração da Aplicação - Migrada para Railway

Railway injeta as variáveis de ambiente diretamente.
As variáveis sensíveis (como GEMINI_API_KEY) são definidas no painel do Railway.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os
from dotenv import load_dotenv

# Carregar .env apenas em desenvolvimento local
if os.environ.get("ENV", "local") != "production":
    load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Edu Assistente"
    ENV: str = Field(default="local", description="Ambiente da aplicação")
    LLM_PROVIDER: str = Field(default="gemini", description="Provedor LLM")
    MODEL_NAME: str = Field(default="models/gemini-1.5-flash-001", description="Modelo padrão")
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Chave da API Gemini")
    CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia global - sempre disponível para a app
settings = Settings()
