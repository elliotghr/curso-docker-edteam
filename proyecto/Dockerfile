FROM python:3

# Actualizamos repositorios
RUN apt-get update
# Instalamos libpq-dev que permitirá la conexión a la DB de postgres
RUN apt-get install libpq-dev -y
# Creamos un directorio /app
RUN mkdir /app

# Definimos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos de nuestra ruta a /app (.)
ADD . .

# Instalamos las dependencias y librerías 
RUN pip install -r requirements.txt

# Ejecutamos el comando dentro del contenedor para correr el programa
CMD python app.py

# Exponemos el código en el puerto 5000
EXPOSE 5000