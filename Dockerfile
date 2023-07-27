# Esto es un comentario

# Imagen base
FROM ubuntu

# Ejecutar comando dentro de la imagen (construcción)
RUN apt-get update
RUN apt-get install python3 python3-dev -y
RUN mkdir /app

# Definir mi directorio de trabajo
WORKDIR /app

# Definimos una variable de entorno
ENV MSG='Saludos a todos ✌'

# Copiar archivos a mi contenedor
# ADD index.html .
ADD . .
# O de otra manera...
# ADD index.html /app

# No lo ocuparemos por ahora
# COPY source dest

# Ejecuta comandos (cuando está corriendo la imagen)
CMD python3 -m http.server 5000


# Exponer puertos
EXPOSE 5000