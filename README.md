# ROAp - Repositorio de Objetos de Aprendizaje

Es una aplicación web que se encarga de administrar objetos de aprendizaje, almacena el objeto en si mismo (PDF, Vídeo, Audio etc.)
y los metadatos asociados a este bajo el estándar LOM (Learning Object Metadata).

# Construido con

## Backend
* Falcon
* MongoDB
* Redis

## Frontend
* ReactJS
* React Admin
* Material UI

ROAp esta construido siguiendo una arquitectura de microservicios con contendedores de Docker.

# Prerrequisitos
* Docker
* Docker Compose
* NPM

# Puesta en marcha

Debemos clonar el repositorio que contiene el código del frontend el cual se encuentra en https://github.com/gaia-unal/roap-ui

`git clone https://github.com/gaia-unal/roap-ui `

luego entramos al directorio clonado `roap-ui` y ejecutamos:

`npm install`

Esto instalará todas las dependencias del frontend.

Ahora, construimos el frontend:

`npm run-script build`

El comando anterior genera un directorio llamado `build`. Ahora tomamos este directorio y lo dejamos con todo su contenido en la carpeta `ui/`

Despues, vamos a la raíz del proyecto y generamos un archivo llamado `.env` con el contenido que tiene el archivo `.env_template`. En el archivo .env daremos valor a cada una de las variables de acuerdo a

```
JWT_SECRET=
DB_HOST=
DB_PORT=
DB_NAME=
SENDER_EMAIL=
SALT=
ACCOUNT_VALIDATION_URL=
RECOVER_PASSWORD_URL=
SENDGRID_API_KEY=
LOS_PER_PAGE_OAI_PMH=
ROAP_ADMIN=
MUST_CREATE_DEFAULT_LEARNING_OBJECTS=
```
...
