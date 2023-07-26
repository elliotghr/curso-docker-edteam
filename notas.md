# Curso Docker

## 1 Introducción

## 1.1 - Introducción a Docker

Indice

- Contenedores
- Imagenes
- Docker Compose
- Desarrollo de aplicaciones

Una tecnología persiste en el tiempo dependiendo de quienes la usan

## 1.2 - Conceptos

- Docker es una cajita magica para correr mis aplicaciones, en cualquier lugar, sin complicaciones y eliminando el casico: "En mi computadora si funciona"
- El termino de contenedores no es algo nuevo dentro del entorno de Linux
- Docker se puede correr en diferentes SO, en la nube, e incluso dentro de una MV

  ![Alt text](image.png)

### Contenedor

Los contenedores son una abstracción en la capa de la aplicación que empaqueta el código y las dependencias juntos.

Esto significa que docker se ubica sobre la capa de infraestructura y posteriormente sobre el SO para poder correr nuestras aplicaciones haciendo uso de nuestra infraestructura y SO

![Alt text](image-1.png)

### MV

Las MV son una abstracción de hardware fisico que convierte un servidor en muchos servidores

Las MV ta,bién están sobre la infraestructura y el SO de nuestra máquina, sin embargo, estas traen su porpio SO, susprocesos, librerías y kernel, esto las hace más pesadas en tamaño (GB)

![Alt text](image-2.png)

### Diferencias

Docker es mucho más ligero, rápido y portable a comparación de un MV

## 1.3 - Instalación

Como alternativas existen:

- Docker desktop - Windows y MAC
  - Interfaz gráfica que nos permite ejecutar docker y administrar los containers
- Docker Engine para linux
- Play with docker
  - Plataforma web para correr docker a través de una interfaz web

### Conceptos

- Docker ce - Docker Community Edition
  - Contiene todas las herramientas básicas para iniciar
  - Existe una versión Enterprise
- Docker CLI - Interfaz de comando
  - Nos permite interactuar con el docker engine

## 1.4 - Arquitectura

### Docker Engine

Es el motor de Docker
Está conformado por 3 partes:

- Server (docker daemon)
  - Es nuestro proceso principal que nos ayuda a correr todos los contenedores en nuestro sistema
- REST API
  - Nos permite comunicarnos con el Server a través de ciertos comandos
- Client (docker CLI)
  - Desde aqui nos comunicamos al REST API a través de comandos que el REST API comunicará al Server

De esta manera nos podemos comunicar con Docker y manejar los containers, images, networks y data volumes

![Alt text](image-3.png)

## Arquitectura de docker

Está dividida en 3 secciones

- Client
  - Es el conjunto de comandos donde se especifican ciertas instrucciones para comunicarnos con Docker
  - Al escribir nuestras instrucciones/comandos nos comunicamos con el REST API que se comunica con el demonio de docker
- Docker Host
  - Es una especificación al demonio de docker y a lo que puede hacer en las imagenes y/o contenedores como:
    - Construir imagenes
    - Levantar contenedores
    - etc.
- Registry
  - Repositorio de imagenes disponibles
  - En caso de usar una imagen que no tengamos docker acudirá al Registry para poder utilizarla

Resumiendo el flujo, desde el Docker CLI enviamos comandos que la REST API manda al demonio de docker, el cual administra las imagenes y contenedores dependiendo de las especificaciones que enviemos, este puede acudir al Registry en caso de que no tengamos dicha imagen descargada

### Imagenes

Archivos ISO que nos funcionan para instalarlas en nuestros containers
Las imagenes puede ser:

- Python
- PHP
- Ruby
- etc.

![Alt text](image-4.png)

## 1.5 - Hola mundo

Comando para obtener imagenes desde Docker hub

```
sudo docker pull nginx
```

Especificando una versión de la imagen con :

```
sudo docker pull nginx:1.17-alpine
```

Comando para crear un container e inicializarlo (también descarga la imagen en caso de no tenerla localmente). También se exponen los puertos.

```
sudo docker run -p80:80 nginx:1.17-alpine
```

Docker se instala a nivel super su, por tanto, necesitamos hacer uso del comando sudo antes de cualquier comando de docker. Por tanto utilizaremos el siguiente comando para agregar un usuario al [grupo Docker](https://docs.docker.com/engine/install/linux-postinstall/), esto evita el uso repetitivo de sudo

```
sudo usermod -aG docker $USER
```
