Title: Services on AlmaLinux Using `systemctl`
Date: 2025-05-04 19:00
Category: Linux
Tags: linux,terminal,comandos
Slug: install-services-on-alma-linx-using-systemctl
Lang: en
Translation: true
Authors: David León
Summary: To manually install services in AlmaLinux using systemctl, the general process involves establishing the program we'll be running in the background, setting the execution conditions, preparing the service file and its environment, and finally, executing the systemctl commands in a defined order to start, enable, and restart the service.

# Installing Services on AlmaLinux Using `systemctl`

## Introduction

Monitoring servers and applications is a fundamental task in system administration. Tools like Prometheus and Grafana have become industry standards for observability, and exporters are used to collect metrics from various sources. These exporters are services that run on the server and expose metrics in a format that Prometheus can understand and collect.

On AlmaLinux, an RHEL-based distribution, the main initialization and service management system is `systemd`, controlled via the `systemctl` command. This post details the general steps for installing a service on AlmaLinux using `systemctl`, taking the installation of exporters like `php-fpm_exporter` (for PHP-FPM metrics) and `mysqld_exporter` (for MySQL metrics) as examples.

## Steps for Service Installation with `systemctl`

Installing a custom service, such as an exporter, typically involves obtaining the executable binary and configuring `systemd` to manage it. The following steps are based on the processes described for `php-fpm_exporter` and `mysqld_exporter`:

1.**Download the service binary file.** This is typically done using a tool like `wget` or `curl` to get the executable file directly from a reliable source. For `php-fpm_exporter`, a specific binary for Linux AMD64 was downloaded. For `mysqld_exporter`, a `.tar.gz` file containing the binary was downloaded.

```bash

wget https://github.com/hipages/php-fpm_exporter/releases/download/v2.2.0/php-fpm_exporter_2.2.0_linux_amd64

wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.17.2/mysqld_exporter-0.17.2.linux-amd64.tar.gz
```

2.If the downloaded file is a compressed archive (like `.tar.gz`), **decompress it.** The `tar -zxvf` command is used for `.tar.gz` files.

```bash
tar -zxvf mysqld_exporter-0.17.2.linux-amd64.tar.gz
```

3.**Place the service binary file** in an appropriate system path, such as `/usr/bin`. This path is common for system executables. The `cp` or `mv` command is used to move the decompressed or downloaded file to the desired path.

```bash

mv php-fpm_exporter_2.2.0_linux_amd64 /usr/bin/php-fpm_exporter

cp mysqld_exporter-0.17.2.linux-amd64/mysqld_exporter /usr/bin/mysqld_exporter
```

4.**Assign the correct user and group** to the binary file. For security and permissions reasons, it is recommended that the service does not run as `root`. In the examples, `chown` was used with specific user and group IDs (`1001:1002`, or `node_exporter` in the service file).

```bash
chown 1001:1002 /usr/bin/php-fpm_exporter
chown 1001:1002 /usr/bin/mysqld_exporter
```

5.**Verify and assign execute permissions** to the binary file. It is crucial that the file has permissions to be executed. The `chmod +x` command is used.

```bash
chmod +x /usr/bin/php-fpm_exporter
chmod +x /usr/bin/mysqld_exporter
```

6.**Create or modify the unit file** (`.service`) for `systemd`. This file defines how `systemd` should manage the service and is saved in the `/etc/systemd/system/` path. It describes the **description** (`Description`), **dependencies** (`After=network.target`), the **user and group** it runs as (`User=`, `Group=`), the **startup type** (`Type=simple`), and most importantly, the **path to the executable binary** (`ExecStart=`). In the examples, an existing service file (`node_exporter.service`) was duplicated and modified.

```bash

cd /etc/systemd/system/

nano php-fpm_exporter.service
```

    Typical content of the `.service` file:

```ini
[Unit]
Description=PHP-FPM Exporter # Or MySQL Daemon Exporter
After=network.target

[Service]
User=node_exporter # Make sure this user exists
Group=node_exporter # Make sure this group exists
Type=simple
ExecStart=/usr/bin/php-fpm_exporter # Or /usr/bin/mysqld_exporter
Restart=on-failure # (Optional but recommended) Restart if it fails

[Install]
WantedBy=multi-user.target
```

7.**Reload the systemd daemon**. This is necessary for `systemd` to read and recognize the new service unit file that has just been created or modified.

```bash
systemctl daemon-reload
```

8.**Start the service** for the first time. The `systemctl start <service_name>` command is used, where `<service_name>` is the name of the `.service` file without the extension (e.g., `php-fpm_exporter` or `mysqld_exporter`).

```bash
systemctl start php-fpm_exporter

systemctl start mysqld_exporter
```

9.**Enable the service** so that it starts automatically every time the system boots.

```bash
systemctl enable php-fpm_exporter

systemctl enable mysqld_exporter
```

10.**Restart the service** if changes were made to the unit file (`.service`) or the service's configuration (although for configuration changes, a `reload` might suffice if the service supports it, `restart` is safer to apply any changes).

```bash
systemctl restart php-fpm_exporter

systemctl restart mysqld_exporter
```

11.**Check the service status** to confirm that it is running correctly. The `systemctl status <service_name>` command is used.

```bash
systemctl status php-fpm_exporter

systemctl status mysqld_exporter
```

    The **important output** to check is that it shows `Active: active (running)`. This confirms that `systemd` has started and is keeping the service running.

## Conclusion

By following these steps, we have successfully installed and configured a service (in this case, an exporter) on AlmaLinux to be managed by `systemd` and `systemctl`. This process is fundamental for ensuring that background applications and tools run reliably and automatically upon system startup. Once the service is `active (running)`, it is ready to perform its function, such as exposing metrics for Prometheus to collect. Centralized management via `systemctl` simplifies the tasks of starting, stopping, restarting, and monitoring the status of services on the server.
