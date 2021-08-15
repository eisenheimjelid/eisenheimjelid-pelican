Title: Instalar Docker en CentOS 7
Date: 2017-12-09 22:20
Category: Docker
Tags: linux,centos,docker,
Slug: instalar-docker-en-centos-7
Authors: David León
Summary: Docker es una excelente herramienta que nos permite aislar y ejecutar en entornos controlados, casi cualquier tipo de aplicativo sobre nuestro sistema operativo; aqui realizo un resumen de como instalarlo en CentOS 7.


Iniciando con lo acostumbrado, el ambiente que he utilizado es **CentOS 7**, para realizar los ejemplos del artículo. Aunque también vale aclarar lo que es [Docker](https://www.docker.com/ "Docker"), antes que nada: **Docker** es un herramienta de código abierto que automatiza el despliegue de aplicaciones con contenedores, proporcionando una capa adicional de abstracción y automatización.

![terminal](/theme/assets/img/docker-install.png)

Aunque también existen otras definiciones más apegadas a su funcionalidad, como: **Docker** es una herramienta que puede empaquetar una aplicación y sus dependencias en un contenedor, para ser ejecutado en cualquier sistema operativo: Mac, Linux, Win. Esto ayuda a permitir la flexibilidad y portabilidad en donde la aplicación se puede ejecutar, ya sea en las instalaciones físicas, la nube pública, nube privada, etc.

**CentOS 7** es un sistema operativo basado en Linux, con un excelente rendimiento, seguridad y estabilidad. Así es una muy buena opción como plataforma para montar Docker, con un laboratorio completo.


### Empezamos con el repositorio

Primero, hay que asegurarnos que contamos con el repositorio de EPEL activado, pues nos da una gama más amplia de paquetes que podemos instalar; para hacer esto basta con ejecutar el siguiente comando con permisos administrativos:

`# yum install epel-release`

Si algún comando que utilice en las siguientes líneas da un error de "command not found", bastará con ejecutar `yum install <comando>` para poder contar con el comando correcto, y seguir con la guía.

Ahora seguimos con la instalación del repositorio oficial de **Docker** en CentOS 7:

`# wget https://download.docker.com/linux/centos/docker-ce.repo -O /etc/yum.repos.d/docker.repo`


### Instalar Docker

Ahora ya estamos listos para realizar la instalación del paquete, basta con ejecutar el siguiente comando:

`# install docker-ce –y`

Es necesario habilitar el servicio de Docker, con esto podremos reiniciar el servidor sin problemas, para que el servicio vuelva a iniciar tras el reinicio; y arrancar el servicio.

`# systemctl start docker`

`# systemctl enable docker`

¡Listo! con esto ya esta instalado Docker.


### Seguridad

Una de las ventajas de instalar Docker, por este medio, es que instala unas dependencias que aseguran que no haya ningún problema con **SELinux**. Uno de los dolores de cabeza más constantes, cuando instalas o cargas ciertos sistemas en CentOS, es que SELinux suele bloquear cualquier actividad que a uno le parece normal, pero será bloqueado.

Así es que, para no deshabilitar SELinux y comprometer el sistema operativo, Docker tiene un paquete especial para generar las políticas necesarias, para que SELinux dé libre paso a las acciones que necesita ejecutar en el sistema operativo. Pero estos paquetes, no abren nada en especial dentro del firewall, así que será necesario abrir los puertos necesarios que vamos a ocupar en nuestro aplicativo, para que tengan libre acceso.

Ejecutando el siguiente comando podemos abrir el puerto que necesitemos, bajo el protocolo TCP (cambiando el número podremos indicar cualquier puerto).

`# firewall-cmd --permanent --add-port=80/tcp`
`# firewall-cmd --permanent --add-port=443/tcp`
`# firewall-cmd --permanent --add-port=8080/tcp`

Usualmente se utilizan puertos como el 80, 443 o el 8080; podemos agregar cuantos puertos necesitemos, igual el protocolo se puede cambiar por TCP o UDP. Ahora solo reiniciemos el firewall, para que se apliquen los cambios adecuadamente.

`# firewall-cmd --reload`

Por último, para asegurarnos de que todo funciona correctamente y sin errores, reiniciamos el servicio de Docker y verificamos el estatus del mismo:

`# systemctl restart docker`

`# systemctl status docker`


#### Fuentes:

1. [How to install Docker](https://blog.vpscheap.net/how-to-install-and-use-docker-on-centos-7/ "How To Install and Use Docker on CentOS 7")
2. [How to install Docker Swarm](https://www.alibabacloud.com/blog/how-to-install-and-configure-docker-swarm-mode-on-centos-7_583495?spm=a2c41.11464609.0.0 "Docker Swarm")
