# Imagen base
FROM python:3.11-slim

# Crear carpeta de trabajo
WORKDIR /app

# Copiar e instalar librerias necesarias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código principal
COPY src/ .
# Copiar tests
COPY tests/ .

# Copiar archivos JSON de prueba
COPY src/samples/ /app/samples/

# Comando por defecto para ejecutar la aplicación
CMD ["python", "main.py"]
