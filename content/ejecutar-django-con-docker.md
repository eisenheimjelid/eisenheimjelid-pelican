Title: Ejecutar Django con Docker
Date: 2017-07-07 22:20
Category: Docker
Tags: linux,django,docker,
Slug: ejecutar-django-con-docker
Authors: David León
Summary: Docker es una excelente herramienta que nos permite aislar y ejecutar en entornos controlados, casi cualquier tipo de aplicativo sobre nuestro sistema operativo. Hasta el momento es compatible con las versiones más recientes de Windows, Mac y Linux.




Iniciando con lo acostumbrado, el ambiente que he utilizado es **GNU/Linux Debian 9 (Stretch) y Ubuntu 16.04 LTS**, para realizar los ejemplos del artículo. Aunque también vale aclarar lo que es [Docker](https://www.docker.com/ "Docker"), antes que nada: **Docker** es un herramienta de código abierto que automatiza el despliegue de aplicaciones dentro de contenedores, proporcionando una capa adicional de abstracción y automatización de Virtualización a nivel de sistema operativo en Linux.

![terminal](/theme/assets/img/docker-django.png)

Aunque también existen otras definiciones más apegadas a su funcionalidad, como: **Docker** es una herramienta que puede empaquetar una aplicación y sus dependencias en un contenedor virtual, para ser ejecutado en cualquier servidor Linux. Esto ayuda a permitir la flexibilidad y portabilidad en donde la aplicación se puede ejecutar, ya sea en las instalaciones físicas, la nube pública, nube privada, etc.

Además de esto, **Django** es un framework Web programado en Python, que nos ayuda y aventaja en muchas características necesarias y recurrentes al momento de trabajar aplicaciones Web. Y aunque de hecho, es una herramienta que menciono mucho en mi sitio, y una de las mejores desde mi punto de vista; e incluso me identifico mucho con su slogan: _con las baterias incluidas_.

Una aclaración necesaria, es que esta configuración es para ejecutar **Django** en un modo de _desarrollo_ o _pruebas_, dado que el uso del servidor web propio de django, nunca se ha recomendado para entoernos productivos; y en ese caso sería mejor utilizar **uwsgi** e interconectarlo con **Apache** o **Nginx**.


### Empezamos con Dockerfile y docker-compose.yml

Primero, de acuerdo al tutorial que nos proporciona el sitio oficial de Docker, creamos un par de archivos y los ejecutamos para obtener las dependencias necesarias para hacer funcionar Django adecuadamente.

##### Dockerfile

Con pocas variantes respecto al tutorial original de docker, separamos en dos carpetas el código (code) y los archivos estáticos o assets (html), además de indicar una carpeta para las plantillas de Django (templates), dejando el archivo como se muestra:

```
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN mkdir -p /var/www/website/html
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./example /code/
ADD ./html /var/www/website/html
ADD ./example/templates /var/www/website/example/templates

```

'example' es como he decidido nombrar el proyecto, lo vamos a revisar un poco más adelante.

##### docker-compose.yml

Con pocas variantes respecto al tutorial original de docker, indicamos el uso del manejador de base de datos **PostgreSQL** y la configuración con la que va a funcionar Django al momento de arrancar el contenedor (_esto es para solo un modo de pruebas o desarrollo_):


```
version: '3'
services:
  db:
    restart: always
    image: postgres
  web:
    restart: always
    build: .
    command: python3 manage.py runserver 0.0.0.0:8001
    volumes:
      - ./example:/code
      - ./html:/var/www/website/html
      - ./example/templates:/var/www/website/example/templates
    ports:
      - "8001:8001"
    depends_on:
      - db
```

##### requirements.txt

Por último, no menos importante, pero ya casi se me olvidaba; cuando trabajamos con proyectos de **Python**, una buena práctica es siempre utilizar el archivo 'requirements.txt', para definir y poder indicar a cualquier otra persona los paquetes y dependencias que requerimos para poder volver a utilizar nuestro código, sin que se tenga que romper la cabeza con las dependencias, con *pip*.

```
Django
psycopg2
WeasyPrint
djangorestframework
```

En este caso, lo que usualmente utilizo es Django en su versión más reciente. Aunque puedes especificar una versión en concreto de cada paquetes colocando doble igual, de esta forma '==1.8'. El paquete de **pyscopg2** sirve de controlador para poder conectarnos a PostgreSQL, el de **WeasyPrint** sirve para convertir HTML a PDF, bastante útil y pocas veces he llegado a precindir de este. Además, **djangorestgramework** es el mejor paquete para hacer "bien" cualquier servicio RESTful que queramos programar.

### Ahora unos comandos para hacerlo funcionar

En un proyecto tradicional de Django, lo que hacemos justo después de terminar la instalación (ahora se realizará esa parte dentro del contenedor), es ejecutar el comando de startproject, **recuerda hacerlo dentro de la carpeta raíz** de nuestro proyecto y lo haremos de la siguiente manera:

```bash
docker-compose run web django-admin.py startproject example .
```

Recuerda no olvidar el *punto al final*, de lo contrario, te va a crear el comando una carpeta llamada 'example' dentro de nuetra carpeta 'example', a lo que vas a necesitar cambiar estas carpetas para que todo funcione correctamente.

Tras ejecutar este comando, se realizará la instalación de todo lo necesario dentro del contenedor, dependencias y demás software. *Prácticamente estamos listos!*. **No te desesperes, pues tardará un rato en terminar** Tenemos que hacer una ligera corrección, dado que Docker aún sigue funcionando en algunas partes con privilegios de administrador, ahora debemos corregirlo para utilizarlo sin problemas.

```bash
chown -R $USER:$USER .
```
La leyenda de '$USER' es necesario que la cambies por el nombre de tu usuario; y también ejecutar estos comandos con privilegios de administrador, como *root* o con *sudo*.

**Nota**. Un punto con el que puedes recordar como realizar ciertas operaciones como *migrate*, *collectstatic* o *shell*, bastante comunes cuando se trabaja con Django, se puede realizar de la siguiente manera:

```bash
docker-compose run web python3 manage.py <comando>
```
Necesitamos configurar nuestro archivo *settings.py* con la base de datos, para poderlo hacer funcionar por completo Django. Por lo que basta agregar estas líneas en el archivo correspondiente.

```python
#..
#...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
#...
#..
```
**Y listo!**, cualquier otro comando que queramos utilizar lo usamos como antes lo mencioné. Y solo basta utilizar los comandos base de *docker-compose* para detener, arrancar o destruir nuestro contenedor con Django, **happy coding...**.


#### Fuentes:

1. [Docker en linux.com](https://www.linux.com/news/docker-shipping-container-linux-code "Docker: A 'Shipping Container' for Linux Code")
2. [Docker Wiki](https://es.wikipedia.org/wiki/Docker_(software) "Docker Wiki")
3. [Tutorial de Docker con Django](https://docs.docker.com/compose/django/ "Docker Tutorial")
