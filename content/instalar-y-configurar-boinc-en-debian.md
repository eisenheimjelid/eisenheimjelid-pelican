Title: Instalar y configurar BOINC en Debian
Date: 2017-03-27 20:20
Category: BOINC
Tags: linux,debian,distribuido
Slug: instalar-y-configurar-boinc-en-debian
Authors: David León
Summary: La **Infraestructura Abierta de Berkeley para la Computación en Red** (por sus siglas en inglés: **BOINC**), es un software de código abierto que permite compartir los recursos locales de un equipo de computo, persiguiendo un objetivo científico o de similares intenciones, donando '_procesamiento_' para cumplir tal objetivo; detallo en este artículo su instalación y configuración para un equipo Debian. 




Empezando desde el inicio, aclaro que he utilizado **GNU/Linux Debian 8 (Jessie)**, para realizar el ejemplo del artículo. Aunque también vale aclarar lo que es **BOINC**, antes que nada: la _Infraestructura Abierta de Berkeley para la Computación en Red_ es un software de código abierto, que utiliza las bondades del Internet y el computo distribuido para crear algo así como una suerte de super-computadora para realizar el análisis o **cálculos necesarios para cumplir con cierto objetivo**, distribuida entre muchos ordenadores al rededor del mundo, por ejemplo, el nuestro.

![terminal](/theme/assets/img/boinc.jpg)

