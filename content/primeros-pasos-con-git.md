Title: Primeros pasos con GIT
Date: 2018-03-04 20:20
Category: Git
Tags: linux,git,vcs,
Slug: primeros-pasos-con-git
Authors: David León
Summary: GIT es un sistema de control de versiones (VCS por sus siglas en inglés), que permite mantener en orden, brindando un seguimiento claro y de formar descentralizada a todo tipo de contenido digital; aunque se utiliza especialmente para contenido en texto, código fuente de programación, su uso puede ser llevado a muchos lugares más.




Iniciando con lo acostumbrado, el ambiente que he utilizado es **GNU/Linux Debian 9 (Stretch)**, para realizar los ejemplos del artículo. Git es el nombre que recibe una de las herramientas más apliamente utilizadas, en el mundo de la informática y desarrollo de software; y fue desarrollada originalmente para una tarea única y enorme: **Mantener y controlar el código fuente del Núcle de Linux** (su kernel). Y aunque fue desarrollada principalmente para eso, para controlar código; también puede ser utilizado para un trabajo editorial, pues todo el contenido que sea texto es fácilmente enlazado para mantener un seguimiento sobre sus cambios.

Aunque también se puede dar seguimiento a otro tipo de formatos o archivos que no sean texto, las herramientas al rededor de Git están enfocadas al texto; es decir, aunque podamos subir imagenes, música o audio, no es tan simple dar seguimiento a cambios en archivos multimedia, como lo es con los archivos de texto.

![terminal](/theme/assets/img/git.jpg)

El principal servicio en Internet, por el cual destaca el uso de **Git** es precisamente el portal **Github**, y aunque existen muchos otros, de forma gratuita como **Bitbucket** o **CloudForge** con proyectos de código abierto, existen muchos más que se pueden usar de forma privada: **Codebase**, **Planio**, **Bitbucket**, y otros proyectos que te permiten tener tu propio servicio hospedado en tu infraestructura como **GitLab**. Existen una gran variedad de opciones, dependiendo del bolsillo, funcionalidades extra, uso y cantidad de programadores (usuarios) involucrados en el proyecto que deseas hospedar o usar en Internet.

Pero todos estos servicios, existen para ser utilizados en línea, porque brindan a los usuarios caracteristicas colaborativas y facilidad de uso, además de respaldos, despliegues automatizados entre otras caracteristicas. Así que propiamente, Git es una herramienta que usa siempre de manera local y fuera de línea, por lo que no es necesario contratar ninguno de esos servicios, al menos no, hasta que veamos los beneficios adicionales que nos brindan, después de empezar a usar Git de manera diaria.

### Empezamos con la instalación

Lo más sencillo, al principio, es la instalación, si haces uso de Linux como yo, ejecutar un comando nos permitirá tener instalada la versión más reciente, obviamente teniendo un repositorio en línea (o fuera de línea) disponible con todas las dependencias del paquete cumplidas, bastará con escribir:

```bash
~# apt-get install git
```

Si utilizas una versión basada en RedHat como Fedora, o CentOs, bastará con el siguiente comando:
```bash
~# yum install git-core
```

Para sistemas tipo MacOS, recomiendo utilizar Homwbrew, pues particularmente con ese sistema operativo, si bien trae una versión ya instalada y funcional, en la mayoría de los casos me ha tocado ver que es una versión vieja o modificada por el fabricante, que a mi parecer tiene unas opciones de menos o distintas a las instalaciones normales. Entonces, si lo 

### Ahora iniciamos el repositorio

Git es un sistema de control de versiones descentralizado, suenan a muchas palabras complicadas juntas, pero realmente es lo que es, y nada complicado. Es una herramienta que nos va a permitir saber y conocer con exactitud en que momento realizamos un cambio a nuestro código, quién lo hizo y muy importante, ya después, facilitar la colaboración y compartir nuestro código con muchos más participantes.

Te recomiendo que leas a detalle el manual oficial, enlace que dejo al final del artículo. Pero para empezar, todo el concepto de control de versiones se basa en **revisión**, es decir, un cambio o un punto en la historia que va a guardar una versión "_congelada_" de nuestro código o proyecto. Entonces, el **repositorio** es el espacio que ocupa dentro de nuestra computadora todo ese historico y control de cada revisión que vamos haciendo, la facilidad de esto, es que se reduce a una simple carpeta.

Cuando inicias tu repositorio, en una carpeta con tu proyecto, Git agregará una carpeta adicional llamada **.git**, en la cual va a guardar todo ese control, como si fuese una base de datos, que además revisa para garantizar que la integridad de cada cambio esta completo en el repositorio

