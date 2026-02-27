# Usa uma versão slim do Python 3.11 para reduzir o tamanho da imagem
FROM python:3.11-slim

# Define variáveis de ambiente para não gerar arquivos .pyc e não bufferizar logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para o psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# Expõe a porta padrão do Flask
EXPOSE 5000

# O comando padrão será o app, mas o docker-compose sobrescreverá para o worker
CMD ["python", "app.py"]
