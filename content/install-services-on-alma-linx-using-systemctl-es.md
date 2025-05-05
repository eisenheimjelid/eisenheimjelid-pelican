Title: Servicios en AlmaLinux Usando systemctl
Date: 2025-05-04 19:00
Category: Linux
Tags: linux,terminal,comandos
Slug: install-services-on-alma-linx-using-systemctl
Lang: es
Authors: David León
Summary: Para instalar manualmente servicios en AlmaLinux usando systemctl, el proceso general implica establecer el programa que ejecutaremos en segundo plano, establecer las condiciones de ejecución, preparar el archivo de servicio y su entorno y, finalmente, ejecutar los comandos systemctl en un orden definido para iniciar, habilitar y reiniciar el servicio.

# Instalación de Servicios en AlmaLinux Usando `systemctl`

## Introducción

El monitoreo de servidores y aplicaciones es una tarea fundamental en la administración de sistemas. Herramientas como Prometheus y Grafana se han convertido en estándares de la industria para la observabilidad, y para recolectar métricas de diversas fuentes, se utilizan exportadores (exporters). Estos exportadores son servicios que se ejecutan en el servidor y exponen métricas en un formato que Prometheus puede entender y recolectar.

En AlmaLinux, una distribución basada en RHEL, el sistema de inicialización y gestión de servicios principal es `systemd`, controlado a través del comando `systemctl`. Este post detalla los pasos generales para instalar un servicio en AlmaLinux utilizando `systemctl`, tomando como ejemplo la instalación de exportadores como `php-fpm_exporter` (para métricas de PHP-FPM) y `mysqld_exporter` (para métricas de MySQL).

## Pasos de Instalación de un Servicio con `systemctl`

La instalación de un servicio personalizado, como un exportador, generalmente implica obtener el binario ejecutable y configurarlo para que `systemd` lo administre. Los siguientes pasos están basados en los procesos descritos para `php-fpm_exporter` y `mysqld_exporter`:

1.**Descargar el archivo binario del servicio.** Esto se hace típicamente utilizando una herramienta como `wget` o `curl` para obtener el archivo ejecutable directamente desde una fuente confiable. Para `php-fpm_exporter`, se descargó un binario específico para Linux AMD64. Para `mysqld_exporter`, se descargó un archivo `.tar.gz` que contenía el binario.

```bash
wget https://github.com/hipages/php-fpm_exporter/releases/download/v2.2.0/php-fpm_exporter_2.2.0_linux_amd64

wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.17.2/mysqld_exporter-0.17.2.linux-amd64.tar.gz
```

2.Si el archivo descargado es un archivo comprimido (como `.tar.gz`), **descomprimirlo**. Se utiliza el comando `tar -zxvf` para archivos `.tar.gz`.

```bash
tar -zxvf mysqld_exporter-0.17.2.linux-amd64.tar.gz
```

3.**Ubicar el archivo binario** del servicio en una ruta apropiada del sistema, como `/usr/bin`. Esta ruta es común para ejecutables del sistema. Se utiliza el comando `cp` o `mv` para mover el archivo descomprimido o descargado a la ruta deseada.

```bash

mv php-fpm_exporter_2.2.0_linux_amd64 /usr/bin/php-fpm_exporter

cp mysqld_exporter-0.17.2.linux-amd64/mysqld_exporter /usr/bin/mysqld_exporter
```

4.**Asignar el usuario y grupo** correctos al archivo binario. Por motivos de seguridad y permisos, es recomendable que el servicio no se ejecute como `root`. En los ejemplos, se utilizó `chown` con un usuario y grupo específicos (`1001:1002`, o `node_exporter` en el archivo de servicio).

```bash
chown 1001:1002 /usr/bin/php-fpm_exporter
chown 1001:1002 /usr/bin/mysqld_exporter
```

5.**Verificar y asignar permisos de ejecución** al archivo binario. Es crucial que el archivo tenga permisos para ser ejecutado. Se utiliza el comando `chmod +x`.

```bash
chmod +x /usr/bin/php-fpm_exporter
chmod +x /usr/bin/mysqld_exporter
```

6.**Crear o modificar el archivo de unidad** (`.service`) para `systemd`. Este archivo define cómo `systemd` debe gestionar el servicio y se guarda en la ruta `/etc/systemd/system/`. Describe la **descripción** (`Description`), las **dependencias** (`After=network.target`), el **usuario y grupo** bajo el que se ejecuta (`User=`, `Group=`), el **tipo de inicio** (`Type=simple`), y lo más importante, la **ruta del archivo binario a ejecutar** (`ExecStart=`). En los ejemplos, se duplicó un archivo de servicio existente (`node_exporter.service`) y se modificó.

```bash

cd /etc/systemd/system/

nano php-fpm_exporter.service
```

    Contenido típico del archivo `.service`:

```ini
[Unit]
Description=PHP-FPM Exporter # O MySQL Daemon Exporter
After=network.target

[Service]
User=node_exporter # Asegúrate de que este usuario exista
Group=node_exporter # Asegúrate de que este grupo exista
Type=simple
ExecStart=/usr/bin/php-fpm_exporter # O /usr/bin/mysqld_exporter
Restart=on-failure # (Opcional pero recomendado) Reiniciar si falla

[Install]
WantedBy=multi-user.target
```

7.**Recargar el daemon de systemd**. Esto es necesario para que `systemd` lea y reconozca el nuevo archivo de unidad de servicio que se acaba de crear o modificar.

```bash
systemctl daemon-reload
```

8.**Iniciar el servicio** por primera vez. Se utiliza el comando `systemctl start <nombre_del_servicio>`, donde `<nombre_del_servicio>` es el nombre del archivo `.service` sin la extensión (por ejemplo, `php-fpm_exporter` o `mysqld_exporter`).

```bash
systemctl start php-fpm_exporter

systemctl start mysqld_exporter
```

9.**Habilitar el servicio** para que se inicie automáticamente cada vez que el sistema arranca.

```bash
systemctl enable php-fpm_exporter

systemctl enable mysqld_exporter
```

10.**Reiniciar el servicio** si se hicieron cambios en el archivo de unidad (`.service`) o en la configuración del servicio (aunque para cambios en la configuración del servicio, a veces basta con un `reload` si el servicio lo soporta, pero `restart` es más seguro para aplicar cualquier cambio).

```bash
systemctl restart php-fpm_exporter

systemctl restart mysqld_exporter
```

11.**Verificar el estado del servicio** para confirmar que se está ejecutando correctamente. Se usa el comando `systemctl status <nombre_del_servicio>`.

```bash
systemctl status php-fpm_exporter

systemctl status mysqld_exporter
```

    La **salida importante** a verificar es que muestre `Active: active (running)`. Esto confirma que `systemd` inició y mantiene el servicio en ejecución.

## Conclusión

Siguiendo estos pasos, hemos logrado instalar y configurar un servicio (en este caso, un exportador) en AlmaLinux para ser gestionado por `systemd` y `systemctl`. Este proceso es fundamental para asegurar que las aplicaciones y herramientas de fondo se ejecuten de manera confiable y automática al inicio del sistema. Una vez que el servicio está `active (running)`, está listo para realizar su función, como exponer métricas para que Prometheus las recolecte. La gestión centralizada a través de `systemctl` simplifica las tareas de inicio, parada, reinicio y monitoreo del estado de los servicios en el servidor.