Entonces, ahora nos ubicamos (desde la terminal), en la carpeta de nuestro proyecto o código, donde vas a mantener el repositorio.

```bash
~$ git config user.email "my-email@gmail.com"
~$ git config user.name "My Name"
```

Solo escriban su correo y su nombre, sustituyendo el contenido entre las comillas dobles, para que configuremos nuestro repositorio. Ahora bien, ¿recuerdas que te había dicho que todo se basa en la **revision**? pues bueno, esta revisión se debe firmar de alguna forma, y Git utiliza nuestro nombre y correo para hacerlo. Si cuando colabores con cualquier otro programador, y utiliza el mismo nombre y correo para firmar sus revisiones, no podrá hacer una distinción entre ambos autores la herramienta de Git.

Es por eso que es importante realizar siempre la configuración de nuestro nombre y correo, para que exista una relación integra del autor a lo largo del repositorio.

### Mi primer revisión (commit)

Es muy común, pues en este mundo de la programación, casi todo es en inglés, Git nombra a las **revisiones** de las que te he venido escribiendo, como **commit**. Solo para que sea más claro, y no existan confuciones, _revisión_ = **commit**, son lo mismo.

Bien, si iniciaste el repositorio en el punto anterior, dentro de una carpeta vacia (usualmente así inician todos los proyectos), no vas a tener ninguna revisión pendiente, hasta que hagas un cambio. Si ya tenías tu proyecto empezado desde antes, con archivos y contenido, ahora vamos a ver como agregar estos cambios y guardar nuestra primera revisión.

Si no tiene contenido, basta con crear un archivo y meter un texto de ejemplo dentro del archivo.

Para empezar, debemos agregar los cambios que queremos grabar en la revisón (en nuestro primer commit). Para esto, debemos ejecutar cualquiera de los dos primeros comandos que se muestran enseguida:

```bash
~$ git add --all
~$ git add .
~$ git commit -am "Init commit"
```

Ambos comandos van a agregar todos los archivos nuevos, que no se han agregado en ningún momento al repositorio. El tercer comando, lo que va a hacer, es crear nuestra revisión, o guardar propiamente nuestro commit. La opción '_-a_' recalca que queremos incluir todos los cambios pendientes, y la opción '_m_' indica que debe guardarse el commit con un mensaje, el que mismo que podemos personalizar cambiando el contenido de lo que muestro entre las comillas dobles.

Cabe recalcar, que los cambios que se van a grabar en la revisión, son solo aquellos que nosotros indiquemos, con el primer comando, también podemos definir con exactitud, los cambios que deseamos agregar a la revisión; por ejemplo, si agregamos dos archivos nuevos a la carpeta, uno llamado '_config.txt_' y otro llamado '_config-prueba.txt_', y el segundo no lo queremos guardar, pues solo lo estamos usando momentaneamente, o simplemente no va a ser parte de nuestro repositorio por que es irrelebante, entonces los comandos son los siguientes:

```bash
~$ git add config.txt
~$ git commit -m "Agregar el archivo config.txt"
```

Si observas el primer comando, no agrega todo, ni el punto (.) del ejemplo anterior, sin embargo si estoy agregando un nombre de archivo, que es propiamente **la ruta** del archivo o carpeta que vamos a agregar como nuevo o como cambio al repositorio. Y también, en el segundo comando la opción '_a_' desaparece, indicando que solo los cambios agregados por la opción '_add_' son los que se van a guardar en la revisión.

El mensaje es opcional, pero una de las mejores prácticas es indicar con presición, lo que estamos haciendo; de esta forma estamos ayudando al 'yo' del futuro, cuando desee revisar que fue lo que se hizo en alguna revisión pasada, en lugar de ir revisando commit por commit.

Por el momento es todo, para evitar que sea una entrega muy larga, continuaré en subsecuentes publicaciones, relatando las opciones, parámetros y diversos comandos con los que disponemos en Git.

Si deseas ubicar más rápido estas publicaciones sobre Git, puedes entrar a la [categoria del archivo, en la sección de Git](/categories.html "Categoria de Git").


#### Fuentes:

1. [Imagen de Git](https://davidescudero.com/1-git-muchos-proyectos-prestashop/ "Imagen tomada originalmente de David Escudero")
2. [Manual de Git Oficial](https://git-scm.com/book/es/v1/Empezando "Manual oficial en el sitio de Git")
