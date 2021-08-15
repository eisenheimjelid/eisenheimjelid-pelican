Title: Respaldo de Postgresql
Date: 2020-04-26 16:20
Category: Postgresql
Tags: commandos,respaldo,base de datos,db,postgresql,docker
Slug: respaldo-de-postgresql
Authors: David León
Summary: Crear un respaldo automatizado en bash, simplemente exportar tu base de datos a otra nueva instancia de Postgresql, o simplemente restaurar un viejo respaldo en un contenedor de Docker, con Postgresql para hacer pruebas. Estos son los comandos básicos que utilizo para transaccionar bases de datos entre instancias.


La base de datos PostgreSQL es uno de los manejadores, de código abierto, más utilizados en el mundo de las tecnologías de la información; en buena parte por su robustes, facilidad de uso, mantenimiento, escalabilidad y rendimiento. Además, de que en lo personal, maneja una de las mejores características de las bases de datos, que por ejemplo, no cuenta MySQL o MariaDB, su competencia directa por ser manejadores gratuitos.

Y a pesar de ello, ribaliza en rendimiento y robustes con algunos de los manejadores más caros del mercado, como bien podría ser Oracle o MSSQLserver. Con los cuales, si comparte una de sus mejores características (a mi parecer), el manejo de equemas (schemes); estructura de la base de datos a nivel tabla-columna y programación de disparadores (triggers). Misma que permite manejar una cantidad exagerada de datos, al manetener una misma estructura, y datos aislados, para varias instancias de un mismo sistema (multi-tenant), pero eso será tema de otro artículo.

![postgresql](/theme/assets/img/postgresql.jpg)


### Crear un respaldo de la base de datos

Para poder exportar la estructura de tablas, columnas, permisos, roles y datos de una base en Postgresql (v9+), tenemos que ocupar el comando `pg_dump`, con ciertos parámetros, y guardar el resultado en un archivo de texto plano con extensión .sql.

```bash
~# dg_dump -U mi-usuario -d mi-bd -p 5433 > mi-export.sql
```

Con el parámetro **-U** especificamos el nombre del usuario con el cual nos estamos conectando a la base de datos; con el parámetro **-d** indicamos el nombre de la base de datos a exportar; con el parámetro **-p** especificamos el puerto, en caso de que sea uno distinto al default **5432**; y por último, el nombre del archivo en el que se va a guardar el contenido exportado.


### Crear un respaldo completo de toda la base de datos

En ocasiones, necesitamos exportar más de una base de datos que exista en el manejador, y el método anterior, tendría que repetirse tantas veces, como bases de datos queramos exportar. Así que para poder exportar, por completo, todas las estructuraa de tablas, columnas, permisos, roles y datos de cada base en Postgresql (v9+), tenemos que ocupar el comando `pg_dump_all`, con ciertos parámetros, y guardar el resultado en un archivo de texto plano con extensión .sql.

```bash
~# dg_dump -U mi-usuario -p 5433 > mi-export-all.sql
```

Con el parámetro **-U** especificamos el nombre del usuario con el cual nos estamos conectando a la base de datos; con el parámetro **-p** especificamos el puerto, en caso de que sea uno distinto al default **5432**; y por último, el nombre del archivo en el que se va a guardar el contenido exportado.


### Restaurar un respaldo de la base de datos

Para poder restaurar la estructura de tablas, columnas, permisos, roles y datos de una base en Postgresql (v9+), tenemos que ocupar el comando `psql`, con ciertos parámetros, consultando el contenido de la base de datos a resutarar, desde un archivo de texto plano con extensión .sql.

```bash
~# cat mi-export.sql | psql -U mi-usuario -p 5433
```

Con el parámetro **-U** especificamos el nombre del usuario con el cual nos estamos conectando a la base de datos; con el parámetro **-p** especificamos el puerto, en caso de que sea uno distinto al default **5432**; y por último, el nombre del archivo que cuenta con el respaldo de la base de datos, para ser importado al manejador.


### Restaurar una base de datos con otro nombre

