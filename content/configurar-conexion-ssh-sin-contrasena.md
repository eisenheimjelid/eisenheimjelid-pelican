Title: Configurar conexión SSH sin contraseña
Date: 2017-04-17 22:20
Category: SSH
Tags: linux,keys,conexion
Slug: configurar-conexion-ssh-sin-contrasena
Authors: David León
Summary: La conexión por medio de SSH hacía un equipo o servidor remoto, es uno de los métodos de conexión más utilizados hoy en día, principalmente por su seguridad y sencillez de uso, pero cuando se trata de automatizar tareas a través de diferentes equipos LinuxLike es mejor prescindir de las contraseñas en favor de llaves encriptadas. 




Empezando con lo usual, el ambiente que he utilizado es **GNU/Linux Debian 8 (Jessie) y Ubuntu 16.04 LTS**, para realizar los ejemplos del artículo. Aunque también vale aclarar lo que es **SSH**, antes que nada: el _Secure SHell_ es un protocolo y un programa que sigue ciertos estandáres, y su versión de código abierto es propiamente **OpenSSH**, que utiliza la red para poder interconectar dos equipos y enviar ciertas instrucciones para que sean ejecutadas en otro equipo, enviar archivos a través de un canal cifrado y seguro.

![terminal](/theme/assets/img/ssh.jpg)

**SSH** es un protocolo versátil, que podemos utilizar para: enviar comandos a otro equipo, enviar/recibir archivos y utilizar como un canal encriptado para conexiones de red. Existen 2 versiones del protocolo, la primera versión ya es actualmente vulnerable, lo contrario ocurre con la versión 2 que es la que debemos utilizar.

El principal requerimiento es que ambos equipos estén al alcance a través de Internet, o una red privada, es decir, la IP o dominio del equipo al que nos vamos a conectar, debe ser accesible por medio de la red, desde el equipo cliente.


### Probamos la conexión de SSH

Primero, nos aseguramos de podernos conectar de forma normal al equipo remoto o servidor, desde la consola tecleando:

```bash
~$ ssh [usuario]@[ip_o_dominio]
```

Nos va pedir la contraseña para concedernos el acceso, y solo tenemos 3 oportunidades, de lo contrario se cerrará el programa, hasta el próximo intento. La IP o dominio, debe ser la información del equipo remoto o servidor. Si conseguimos conectarnos con éxito, proseguimos con el siguiente paso; de lo contrario, tendremos que revisar la configuración de nuestro firewall, e inclusive en el equipo remoto, revisar los permisos de conexión.


### Generar una llave local

Si es la primera vez que intentamos conectarnos a un equipo, por medio de SSH sin utilizar una contraseña, debemos generar un par de llaves, una privada y otra pública, que nos permitirá realizar la conexión. Si ya contamos con ellas, solo pasamos al siguiente punto; pero si no es así, ejecutaremos el siguiente comando:

```bash
~$ cd ~/.ssh
~$ ssh-keygen -t rsa -b 4096 -C "mi_correo@ejemplo.com"

~$ eval "$(ssh-agent -s)"
~$ ssh-add ~/.ssh/id_rsa
```

La ubicación por defecto de las llaves generadas es _~/.ssh_, es decir, dentro de la carpeta del usuario, el subdirectorio **.ssh**, aunque al momento de ejecutar **ssh-keygen** nos pedirá la ubicación, si deseamos cambiarla en ese paso es el adecuado. Nos pedirá igualmente un **passprhase**, o propiamente una contraseña.

En este paso, es importante aclarar, que **si deseamos automatizar tareas entre ambos equipos, es necesario dejar en blanco este paso**; es decir, no introducir una contraseña. Por seguridad lo solicita, dado que esta llave evitará que el equipo remoto solicite la contraseña del usuario con el que nos conectamos, y en favor utilizará esta llave encriptada; es necesario que también este asegurada esta llave, detrás de una contraseña.

En resumen, si seguiremos haciendo a mano las conexiones, vale la pena seguir usando una contraseña distinta a la del usuario del equipo remoto, para la llave que generamos, pero si vamos a automatizar algunas tareas, es mejor dejarlo en blanco.

Los últimos dos comandos, refrescan la cache del sistema y agregamos la llave **id_rsa** a la configuración de nuestro usuario. En caso de que le hayamos colocado otro nombre a la llave, debemos cambiar el nombre del archivo por que hayamos seleccionado.


### Conectar SSH sin contraseña

Por último, el paso que nos faltaba para terminar la conexión de SSH a un servidor, sin necesidad de utilizar una contraseña. Una vez que contamos con nuestras llaves ya configuradas, lo que vamos a hacer es pasar la llave pública al servidor o equipo remoto al que nos queremos conectar; el contenido del archivo **id_rsa.pub** quedará en el servidor con el siguiente comando:

```bash
~$ ssh-copy-id -i ~/.ssh/id_rsa.pub [usuario]@[ip_o_dominio]
```

En caso de que no contemos con el comando **ssh-copy-id**, debemos conectarnos al servidor o equipo remoto, y en la ubicación siguiente, agregar el contenido del archivo **id_rsa.pub** (o la correspondiente llave publica) en: **~/.ssh/authorized_keys**.

Esto último, dado que el comando **ssh-copy-id** no siempre esta presente con la instalación de OpenSSH. Y con esto, ya solo falta probar, realizando el primer paso de este artículo, y ahora ya no nos pedirá contraseña para conectarnos.


#### Fuentes:

1. [SSH Wiki](https://es.wikipedia.org/wiki/Secure_Shell "SSH Wiki")
2. [OpenSSH](https://www.openssh.com/ "OpenSSH")

