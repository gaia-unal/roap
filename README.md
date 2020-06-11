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

El comando anterior genera un directorio llamado `build`. Ahora tomamos este directorio y lo movemos junto a su contenido a la carpeta `ui/`

Despues, vamos a la raíz del proyecto y generamos un archivo llamado `.env` con el contenido que tiene el archivo `.env_template`. Algunos de estos tienen un valor por defecto, otros, pueden ser cambiados de acuerdo a la tabla.

```
JWT_SECRET=
DB_HOST=db
DB_PORT=27017
DB_NAME=roap
SENDER_EMAIL=roap.unal.master@gmail.com
SALT=
ACCOUNT_VALIDATION_URL=http://gaia.manizales.unal.edu.co:8081/#/user-validate
RECOVER_PASSWORD_URL=http://gaia.manizales.unal.edu.co:8081/#/recover-password
SENDGRID_API_KEY=
LOS_PER_PAGE_OAI_PMH=100
ROAP_ADMIN=gaia_man@unal.edu.co
MUST_CREATE_DEFAULT_LEARNING_OBJECTS=0
```
A cotinuación se ofrece una breve explicación de cada una de estas variables y del valor que debería tomar:

| Variable                             | Descripción                                                                                                                                                                                                                                                      |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| JWT_SECRET                           | Cadena aleatoria que servirá para generar la firma del token JWT                                                                                                                                                                                                 |
| DB_HOST                              | Host en el que corre MongoDB. El valor por defecto es `db`, si va a ser cambiado debe tenerse en cuenta el contenido del archivo  `docker-compose.yml` puntualmente el service `db`                                                                              |
| DB_PORT                              | Puerto en el que MongoDB escucha. El valor por defecto es `27017`, si va a ser cambiado debe tenerse en cuenta el contenido del archivo `docker-compose.yml` puntualmente el service `db`                                                                        |
| DB_NAME                              | Nombre de la base de datos. El valor por defecto es `roap`                                                                                                                                                                                                       |
| SENDER_EMAIL                         | Correo desde el que se envían los emails generados (confirmación de cuenta, recuperación de contraseña etc.)desde la app.                                                                                                                                        |
| SALT                                 | Cadena aleatoria que ayuda a proteger las contraseñas.                                                                                                                                                                                                           |
| ACCOUNT_VALIDATION_URL               | Esta variable se usa para almacenar el enlace que permita la validación de una cuenta recien creada. El valor por defecto es `http://gaia.manizales.unal.edu.co:8081/#/user-validate` el cual debe ser cambiado de acuerdo a donde vaya a correr ROAp.           |
| RECOVER_PASSWORD_URL                 | Esta variable se usa para almacenar el enlace que permita la recuperación de la contraseña de una cuenta. El valor por defecto es  `http://gaia.manizales.unal.edu.co:8081/#/recover-password`  el cual debe ser cambiado de acuerdo a donde vaya a correr ROAp. |
| SENDGRID_API_KEY                     | API key generada en Sendgrid.                                                                                                                                                                                                                                    |
| LOS_PER_PAGE_OAI_PMH                 | Cantidad de objetos que va a devolver la aplicación ante una petición mediante el protocolo OAI-PMH. El valor por defecto es `100`.                                                                                                                              |
| ROAP_ADMIN                           | Correo del administrador de ROAp. El valor por defecto es el correo GAIA.                                                                                                                                                                                        |
| MUST_CREATE_DEFAULT_LEARNING_OBJECTS | Esta variable permite precargar objetos de aprendizaje al momento de levantar la aplicación. Si el valor es 1 el buscará en la ubicación adecuada los objetos a cargar, si es 0 no lo hará.                                                                      |

### Precarga de objetos de aprendizaje (Opcional)
Dejar cada uno de los OA a precargar en la siguiente ruta `roap/learning_object/default_files/files/`

Dejar cada uno de los archivos XML con los metadatos de cada objeto en `roap/learning_object/collection/setup/default_learning_objects_xml/`

### Construcción
Luego de tener cada una de las variables del archivo .env con el valor adecuado, ejecutamos el siguiente comando en la raíz del proyecto:

`docker-compose up --build`

Este comando se encargará de construir cada uno de los servicios que componen a ROAp. Una vez termine su ejecución deberíamos poder acceder a la aplicación en http://localhost:8081/