En ocasiones, tenemos un ambiente de pruebas y uno de producción, con dos manejadores de Psotgresql distintos; y necesitamos exportar la base de pruebas ya lista, que tiene el nombre `lista-para-prod`, y mandarla al manejador en producción con el nombre `mi-sistema` (o cualquier nombre distinto). Entonces se vuelve algo complicado, dado que el archivo exportado en un inicio, amarra la estructura, roles, permisos y demás con el nombre original de la base de datos, así que si decidimos importar el archivo .sql en el nuevo manejador con el mismo archivo, no va surtir efecto en la base que deseamos, si no que va a crear una nueva, con el mismo nombre que la anterior.

Pero eso no es lo que queremos hacer, deseamos tener la base de datos `lista-para-prod` en `mi-sistema`, con los nombres de `mi-sistema` y no los originales. Entonces, utilizamos el método más rápido, creamos una base de datos con el nuevo nombre, el manejador original y lo exportamos, así el archivo resultante tendrá el nuevo nombre, y en el nuevo manejar, simplemente lo restauramos como si nada pasara.

```bash
~# createdb -U mi-usuario -T lista-para-prod mi-sistema
~# pg_dump -U mi-usuario -d mi-sistema -p 5433 > mi-sistema.sql
.
.
.
~# cat mi-sistema.sql | psql -U mi-servidor -d mi-sistema -p 5433
```

El primer comando, hace la diferencia, porque creamos una base de datos con un nuevo nombre, tomando de base la ya existente; con el parámetro **-T** indicamos que deseamos crear una base de datos usando de plantilla (template) otra base, que en este caso, es la original. Una ves hecho eso, ya usamos lo que conocemos, y exportamos la nueva base, con el nuevo nombre, movemos el archivo y lo cargamos en el otro manejador, para poder restaurarla con el otro comando.


### Respaldar/Restaurar una base de datos en Docker

Algo que también he estado haciendo mucho, es perder datos en Docker, ¿no les ha ocurrido que actualizan el paquete `docker-ce` en su sistema operativo y se pierden los contenedores? Pues que suerte si no; pero a mi, me ha ocurrido al menos un par de ocasiones, en donde, después de actualizar `docker-ce` desde `apt-get upgrade -y` ´la instalación de docker, reinicia la carpeta `/var/lib/docker` que es la ruta por defecto, para guardar los contenedores; así que al levantar el servicio actualizado de docker, **¡adios!** ya no existen los viejos contenedores. Y no es que los borre, creo que limpia algunos registros y pierde la referencia de los contenedores, así que al querer iniciar de nuevo tu viejo contenedor, aparecerá algun error de una referencia borrada, no encontrada o algo parecido.

Así que podemos optar por dos esquemas: el primero, hacemos persistentes en el sistema de archivos la carpeta de datos de postgresql, o segundo, implementamos un esquema de respaldos, para poder exportar la base de datos en un archivo .sql, garantizando siempre tener un respaldo en otra ubicación, y nunca dentro del contenedor ... que tarde que temprano, puede ser eliminado.

Este segundo esquema, es el que a mi parecer, es mejor, bajo el supuesto de que tus contenedores guarden información importante y se encuentren bajo un uso productivo, es decir, que si lo pierdes, te metes en buenos líos!. Así que lo que tendríamos que hacer, es generar el respaldo de Postgresql, desde fuera del contenedor, hacía el sistema de archivos, y bajo cualquier otro esquema de respaldo, mover ese archivo a otra ubicación segura; de la siguiente manera.

```bash
~# docker exec -t your-db-container pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
.
.
.
~ # cat your_dump.sql | docker exec -i your-db-container psql -U postgres
```

Por el momento, hasta aquí queda este pequeño recordatorio de como exportar/importar bases de datos, desde el manejador de PostgreSQL. ¡Gracias! y nos vemos la próxima.

### Fuentes

Puedo mencionar la documentación y manuales, en el sitio oficial de Postgresql, pero creo que es la referencia básica en cualquier punto relacionado a este manejador de base de datos; pero realmente, es experiencia propia, y varios años administrando bases de datos. 
