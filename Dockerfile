# Imagen base
FROM python:3.11-slim

# Crear carpeta de trabajo
WORKDIR /app

# Copiar código principal
COPY src/ .

# Copiar archivos JSON de prueba
COPY src/samples/ /app/samples/

# Comando por defecto para ejecutar la aplicación
ENTRYPOINT ["python", "main.py"]
