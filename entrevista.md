# ¿Por qué un contenedor pasa a estado Exited?

"Porque el proceso principal del contenedor terminó. En Docker, un contenedor solo permanece en ejecución mientras su proceso principal (PID 1) siga activo. Si ese proceso finaliza, el contenedor cambia al estado Exited, incluso si no ocurrió ningún error."

---

# Writable Layer vs Volume vs Bind Mount

## Writable Layer

Es la capa de escritura que Docker crea al iniciar un contenedor. Todos los cambios realizados dentro del contenedor se almacenan aquí.

- Pertenece al contenedor.
- Persiste mientras el contenedor exista (aunque esté detenido).
- Se elimina al borrar el contenedor.

**Uso:** archivos temporales, caché, pruebas.

## Docker Volume

Es un almacenamiento administrado por Docker e independiente del contenedor.

- Pertenece a Docker, no al contenedor.
- Sobrevive aunque el contenedor se elimine.
- Puede compartirse entre varios contenedores.

**Uso:** bases de datos, uploads y cualquier dato persistente.

**Ejemplo:**

```bash
docker volume create datos

docker run -v datos:/app ubuntu
```

## Bind Mount

Monta una carpeta del host dentro del contenedor.

- Los archivos viven en el host.
- Docker no administra esos archivos.
- Los cambios se reflejan inmediatamente en ambos lados.

**Uso:** desarrollo (CodeIgniter, Laravel, React, Node.js, etc.).

**Ejemplo:**

```bash
docker run -v $(pwd):/app ubuntu
```

## Comparación

|                                        | Writable Layer | Docker Volume | Bind Mount |
| -------------------------------------- | -------------- | ------------- | ---------- |
| ¿Dónde viven los datos?                | Contenedor     | Docker        | Host       |
| ¿Se pierden al eliminar el contenedor? | ✅ Sí          | ❌ No         | ❌ No      |
| ¿Docker administra los datos?          | Sí             | Sí            | No         |
| Uso principal                          | Temporales     | Persistencia  | Desarrollo |

## Regla para recordar

- **Writable Layer:** los datos viven **dentro del contenedor**.
- **Docker Volume:** los datos viven **en Docker**.
- **Bind Mount:** los datos viven **en el host**.

---

## Ejemplo de ejecución de un contenedor con variable de entorno

```bash
docker run --rm -e MSG="Elliot" --name alpine-dev alpine sh -c 'echo "hola $MSG"'
```

En este ejemplo, se crea un contenedor a partir de la imagen `alpine`, se establece la variable de entorno `MSG` con el valor "Elliot", y se ejecuta un comando que imprime "hola Elliot". El contenedor se elimina automáticamente después de que el comando finaliza debido a la opción `--rm`.

- sh: shell que se ejecuta dentro del contenedor.
- -c: permite pasar un comando como argumento a la shell.
- --rm: elimina el contenedor automáticamente después de que finaliza.
- echo: comando que imprime el mensaje en la salida estándar.

En el comando se usa `sh -c` para ejecutar un comando **dentro** del contenedor. A comparación, si se ejecutara `docker run --rm -e MSG="Elliot" --name alpine-dev alpine echo "hola $MSG"`, el contenedor imprimiría "hola " (sin el valor de la variable) porque la variable de entorno no se expandiría correctamente en ese contexto, el contexto sería el del host, no el del contenedor.

---

# Docker - `ARG` vs `ENV`

## `ARG`

- Existe **solo durante la construcción de la imagen** (`docker build`).
- Se utiliza para parametrizar el proceso de construcción.
- **No** está disponible cuando el contenedor se está ejecutando.

### Ejemplo

```dockerfile
FROM php:8.3-apache

ARG APP_VERSION=1.0

RUN echo "Versión: $APP_VERSION"
```

Construcción:

```bash
docker build --build-arg APP_VERSION=2.0 -t mi-app .
```

Una vez creada la imagen:

```bash
docker run mi-app env
```

`APP_VERSION` **no aparecerá**.

## `ENV`

- Existe durante el `docker build` y también cuando el contenedor está en ejecución.
- Se utiliza para variables de configuración que la aplicación necesita al ejecutarse.
- Puede sobrescribirse al iniciar un contenedor con `docker run -e`.

### Ejemplo

```dockerfile
FROM php:8.3-apache

ENV APP_ENV=production
ENV TZ=America/Mexico_City
```

Al ejecutar:

```bash
docker run mi-app env
```

Salida:

```text
APP_ENV=production
TZ=America/Mexico_City
```

## Diferencias

