# Usa la imagen oficial de Python
FROM python:3.11

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Mueve al directorio api, donde está app.py
WORKDIR /app/api

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expone el puerto en el que corre Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