**BOINC** fue un proyecto que nació de la mano de [SETI](https://es.wikipedia.org/wiki/SETI), el programa de **búsqueda de inteligencia extraterrestre**, al rededor del año 2002. Este software permitiría al proyecto contar con un procesamiento mayor al de muchas super-computadoras que funcionan hoy en día, **con un costo mucho menor**. Pero después de su publicación, y al dar cuenta de su enorme poder, muchos otros proyectos se sumaron, y ahora también se puede contribuir a cosas tan variadas como: economía (bitcoin), biología (rosetta), matemáticas (búsqueda de números primos), etc.

Con cualquiera de estos proyectos nos podemos sentir identificados, y a su vez, **donar el uso o capacidad de procesamiento de nuestros modestos equipos** locales (o tal vez ni tan modestos), aportando un granito de arena al desarrollo científico. 

_¿Recibimos algo a cambio?_ Además de la satisfacción de ser parte algo mucho mayor, en una contribución directa; cada proyecto nos brinda un **certificado digital**, firmado por los directores o responsables de cada proyecto, que respalda cada una de las universidades que hacen uso de esta pieza de software, y nos dan el agradecimiento por las horas/procesamiento invertidas en sus proyectos

Fuera de esto (reconocimiento), **desconozco si existe algún otro beneficio directo**; pero como informático, participar en este tipo de actividades, sin duda brinda un bosquejo general de **como funcionan los sistemas distribuidos**, y el alcance que se puede conseguir, si uno mismo intenta crear un nuevo proyecto, es completamente libre.


### Instalar BOINC

Si usan un entorno gráfico, será mucho más sencillo, pero en mi caso he usado un servidor que utilizo para pruebas, así que **no tiene un entorno de ventanas**. Al instalar **BOINC** con el administrador es mucho más sencillo agregar los proyectos y determinar la cantidad de recursos que destinaremos a cada uno, pero les mostraré una forma quizás más complicada, pero que funciona para sistemas sin entorno de ventanas.

Es necesario poder utilizar un usuario con privelegios administrativos (**root**), y para instalar BOINC con en entorno gráfico, ejecutamos:

```bash
# apt-get install boinc-client boinc-manager
```

Pero en nuestro caso, sin entorno gráfico, solo instalamos el cliente:

```bash
# apt-get install boinc-client
```

Este comando instalará BOINC, pero entiendo un poco más al respecto, realizará los siguientes pasos:

1. Crea el script del demonio en **/etc/default/boinc-client**.
2. Coloca los binarios BOINC (boinc_client, boinc_cmd y boincmgr) en /etc/boinc-client/.
3. Crea /var/lib/boinc-client/ para los archivos de datos de BOINC y los directorios de los proyectos.
4. Nombra el demonio **boinc-client**.
5. Crea un usuario llamado boinc. Por razones de seguridad, boinc debe estar asignado al directorio de datos de BOINC (/var/lib/boinc-client/) y todos los archivos de datos y subdirectorios que crea en el directorio de datos.

Ahora, solo basta con reiniciar el sistema, para verificar que en efecto arranca BOINC (paso 4) sin problemas; esto nos va a permitir que aunque el sistema pierda energía electríca, o lo reiniciemos por algún motivo, vuelvea a arrancar el demonio de BOINC al arrancar nuevamente el sistema operativo.

Para detener o volver a arrancar el demonio de BOINC, basta con usar el script del paso 1:

```bash
# /etc/init.d/boinc-client start
```

Para comprobar que el demonio esta vivo en el sistema, podemos ejecutar el siguiente comando:

```bash
# ps -el | grep boinc
```

El resultado mostrará algo como _boinc_client_, de lo contrario, habrá que revisar los logs de la pieza de software, ubicados en /var/log/boinc. En las referencias al final del artículo, podremos buscar alguna solución.


### Agregar un proyecto

Una vez instalado **BOINC**, ahora necesitamos anotarnos a un proyecto al que deseemos contribuir, y puede buscar el que más sea de su agrado en: [Projects Berkeley](http://boinc.berkeley.edu/projects.php "Proyectos de Berkeley"). Habrá que seguir el proceso de cada uno de los proyectos para crear una cuenta, pues requerimos el nombre de usuario y contraseña, para empezar a contribuir.

Ya que contamos con nuestro usuario y contraseña, ejecutamos el comando de **_boinccmd_** con el parámetro de _lookup_account_, para obtener la llave correspondiente, para no utilizar la contraseña siempre, en su lugar, solo una clave de acceso. Después solo bastará utilizar el parámetro _project_attach_ para poder iniciar el proceso y así contribuir al proyecto.

Un ejemplo de lo anterior es:

```bash
$ boinccmd --lookup_account setiathome.berkeley.edu miusuario micontrasena
    status: Success
    poll status: operation in progress
    poll status: operation in progress
    poll status: operation in progress
    account key: 73c06fcd129df53a76e620d128943a019b072
$ boinccmd --project_attach setiathome.berkeley.edu 73c06fcd129df53a76e620d128943a019b072
```

Este ejemplo es con el proyecto de SETI, pero depende de cada uno, nos dará una URL distinta, usualmente con el nombre del poryecto en minusculas, seguido de _berkeley.edu_, así que es un dato que debemos revisar en nuestra cuenta del proyecto, para definiar correctamente la ruta.

Al momento de elegir el proyecto al que deseamos contribuir, también es necesario revisar la plataforma en la que esta disponible el proyecto, dado que no todos son para Linux o Windows, y algunos tienen el software necesario para explotar el uso de GPU's, si es que el equipo cuenta con ellos.


### Configurar y parámetrizar los proyectos

BOINC por defecto va a **acaparar todos los recursos disponibles** del sistema para realizar las operaciones designadas del proyecto. Así que si deseamos seguir ocupando el equipo para nosotros, o que simplemente ocupe los recursos del sistema en ciertos horarios BOINC, necesitaremos realizar cierta configuración, para limitar su uso.

Para el ambiente gráfico, si es que decidimos utilizar el ambiente gráfico, vale la pena consultar las instrucciones detallas en la [Wiki de Berkeley](https://boinc.berkeley.edu/wiki/Editing_computing_preferences_with_the_BOINC_Manager "Wiki de Berkeley"). Pero hablando de lo que nos interesa, sin utilizar el ambiente de ventanas, debemos tocar los siguientes parámetros:

* **max_ncpus_pct** Este valor nos permite definir la cantidad de núcleos a utilizar, expresado como un porcentaje. Por ejemplo, si contamos con 8 núcleos de procesamiento, y definimos el valor al 75% solo se usarán 6 núcleos, el resto estarán libres.
* **cpu_usage_limit** Este valor nos permite definir la capacidad a utlizar, expresado como un porcentaje. Por ejemplo, si definimos 70% no se utilizará más allá de ese porcentaje de procesamiento en cada procesador; mientras más alto sea este valor, más estaremos aportando al proyecto.
* **run_on_batteries** Este valor nos permite definir si el proceso de BOINC funcionará con el equipo usando la bateria, o no. El valor por defecto es 0, que quiere decir que NO detendrá BOINC en caso de que el sistema se quede sin alimentación electrica, utilizando solamente las baterias; esto aplica principalmente para equipos portátiles.
* **run_if_user_active** Este valor nos permite definir si el proceso de BOINC funcionará siempre que un usuario no este utilizando el equipo, es decir, con el valor 0 indica que NO se detendrá BOINC en caso de que el sistema este siendo usado por un usuario.
* **run_gpu_if_user_active** Similar al punto anterior, solo si esta presente un GPU en el sistema, no se utilizará en caso de que el usuario del sistema este haciendo uso de él; y solo funcionará cuando este desocupado.
* **idle_time_to_run** Este es el parámetro que utiliza BOINC para definir, si no hay una interacción del teclado o mouse por más de 3 minutos (definido por defecto, y siempre expresado en minutos), da por hecho que el sistema esta desocupado.
* **suspend_if_no_recent_input** Este parámetro nos ayuda a definir si el sistema utiliza cierto porcentaje de procesamiento, detiene en automático BOINC, para darle prioridad a otros procesos, por defecto esta desactivado con un 0 y activado con un 1.
* **suspend_cpu_usage** Este parámetro va de la mano del anterior, en caso de que este activado, tomará de referencia este porcentaje para saber si, por ejemplo, el uso del sistema esta por arriba del 25% del uso del procesamiento, entonces detendrán BOINC; podemos colocar cualquier porcentaje en este parámetro.
* **work_buf_min_days** Este parámetro nos define la cantidad mínima de información sobre los procesos del proyecto, que será guardada de manera local, usualmente se define entre 0.1 y 1.5, es decir, entre una porción de 1 día y hasta día y medio guardado, solo como referencia.
* **work_buf_additional_days** Este parámetro nos define la cantidad máxima adicional, sobre los procesos del proyecto, que será guardada de manera local.
* **cpu_scheduling_period_minutes** Este parámetro indica los periodos de tiempo en que se programan los procesos indicados de cada proyecto, es decir, si se inicia una tarea de cierto proyecto, debe durar N minutos antes de volver a aceptar el siguiente proceso.
* **disk_max_used_gb** Este parámetro nos indica la cantidad máxima en GB de espacio en el disco duro que se pude utilizar para los procesos de cada proyecto.
* **disk_min_free_gb** Este parámetro nos indica la cantidad mínima en GB disponible de spacio en el disco duro que se puede utilizar para los procesos de cada proyecto.
* **disk_max_used_pct** Este parámetros nos indica en porcentaje total del espacio del disco duro que puede ser utilizado para los procesos de los proyectos.
* **ram_max_used_busy_pct** Este parámetro nos indica el porcentaje máximo que se puede utilizar de la memoria RAM, cuando el sistema este en uso por un usuairo.
* **ram_max_used_idle_pct** Este parámetro nos indica el porcentaje máximo que se puede utilizar de la memoria RAM, cuando el sistema NO esta en uso por un usuario.
* **max_bytes_sec_down** Este parámetro nos indica el ratio de bytes por segundo de bajada, que pueden utilizar los procesos de los proyectos, de la red a la que este conectada el sistema, es importante recordar que el uso de la conexión a Internet es indispensable para el correcto funcionamiento de BOINC.
* **max_bytes_sec_up** Este parámetronos indicar el ratio de bytes por segundo de subida, que pueden utilizar los procesos de los proyectos, de la red a la que este conectada el sistema.


Estos parámetros estarán definidos en el archivo: **/var/lib/boinc-client/global_prefs.xml** en formato XML, y los valores por defecto sirven perfectamente para empezar a aportar a los proyectos; pero si requerimos realizar algún cambio, esta mencionado para que sirven la mayoría de estos parámetros.

Ahora bien, en caso de que el equipo lo estemos **destinando** integramente al proceso de BOINC, de uno o multiples proyectos, _no es necesario realizar esta configuración_, pues por defecto BOINC utilizará todos los recursos disponibles del sistema, balanceando cada proyecto que hayamos definido.

Si tienes alguna duda u observación, puedes utilizar la sección correspondiente para externar tus comentarios. Cualquier comentario será bienvenido.

#### Fuentes:

1. [Instalar BOINC](https://boinc.berkeley.edu/wiki/Installing_BOINC_on_Debian "Instalar BOINC")
2. [Acerca de BOINC](https://es.wikipedia.org/wiki/Berkeley_Open_Infrastructure_for_Network_Computing "Acerca de BOINC")
3. [Listado de proyectos de Berkeley](http://boinc.berkeley.edu/projects.php "Proyectos de Berkeley")
4. [Listado ampliado de proyectos activos](https://wiki.debian.org/BOINC/Projects "Proyectos Activos")
5. [Referencia completa de los parámetros](https://boinc.berkeley.edu/wiki/Preferences "Parámetros de BOINC")

