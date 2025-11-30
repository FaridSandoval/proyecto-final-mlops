FROM python:3.9-slim

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src/ ./src/

# Comando para correr la app
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]

# Configuración optimizada para producción