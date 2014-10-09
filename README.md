# pyGnoll #

pyGnoll es un bot IRC hecho en Python, el cual es una evolución de
[Gnoll](https://bitbucket.org/radiognu/gnoll) (hecho en PHP), el bot troll del
canal `#radiognu` en irc.radiognu.org.

Esta es una reescritura desde cero, en un esfuerzo de hacer al bot más
eficiente, con más funcionalidades y más fácil de configurar, entre otros
aspectos.

Para hacer funcionar al bot se necesita el modulo de python irc.py
para ello:

En Debian y derivados:

apt-get install python2-pip

luego:

#pip install irc

Si faltan mas cosas, ver el fichero requirements.txt
- - -

## ¿Cómo configurar el bot? ##

Edita el archivo: `configuracion.json`:

```
#!json
{
    "servidor":   "irc.servidor.com",
    "puerto":     6667,
    "canal":      "#canal",
    "nick":       "Gnoll",
    "reconexion": 10
}
```

## ¿Cómo ejecutar el bot? ##

Para iniciar el bot, ejecuta en una consola:

```
#!bash
$ python2 gnoll.py
```

## Funcionalidades de Gnoll ##

Las funcionalidades indicadas con * aún no están disponibles.

* Se autoidentifica cuando entra al canal. *
* Responde de una agradable manera cada vez que le nombran.
* Se asegura de que todos/as los usuarios/as tengan voz. *
* Saluda a ciertos/as usuarios/as cuando ingresan al canal. *
* Detecta malas palabras y advierte a el/la usuario/a que las emite.

## Comandos disponibles ##

Los comandos indicados con * aún no están disponibles.

Comando | Función
------ | :-----
'!comandos' | Muestra una lista de los comandos disponibles.
'!ayuda comando' | Muestra una descripción de ayuda del `comando` indicado.
'!cuantos'| Indica cuantos ñuescuchan la radio en ese momento.
'!sonando'| Indica qué es lo que suena en la radio en ese momento.
'!hablaclaro nick' | Le da un amistoso saludo a `nick`, quien debe ser un usuario/a presente en ese momento en el canal.
'!invitar'* | Invita a los usuarios del canal a conectarse, por que comienza un programa en vivo.
'!cita cita'* | Registra una cita en el archivo de citas.
'!recita'* | Muestra una cita registrada previamente con `!cita`.
'http://www.algo.com` o `www.algo.com` | Devuelve el título de la página web indicada en la URL. En el segundo caso se agrega automáticamente el `http://`.
'!salir' | Termina la ejecución del bot (Sólo operadores).
'!r' | Detiene y reinicia la ejecución del bot, por el tiempo definido en la configuración (Sólo operadores).
'!sl' | Muestra citas celebres de Richard Stallman

Caveats/fallos:

* Si a Gnoll se le pasa codigo no utf-8 se cae... (a veces pasa)
* Si le pasas una url con mas de 256 caracteres en su titulo, tambien se cae...