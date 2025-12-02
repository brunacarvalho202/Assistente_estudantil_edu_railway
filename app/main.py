from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.chat import router as chat_router

def create_app() -> FastAPI:
    """
    Cria a instância principal da aplicação FastAPI.
    Isolado em função para facilitar testes.
    """
    app = FastAPI(
        title="LLM Chat API",
        version="1.0.0",
        description="API modular para comunicação com modelos de linguagem.",
    )

    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health Check Endpoints (requerido pelo Railway)
    @app.get("/health")
    async def health_check():
        """Health check simples para Railway"""
        return JSONResponse(
            status_code=200,
            content={"status": "healthy", "environment": settings.ENV}
        )

    @app.get("/docs")
    async def docs_redirect():
        """Documentação interativa (Swagger UI)"""
        # FastAPI redireciona automaticamente para /docs
        pass

    @app.get("/")
    async def root():
        """Endpoint raiz com informações da API"""
        return {
            "app_name": settings.APP_NAME,
            "version": "1.0.0",
            "environment": settings.ENV,
            "status": "running",
            "docs": "/docs",
            "health": "/health",
            "endpoints": {
                "chat": "/chat/"
            }
        }

    # Rotas da aplicação
    app.include_router(chat_router)

    return app


app = create_app()