| Característica                            |     `ARG`     |     `ENV`      |
| ----------------------------------------- | :-----------: | :------------: |
| Disponible durante `docker build`         |      ✅       |       ✅       |
| Disponible al ejecutar el contenedor      |      ❌       |       ✅       |
| Se puede pasar desde la línea de comandos | `--build-arg` | `-e` / `--env` |
| Se guarda en la imagen                    |      ❌       |       ✅       |

## ¿Cuándo usar cada uno?

### Usa `ARG` cuando...

- Necesites un valor **solo para construir la imagen**.
- Quieras parametrizar el `Dockerfile`.

Ejemplos:

- Versión de una dependencia.
- Flags de Composer (`--no-dev`).
- Rama de Git a clonar.
- URL de descarga durante el build.

### Usa `ENV` cuando...

- La aplicación necesite la variable al ejecutarse.
- Sea una configuración del contenedor.

Ejemplos:

- `APP_ENV`
- `TZ`
- `APACHE_DOCUMENT_ROOT`
- `DB_HOST`
- `PORT`

> **Nota:** Variables sensibles como `DB_PASSWORD`, `API_KEY` o `SECRET_KEY` no deberían quedar fijas en el `Dockerfile`. Es preferible inyectarlas al ejecutar el contenedor (`docker run -e`, `docker compose`, archivos `.env` o un gestor de secretos).

## Ejemplo real (CodeIgniter 4)

```dockerfile
FROM php:8.3-apache

ARG COMPOSER_FLAGS="--no-dev"

RUN composer install $COMPOSER_FLAGS

ENV TZ=America/Mexico_City
ENV APACHE_DOCUMENT_ROOT=/var/www/html/public
```

### ¿Por qué?

- `COMPOSER_FLAGS` solo se necesita durante la construcción → **`ARG`**.
- `TZ` y `APACHE_DOCUMENT_ROOT` deben existir cuando el contenedor se ejecuta → **`ENV`**.

## Regla para entrevistas

Pregúntate:

> **¿La variable debe existir cuando el contenedor ya está corriendo?**

- **Sí** → `ENV`
- **No, solo durante el build** → `ARG`

---

# Docker - `ARG` con valor por defecto y `ENV`

## `ARG` sin valor por defecto

```dockerfile
ARG APP_ENV
ENV APP_ENV=$APP_ENV
```

- Si **no** se pasa `--build-arg`, `APP_ENV` queda vacío.
- Si se pasa `--build-arg`, ese valor se copia a `ENV`.

Ejemplo:

```bash
docker build --build-arg APP_ENV=development -t mi-app .
```

Resultado:

```text
APP_ENV=development
```

## `ARG` con valor por defecto

```dockerfile
ARG APP_ENV=production
ENV APP_ENV=$APP_ENV
```

El valor de `production` actúa como **valor por defecto**.

Si se construye sin `--build-arg`:

```bash
docker build -t mi-app .
```

Resultado:

```text
APP_ENV=production
```

Si se construye con:

```bash
docker build --build-arg APP_ENV=testing -t mi-app .
```

Resultado:

```text
APP_ENV=testing
```

## ¿Por qué usar `ARG` + `ENV`?

Permite construir imágenes con distintos valores sin modificar el `Dockerfile`.

```dockerfile
ARG APP_ENV=production
ENV APP_ENV=$APP_ENV
```

Ejemplos:

```bash
docker build --build-arg APP_ENV=development -t app-dev .
docker build --build-arg APP_ENV=testing -t app-test .
docker build --build-arg APP_ENV=production -t app-prod .
```

Cada imagen conservará el valor de `APP_ENV` con el que fue construida.

## Prioridad de las variables

1. `docker run -e` (mayor prioridad)
2. `ENV` del `Dockerfile`
3. `ARG` (solo existe durante `docker build`)

Ejemplo:

```dockerfile
ENV APP_ENV=production
```

```bash
docker run -e APP_ENV=testing mi-app
```

Resultado dentro del contenedor:

```text
APP_ENV=testing
```

> `docker run -e` sobrescribe el valor definido con `ENV`.

## Regla rápida

- **¿Se necesita solo durante `docker build`?** → `ARG`
- **¿Se necesita cuando el contenedor está ejecutándose?** → `ENV`

> `ARG` puede tener un valor por defecto, el cual será utilizado si no se proporciona `--build-arg`.

---

# Docker - Caché de capas (Layer Cache)

## ¿Cómo funciona la caché?

Docker construye una imagen **capa por capa**.

Cada instrucción del `Dockerfile` genera una nueva capa:

