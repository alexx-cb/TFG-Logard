# Usa una imagen ligera de Python
FROM python:3.11-slim

# Evita que Python guarde archivos .pyc y buffer
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Crea y usa el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala paquetes del sistema necesarios para compilar dependencias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de requerimientos e instala dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia todo el proyecto dentro del contenedor
COPY . .

# Expón el puerto
EXPOSE 8000

# Comando para ejecutar el servidor
CMD gunicorn LogardBackEnd.wsgi:application --bind 0.0.0.0:$PORT --log-file -