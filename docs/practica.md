# Práctica 2: (Docker)

## Contexto

En esta práctica construirás un **Linktree**: una página web donde tienes enlaces a tus redes sociales y otros sitios de interés.

**Duración sugerida:** 4 horas.

## Producto final esperado

Una página que permite dar clicka a botones para visitar rus redes sociales, blogs personales o sitios de interés. El diseño es libre, pero debe incluir:

- botones o tarjetas hacia  algunos sitios de interes.
- Una fotografia cualquiera (puede ser tuya o una imagen de stock).

## Habilidades que repasa

### HTML

- Etiquetas comunes y HTML5 semántico para poder hardcodear la informacion en las etiquetas.

### CSS

- Para poder darle estilo a la pagina.

### JavaScript

- DOM: `querySelector`, eventos
- HTTP: `fetch`
- Renderizado en DOM (actualizar texto/atributos)

### Docker
- Dockerfile: `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`
- Comandos: `docker build`, `docker run`, `docker ps`, `docker logs`, `docker stop`, `docker rm`, `docker rmi`, `docker images`y`docker exec`.
- Volúmenes: `-v`
- Puertos: `-p <host_port>:<container_port>`
-banderas: `--rm`, `-d`, `--name`, `-it` y `-t`
- docker-compose.yml: `services`, `build`, `ports`, `volumes`, `depends_on`, `context`y `dockerfile`.
- docker compose: `docker-compose.yml`, `docker compose build` y `docker compose up`



## Guías para la práctica

### Paso 1: Verificar el funcionamiento del frontend en docker

1. Verificar que docker esté instalado y funcionando correctamente ejecutando `docker --version` y entrar a la carpeta de `Front`para ejecutar `docker build -t front:1.0.0 .` y luego `docker run -it --rm -d -p 8080:80 --name Front front:1.0.0` para verificar que la aplicación se levanta correctamente.

2. Verificar que la aplicación se levanta correctamente accediendo a `http://localhost:8080` en tu navegador.

### Paso 2: Verificar el funcionamiento del backend en docker

1. Verificar que docker esté instalado y funcionando correctamente ejecutando `docker --version` y entrar a la carpeta de `Back` para ejecutar `docker build -t back:1.0.0 .` y luego `docker run -it --rm -d -p 5000:5000 --name Back back:1.0.0` para verificar que la aplicación se levanta correctamente.

2. Verificar que la aplicación se levanta correctamente accediendo a `http://localhost:5000/persona` en tu navegador o usando `curl` para verificar que la API responde correctamente.

3. Aqui tendran un error  de acceso deberan solucionarlo.

### Paso 3: Levantar ambos servicios y probar la comunicación entre ellos.

1. Levantar ambos servicios usando `docker run` para cada uno, asegurándose de mapear los puertos correctamente (8080 para el frontend y 5000 para el backend).

2. Verificar que el frontend puede comunicarse con el backend accediendo a `http://localhost:8080` y verificando que los datos del backend se muestran correctamente en la interfaz del frontend.

3. Detener ambos contenedores usando `docker stop`.

### Paso 4: Usar docker-compose para levantar ambos servicios juntos.

1. Crear un archivo `docker-compose.yml` en la raíz del proyecto con la configuración necesaria para levantar ambos servicios (frontend y backend) juntos.

2. Hacer el build de ambos servicios usando `docker compose build`.

3. Levantar ambos servicios usando `docker compose up` y verificar que ambos servicios se levantan correctamente y pueden comunicarse entre sí.

### Paso 5: Configurar volúmenes para desarrollo.

1. Modificar el `docker-compose.yml` para incluir volúmenes que permitan mapear el código fuente del frontend y backend desde tu máquina local al contenedor, de modo que puedas hacer cambios en el código sin tener que reconstruir la imagen cada vez.

## Entregables

1. **Funcionalidad:** la aplicación debe funcionar correctamente, mostrando los datos del backend en el frontend y permitiendo la comunicación entre ambos servicios.

2. **README.md (obligatorio)** con:
   - **Datos del alumno** (nombre, grupo, correo)
   - **Cómo ejecutar** (pasos y comandos)
   - **Problemas/incidencias** (qué se te complicó y cómo lo resolviste o qué quedó pendiente)
   - (opcional) captura de pantalla

## Referencias sugeridas

### Referencias generales

- [cheatsheets Docker](https://dockerlabs.collabnix.com/docker/cheatsheet/)
- [documentacion Docker](https://docs.docker.com)

### Donde practicar Docker

- [Play with Docker](https://www.docker.com/play-with-docker/)
