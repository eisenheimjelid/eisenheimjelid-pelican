Title: Agregar un disco secundario a Debian desde la Terminal
Date: 2017-03-24 20:20
Category: Debian
Tags: linux,terminal,bash
Slug: agregar-un-disco-secundario-a-debian-desde-la-terminal
Authors: David León
Summary: Después de realizar una instalación limpia de GNU/Linux Debian, en ocasiones es necesario realizar la configuración adicional de un disco duro secundario, o inclusive en ocasiones, no se configura el 100% del disco duro durante la instalación y es necesario configurar el restante espacio libre para que se utilice en alguna ruta especial. Se muestra en este artículo, los comandos y secuencias necesarias para realizarlo. 


Después de realizar la instalación limpia de GNU/Linux Debian, es necesario en ocasiones realizar la configuración extra de un disco duro secundario, o cuando no se configura al 100% el uso del disco duro principal durante la instalación, se configura el restante espacio libre para que se utilice en alguna ruta especial. A continuación describiré los comandos y secuencias necesarias para realizarlo.

![terminal](/theme/assets/img/terminal.png)

### 1. Obtener el nombre del dispositivo

```bash
# fdisk -l
```

Con este comando, se listan los dispositivos conectados al equipo y que están reconocidos con los controladores correspondientes del núcleo de Linux. En caso de que no aparezca el disco duro, tendrás que revisar si esta funcionando correctamente, o revisar si el sistema tiene los controladores correctos para su dispositivo.

Como observación, los comandos indicados en este paso y los suscesivos, se ejecutan con privilegios de administrador (_#_), de otra manera marcará un error.

El resultado del comando es similar al siguiente, debe aparecer algo como un *sdb* u otra letra después de _sb_ dependiendo de la cantidad de unidades de almacenamiento que tenga el sistema. Anota este nombre en algún otro lugar, pues es la referencia que buscamos para utilizarse como parámetro en los siguientes comandos.

```bash
Disk /dev/sda: 298.1 GiB, 320072933376 bytes, 625142448 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disklabel type: dos
Disk identifier: 0xf881ab01

Disposit.  Inicio     Start     Final  Sectores   Size Id Tipo
/dev/sda1              2048   7954431   7952384   3.8G 82 Linux swap / Solaris
/dev/sda2  *        7954432 154439679 146485248  69.9G 83 Linux
/dev/sda3         154441726 625141759 470700034 224.5G  5 Extendida
/dev/sda5         154441728 625141759 470700032 224.5G 83 Linux


Disk /dev/sdb: 14.6 GiB, 15610576896 bytes, 30489408 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xc3072e18

Disk /dev/sdb doesn't contain a valid partition table

```


### 2. Escribir el particionado del disco

Ya que el dispositivo que deseamos agregar esta identificado, ejecutamos el comando _cfdisk_ para poder crear las particiones que necesitemos. Una vez dentro de la utilidad, seleccionamos _New_ y _Primary_ para después indicar el tamaño de la partición; confirmamos la operación y le damos salir.

```bash
# cfdisk /dev/sdb
 
> New -> Primary -> Specify size in MB
> Write
> Quit

```


### 3. Formatear la partición

Con la partición definida en el paso anterior, se procede a realizar el formateo de la misma; este comando se puede utilizar de igual forma para borrar cualquier partición definida en otro disco. En el ejemplo, realizo el formateo con *EXT3*.

```bash
# mkfs.ext3 /dev/sdb1
```


### 4. Montar la unidad en una ubicación

Se tiene que definir una ubicación para poder acceder a los archivos del nuevo disco, utilizando el comando _mkdir_ seguido de un nombre, podemos ubicar el formato en cualquier ruta que descidamos. Y después montamos la unidad, indicando el formato de la partición, con la ruta de acabamos de definir, de la siguiente manera.

```bash
# mkdir /disk2
# mount -t ext3 /dev/sdb1 /disk2
```

Puedes cambiar la ruta "_/disk2_" por cualquier otra que te convenga.


### 5. Convertimos el punto de montaje en uno permanente

Con el paso anterior, todo funcionará correctamente, pero tras un reinicio del sistema deberemos volver a realizarlo; para evitar esto y que el disco secundario siempre este disponible, sin importar que el sistema se reinicie, es necesario modificar un archivo que identificará la ruta y el dispositivo, en automático, montando la unidad y dejandola lista en todo momento.

El archivo a modificar es _/etc/fstab/_ con el editor de su texto plano de su preferencia (recuerde revisar los privilegios del usuario con el cual se edita), y agregamos la siguiente línea en el archivo mencionado:

```bash
/dev/sdb1 /disk2 ext3 defaults,errors=remount-ro 0 1
```

La ruta de "_/disk2_" se debe cambiar de acuerdo a la que se haya definido en el paso anterior.

Con esto, queda terminado, y ahora la unidad estará disponible en todo momento para ser utilizada. Este es el primer artículo de una serie de varios datos que he recabado durante mi experiencia profesional, tips útiles que siempre vale la pena tener a la mano en todo momento.

Eres libre de comentar más abajo, tu ipión o cualquier otro tema relacionado. Gracias por tu tiempo para leerlo y/o compartirlo.
