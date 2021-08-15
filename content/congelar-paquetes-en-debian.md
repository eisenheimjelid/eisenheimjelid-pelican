Title: Congelar paquetes en Debian
Date: 2020-05-10 19:50
Category: Debian
Tags: linux,terminal,bash,apt,dpkg
Slug: congelar-paquetes-en-debian
Authors: David León
Summary: En ocasiones es necesario congelar ciertos paquetes (programas) en sistemas basados en Debian, en ambiente productivos, suele ser común que queremos evitar la actualización de algunos paquetes, para que simplemente, siga funcionando el sistema operativo ¿cómo hacerlo?


La última ocasión que intenté actualizar un sistema operativo en producción, por aquello de los certificados de seguridad, parches de los paquetes y demás actualizaciones importantes; ¡todo murió! y es que no sé si alguien ha intentado actualizar `docker-ce` en producción, reinicia y pierde la referencias a muchos contenedores, por lo que es necesario volver a construilos ... ¡datos perdidos!

![terminal](/theme/assets/img/apt-get-purge-windows.png)

### 1. Congelar un paquete con dpkg

Para aquellos administradores o usuarios versados en el mundo `Debian Like`, **dpkg** es un programa básico, cuando por algún momento **apt-get** no esta funcionando bien, o instalando paquetes fuera de los repositorios oficiales, es necesario conocer su uso, pero para el objetivo de este artículo, vamos a ocupar este programa para bloquear/congelar un paquete, y aunque existan actualizaciones disponibles, no se va a mover ni un solo archivo.

```bash
echo "<nombre-de-paquete> hold" | dpkg --set-selections

echo "<nombre-de-paquete> install" | dpkg --set-selections

dpkg --get-selections

dpkg --get-selections | grep "<nombre-de-paquete>"
```

Importante, cada uno de estos comandos, se ejecuta con privilegios de administración, anteponiendo `sudo` en caso de trabajar con Ubuntu, o `sudo su` como primer comando. La segunda línea te permite desactivar el 'bloqueo', por si ya no necesitas tener congelado el paquete, y si requieres su instalación o actualización. El resto de los paquetes son variantes para poder consultar el nombre exacto que tienen los paquetes, y su estatus.

### 2. Congelar un paquete con apt

El en mundo de Ubuntu es muy normal, hoy en día utilizar solo `apt`, y aunque no es un dpkg es una herramienta muy potente. Ahora bien, con apt, tenemos que ejecutar los siguiente comandos.


```bash
sudo apt-mark hold <nombre-de-paquete>

sudo apt-mark unhold <nombre-de-paquete>

sudo apt-mark showhold
```

De nuevo, la segunda línea es para poner el ejemplo, de cómo desactivar el bloqueo al paquete para poder instalar sus actualizaciones. Y la última línea te permite consultar un listado, con los paquetes bloqueados en el sistema.

### 3. Congelar un paquete con aptitude

También contamos con `aptitude`, otra excelente herramienta para manejar los paquetes instalados en el sistema operativo, y la forma de hacerlo es la siguiente:

```bash
sudo aptitude hold <nombre-de-paquete>

sudo aptitude unhold <nombre-de-paquete>
```

**Y listo!**, así de fácil podemos ahorranos muchos problemas, al momento de hacer actualizaciones en sistemas operativos basados en Debian. Evitando que se actualicen programas problematicos, como puede llegar a ser `docker-ce`.


#### Fuentes:

1. [Ayuda en Askubuntu](hhttps://askubuntu.com/questions/18654/how-to-prevent-updating-of-a-specific-package "How to prevent updating of a specific package?")