```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Si una capa **no cambia**, Docker reutiliza su caché.

Si una capa **cambia**, Docker invalida esa capa y **todas las posteriores**.

## Regla de oro

> **Si una capa cambia, Docker invalida esa capa y todas las capas posteriores. Las capas anteriores siguen reutilizándose.**

## Ejemplo

### Build 1

Primera construcción:

```bash
docker build -t mi-app .
```

Docker ejecuta todas las capas.

### Build 2

Solo cambia:

```text
app.py
```

Capas reutilizadas:

```text
FROM                  ✅
WORKDIR               ✅
COPY requirements.txt ✅
RUN pip install       ✅
COPY . .              ❌
CMD                   (sin costo)
```

No se vuelven a instalar las dependencias.

### Build 3

Ahora cambia:

```text
requirements.txt
```

Capas reutilizadas:

```text
FROM                  ✅
WORKDIR               ✅
COPY requirements.txt ❌
RUN pip install       ❌
COPY . .              ❌
CMD                   (sin costo)
```

Como cambió `requirements.txt`, también se invalida `pip install` y todas las capas posteriores.

# Optimización de Dockerfiles

## ❌ Mala práctica

```dockerfile
FROM python:3.12

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

Problema:

- Cualquier cambio en el proyecto invalida `COPY . .`.
- Docker vuelve a ejecutar `pip install` en cada build.

## ✅ Buena práctica

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Ventajas:

- Las dependencias solo se reinstalan cuando cambia `requirements.txt`.
- Los builds son mucho más rápidos.

# Caso de Composer (PHP / CodeIgniter)

## ✅ Recomendado

```dockerfile
FROM php:8.3-apache

WORKDIR /var/www/html

COPY composer.json composer.lock ./

RUN composer install --no-dev

COPY . .
```

¿Por qué?

- `composer.json` y `composer.lock` cambian con poca frecuencia.
- El código fuente cambia constantemente.
- Docker reutiliza la caché de `composer install` mientras las dependencias no cambien.

Si primero se hiciera:

```dockerfile
COPY . .
```

cualquier cambio en el código invalidaría la capa y Composer volvería a instalar todas las dependencias.

# Buenas prácticas

- Coloca primero los archivos que cambian poco.
- Ejecuta después los procesos costosos (`composer install`, `npm install`, `pip install`, etc.).
- Copia el resto del proyecto al final.

Esto maximiza el uso de la caché y reduce significativamente el tiempo de construcción de la imagen.

# Regla para entrevistas

Cuando veas un `Dockerfile`, pregúntate:

1. ¿Qué archivos cambian con poca frecuencia?
2. ¿Qué instrucciones son costosas de ejecutar?
3. ¿Estoy copiando más archivos de los necesarios antes de instalar dependencias?

Si la respuesta es sí, probablemente el `Dockerfile` pueda optimizarse aprovechando mejor la caché de Docker.

---

# Docker - Red interna vs acceso desde el host

## Comunicación entre contenedores

Los contenedores que pertenecen a la misma red de Docker pueden comunicarse entre sí utilizando:

- El nombre del servicio (`docker-compose.yml`)
- El nombre del contenedor (aunque es preferible usar el nombre del servicio)

Ejemplo:

```yaml
services:
  app:
    build: .

  mysql:
    image: mysql:8
```

Desde `app`:

```text
Host: mysql
Puerto: 3306
```

No es necesario publicar el puerto de MySQL.

## Comunicación desde el host

Para acceder desde:

- Navegador
- Postman
- DBeaver
- MySQL Workbench

es necesario publicar el puerto.

Ejemplo:

```yaml
services:
  app:
    build: .
    ports:
      - "8080:80"
```

Ahora el navegador puede acceder a:

```text
http://localhost:8080
```

## ¿Cuándo usar `ports`?

### Sí

Cuando un programa que corre en el host necesita acceder al contenedor.

Ejemplos:

- Navegador
- DBeaver
- Postman
- curl

### No

Cuando únicamente otros contenedores necesitan comunicarse.

Ejemplo:

```text
CodeIgniter → MySQL
```

La comunicación ocurre por la red interna de Docker.

## Regla para entrevistas

> Los contenedores de una misma red no necesitan `ports` para comunicarse entre ellos. `ports` solo sirve para permitir el acceso desde el host hacia un contenedor.

---

# Docker - `EXPOSE` vs `ports`

## `EXPOSE`

Se define en el `Dockerfile`.

```dockerfile
EXPOSE 80
```

Indica que la aplicación escucha en ese puerto dentro del contenedor.

No publica el puerto hacia el host.

Es una instrucción informativa para Docker y para otros desarrolladores.

## `ports`

Se define al ejecutar el contenedor.

Ejemplo en Docker Compose:

```yaml
ports:
  - "8080:80"
```

o con Docker:

```bash
docker run -p 8080:80 nginx
```

Crea el mapeo:

