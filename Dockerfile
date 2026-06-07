# Usamos una imagen liviana oficial de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Evita que Python escriba archivos .pyc en el disco
ENV PYTHONDONTWRITEBYTECODE 1
# Evita que Python guarde en buffer los textos de salida (para ver los logs en tiempo real)
ENV PYTHONUNBUFFERED 1

# Copiamos primero el archivo de dependencias para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código del backend al contenedor
COPY . .

# Exponemos el puerto en el que corre la API
EXPOSE 8000

# Comando para ejecutar la aplicación en producción (sin --reload)
CMD ["uvicorn", "api.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]