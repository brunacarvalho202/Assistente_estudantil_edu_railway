"""Gerencia variáveis de configuração da aplicação.
Variáveis sensíveis (como GEMINI_API_KEY) são lidas de variáveis de ambiente.
"""

import os

def get_config_variables() -> dict:
    """Retorna as variáveis de configuração da aplicação.
    
    Todas as variáveis são lidas de variáveis de ambiente,
    que são injetadas pelo Railway na produção.
    """
    
    return {
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY"),
        "LLM_PROVIDER": os.environ.get("LLM_PROVIDER", "gemini"),
        "MODEL_NAME": os.environ.get("MODEL_NAME", "models/gemini-1.5-flash-001"),
        "ENV": os.environ.get("ENV", "local") 
    }