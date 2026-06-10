# 1. Usar una imagen oficial de Python ligera
FROM python:3.11-slim

# 2. Establecer variables de entorno para optimizar Python en Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar las dependencias del sistema necesarias (opcional, por si usas librerías que compilan)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# 5. Copiar primero el archivo de requerimientos para aprovechar la caché de Docker
COPY requirements.txt .

# 6. Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copiar el resto del código de la aplicación
COPY . .

# 8. Exponer el puerto en el que corre la app
EXPOSE 8000

# 9. Comando para ejecutar la aplicación (Optimizado para producción)
CMD ["uvicorn", "api.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]