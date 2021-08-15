Title: Clientes HTTP/S: curl o guzzle
Date: 2019-06-25 13:00
Category: Php
Tags: curl,php,guzzle,
Slug: clientes-http-s-curl-guzzle
Authors: David León
Summary: Los clientes de HTTP/S son escenciales hoy en día, bajo las nuevas arquitecturas de Microservicios, son estos los agentes que consumen los servicios API RESTful y que sirven como insumo para los procesos internos de los sistemas Web.


## Introducción

Hoy en día esta algo de moda la arquitectura de "_Microservicios_", que permite crear y mantener sistemas complejos, interactuando entre distintos servicios que hacen pocas "operaciones" muy bien, de manera independiente (de recursos). Pero en el desarrollo de este tipo de sistemas, se usan las llamadas de HTTP/S como la amalgama que permite la interacción entre cada uno de esos elementos. Para unos como cliente que consume los servicios **API RESTful**, y en otras formas como el insumo que requieren ciertos sistemas.

![microservicios](https://cdn-images-1.medium.com/max/1600/1*IiyPCOKiGOf65UmGedPrlw.png)

> **Cliente HTTP/S**: Es un "algo" parecido a un navegador Web, pero sin todo lo adicional (js, ui, html, css); solo el puro contenido (texto, mayormente).

## Curl

Es una **librería** propia de PHP, que nos permite conectarnos y comunicarnos con diferentes tipos de servidores usando diferentes tipos de protocolos como http, https, ftp, entre otros. No es necesario instalar nada adicional, pues PHP ya lo tiene inlcuido dentro de su código. Además, existen ejemplos de código para [conectar a un servicio de FTP por medio de Curl](http://nlslack.com/ftp-access-using-curl-with-php/ "Conectar a un FTP con Curl").

## Guzzle

Guzzle es un cliente HTTP/S de PHP que facilita el envío de solicitudes HTTP y la integración sencilla con los servicios web. A diferencia de curl, Guzzle solo hace peticiones a HTTP/S, y no considera peticiones bajo algún otro protocolo. Es necesario instalar este cliente por medio de [Composer](http://getcomposer.org) (es lo recomendado):

### Instalar Guzzle

```bash
# Instalar Composer
curl -sS https://getcomposer.org/installer | php
```

Después, correr el comando de composer para instalar la versión última estable de Guzzle:

```bash
php composer.phar require guzzlehttp/guzzle
```

Después, es necesario agregar el autoloader de Composer al código:

```php
require 'vendor/autoload.php';
```

## Ejemplos practicos de Curl y Guzzle

Para la charla que preparé con este tema, preparé algunos ejemplos que pueden consultar en el [repositorio de github](https://github.com/phpwaymx/curlguzzle "Repositorio con el código de ejemplo"), y que explico a grandes rasgos, aquí mismo:

### php -f curl_01.php

Este archivo va a obtener de manera simple la respuesta de example.com, presentando en la terminal el código HTML que responde ese sitio. Además, esta comentada una línea, para que se ejecute como una versión adicional, ejemplificando el error del encabezado de agente en las peticiones HTTP/S. Este agente se manda siempre con toda petición, y muchos servidores la toman como referencia para saber si descartar o no la solicitud.

Cuando utilizamos Curl, es muy sencillo omitir este punto que se considera importante por muchos servicios. Entre este, cada uno de todos los [headers de HTTP](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields "Consultar todos los encabezados del estándar") se pueden enviar/leer en cada solicitud/respuesta.

### php -f curl_02.php

Con este ejemplo, mostramos todo lo que hace el Curl _tras bambalinas_, sobre como va construyendo la petición, y todos los valores que obtiene de la respuesta de esta solicitud/respuesta.

### php -f guzzle_01.php

Similar al primer ejemplo de Curl, aquí se muestra el código mínimo necesario para poder realizar una solicitud con Guzzle, muy básica; pero que al ser un código _moderno_ se requiere una línea adicional, para considerar lo que hicimos en el punto de Composer y la instalación de Guzzle.

###php -f guzzle_02.php

Similar al segundo ejemplo de Curl, aquí se muestra el código que permite mostrar lo que hace _tras bambalinas_ la libreria, al momento de construir la solicitud y obtener la respuesta del servicio.

## Meetup de PHP México, para este 27 de junio en la [Estela de Luz](https://goo.gl/maps/jiJeYy6MuHB7AxMH8 "cómo llegar a la Estela de Luz")

El repositorio que preparé para la charla, es para el grupo de programadores que organiza en Ciudad de México el evento, y están invitados a participar este 27 de Junio; todos los detalles en [meetup.com](https://www.meetup.com/es/PHP-The-Right-Way/events/258972833/).

Además, si no pueden asistir a esta edición se pueden apuntar a la siguiente meetup. Aunque si gustan de PHP, o son solo desarrolladores Web también estan invitados a participar en [el canal de Slack de la comunidad](https://chat.phpmexico.mx/ "Solicitar invitación al Slack de PHPMX").

Gracias por leer el artículo, y espero les sea de utilidad estos ejemplos de código.

#### Fuentes:

1. [Guzzle Repo Github](https://github.com/guzzle/guzzle "Repositorio oficial de Guzzle")
2. [Manual de Curl PHP](https://www.php.net/manual/es/book.curl.php "Manual de php.net")
3. [Ejemplos de POST con Guzzle](https://dzone.com/articles/make-a-post-request-from-php-with-guzzle "Artículo de DZone")
4. [Ejemplo de FTP con Curl](http://nlslack.com/ftp-access-using-curl-with-php/ "Conectar a un FTP con Curl")
5. [Repositorio de PHPMX](https://github.com/phpwaymx/curlguzzle "Código para la charla de la meetup")