```text
Host:8080
        │
        ▼
Contenedor:80
```

Ahora el host puede acceder al contenedor.

## Diferencias

| `EXPOSE`                        | `ports`                         |
| ------------------------------- | ------------------------------- |
| Dockerfile                      | docker-compose / docker run     |
| Documenta el puerto interno     | Publica el puerto al host       |
| No permite acceso desde el host | Sí permite acceso desde el host |

## Regla para entrevistas

> `EXPOSE` no abre puertos al exterior. Solo indica qué puerto utiliza la aplicación. Para acceder desde el host es necesario usar `ports` o `docker run -p`.

---

# Docker - `RUN` vs `CMD` vs `ENTRYPOINT`

## `RUN`

Se ejecuta **durante la construcción de la imagen** (`docker build`).

Se utiliza para instalar paquetes, copiar archivos, compilar código o preparar el entorno.

Ejemplo:

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y curl
```

Una vez construida la imagen, `RUN` **no vuelve a ejecutarse** al iniciar un contenedor.

---

## `CMD`

Define el **comando por defecto** que ejecutará el contenedor al iniciarse.

Puede ser reemplazado al ejecutar `docker run`.

Ejemplo:

```dockerfile
FROM ubuntu

CMD ["echo", "Hola Mundo"]
```

```bash
docker run mi-imagen
```

Resultado:

```text
Hola Mundo
```

Si se ejecuta:

```bash
docker run mi-imagen ls -la
```

Docker reemplaza completamente el `CMD` y ejecuta:

```bash
ls -la
```

---

## `ENTRYPOINT`

Define el **ejecutable principal** del contenedor.

Generalmente **no se reemplaza**; los argumentos que se pasan con `docker run` se agregan al `ENTRYPOINT`.

Ejemplo:

```dockerfile
FROM ubuntu

ENTRYPOINT ["echo"]
```

```bash
docker run mi-imagen Hola
```

Docker ejecuta:

```bash
echo Hola
```

---

## `ENTRYPOINT` + `CMD`

Se utilizan juntos para definir:

- `ENTRYPOINT` → programa principal.
- `CMD` → argumentos por defecto.

Ejemplo:

```dockerfile
FROM ubuntu

ENTRYPOINT ["python"]

CMD ["app.py"]
```

Al ejecutar:

```bash
docker run mi-app
```

Docker ejecuta:

```bash
python app.py
```

Si ejecutas:

```bash
docker run mi-app otro.py
```

Docker ejecuta:

```bash
python otro.py
```

El `ENTRYPOINT` permanece igual; únicamente cambia el `CMD`.

---

# ¿Cuándo usar cada uno?

### `RUN`

Cuando necesitas preparar la imagen durante el build.

Ejemplos:

- Instalar dependencias.
- Actualizar paquetes.
- Compilar código.
- Crear directorios.

---

### `CMD`

Cuando quieres definir un comando por defecto que el usuario pueda reemplazar fácilmente.

Ejemplo:

```dockerfile
CMD ["php", "spark", "serve"]
```

---

### `ENTRYPOINT`

Cuando el contenedor siempre debe ejecutar un programa específico.

Ejemplos:

- MySQL
- Redis
- PostgreSQL
- Nginx

---

# Diferencias

| Instrucción  | ¿Cuándo se ejecuta?      | ¿Se puede reemplazar?                    | Uso principal       |
| ------------ | ------------------------ | ---------------------------------------- | ------------------- |
| `RUN`        | Durante `docker build`   | No aplica                                | Construir la imagen |
| `CMD`        | Al iniciar el contenedor | Sí                                       | Comando por defecto |
| `ENTRYPOINT` | Al iniciar el contenedor | Normalmente no (solo con `--entrypoint`) | Programa principal  |

---

# Regla rápida

- **`RUN`** → Construye la imagen.
- **`CMD`** → Define qué hacer por defecto al iniciar el contenedor.
- **`ENTRYPOINT`** → Define qué programa debe ejecutarse siempre.

---

# Ejemplo completo

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python"]

CMD ["app.py"]
```

¿Qué ocurre?

- `RUN pip install...` se ejecuta **una sola vez** durante el `docker build`.
- Al ejecutar `docker run mi-app`, Docker lanza:

```bash
python app.py
```

- Si ejecutas:

```bash
docker run mi-app otro.py
```

Docker lanza:

```bash
python otro.py
```

porque `otro.py` reemplaza el `CMD`, pero el `ENTRYPOINT` sigue siendo `python`.

---

# Notas Extra

- docker run → crea un contenedor nuevo a partir de una imagen.
- docker start → inicia un contenedor existente.
- docker exec → ejecuta un comando dentro de un contenedor que ya está en ejecución.
