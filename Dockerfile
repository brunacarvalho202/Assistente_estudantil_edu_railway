# Use a imagem base Python
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Instalar o supervisord
RUN apt-get update && \
    apt-get install -y supervisor curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de dependência e instalá-los
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar toda a aplicação
COPY . /app/

# Expor portas (FastAPI e Streamlit)
EXPOSE 8000 8501

# Health check para Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando final: iniciar o supervisord
CMD ["/usr/bin/supervisord", "-c", "supervisord.conf"]