#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# pyGnoll - Versión en python de Gnoll, el bot de RadioÑú
#
# Versión ???
#
#  Copyleft 2014 Tomás Vielma (@tomivs in twitter) <contacto@tomivs.com>
#                Felipe Peñailillo Castañeda (@breadmaker in identi.ca)
#                    <breadmaker@radiognu.org>
#                Dj_Dexter (@djdexter in identi.ca) <djdexter@gentoo-es.com> 
#
# Este programa es software libre; puede redistribuirlo y/o modificarlo bajo
# los términos de la Licencia Pública General GNU tal como se publica por
# la Free Software Foundation; ya sea la versión 3 de la Licencia, o
# (a su elección) cualquier versión posterior.
#
# Este programa se distribuye con la esperanza de que le sea útil, pero SIN
# NINGUNA GARANTÍA; sin incluso la garantía implícita de MERCANTILIDAD o
# IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Vea la Licencia Pública
# General de GNU para más detalles.
#
# Debería haber recibido una copia de la Licencia Pública General de GNU
# junto con este programa; de lo contrario escriba a la Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, EE. UU.

import sys
import re
import irc.bot
import simplejson as json
import requests
import HTMLParser
from BeautifulSoup import BeautifulSoup
from pprint import pprint
from random import choice

reload(sys)
sys.setdefaultencoding('utf-8')

## INICIANDO CONFIGURACIONES ##
try:
   conf = json.loads(open("configuracion.json").read())
except Exception, e:
   print "Hubo un error al intentar leer el archivo de configuración:"
   print "La excepción original es:"
   raise e

# define a Gnoll
class pyGnoll(irc.bot.SingleServerIRCBot):
   def __init__(self, channel, nickname, server, realname, port=6667):
      irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname,
         realname, reconnection_interval=conf["reconexion"])
      self.channel = channel

   # define un comportamiento cuando el nick ya está en uso
   def on_nicknameinuse(self, c, e):
      c.nick(c.get_nickname() + "_")

   # define un comportamiento al entrar al servidor
   def on_welcome(self, c, e):
      c.join(self.channel)

   # define un comportamiento cuando un usuario entra al canal
   def on_join(self, c, e):
      return

   # define un comportamiento cuando se le envían mensajes privados al bot
   def on_privmsg(self, c, e):
      if self.channels[conf["canal"]].is_oper(e.source.nick):
         texto = e.arguments[0].split(" ")
         self.ejecutar(e.source.nick, texto[0], texto[1] if len(texto) > 1
            else "")
      else:
         self.connection.privmsg(e.source.nick,
            "ola k ase intenta hablar con un bot o k ase")

   # define un comportamiento cuando se envían mensajes al canal
   def on_pubmsg(self, c, e):
      self.logear(e.source.nick, e.arguments[0])
      regex_malaspalabras = \
         re.compile(open("textos/malaspalabras.txt").read().replace("\n", "|"),
            re.IGNORECASE)
      if regex_malaspalabras.search(e.arguments[0]):
         c.privmsg(conf["canal"], "%s: ¿pudieras dar esa magistral demostración"
            " de léxico con menos frecuencia?" % e.source.nick)
      regex_comando = re.compile("(!(?:[a-z][a-z]+))", re.IGNORECASE)
      if regex_comando.search(e.arguments[0]):
         texto = e.arguments[0].split("!")[1:][0].split(" ")
         self.ejecutar(e.source.nick, texto[0], texto[1] if len(texto) > 1
            else "")
      regex_nombrado = re.compile(conf["nick"], re.IGNORECASE)
      if regex_nombrado.search(e.arguments[0]):
         self.nombrado(c, e)
      regex_url_http = re.compile(ur'((?:http|https)(?::\/{2}[\w]+)'
         '(?:[\/|\.]?)(?:[^\s"]*))', re.IGNORECASE)
      regex_url_www = re.compile(ur'((?:[a-z][a-z\.\d\-]+)'
         '\.(?:[a-z][a-z\-]+))(?![\w\.])', re.IGNORECASE)
      if regex_url_http.search(e.arguments[0]):
         self.titulo_url(c, e.source.nick,
            regex_url_http.findall(e.arguments[0])[0])
      elif regex_url_www.search(e.arguments[0]):
         self.titulo_url(c, e.source.nick,
            "http://%s" % regex_url_www.findall(e.arguments[0])[0])

   # función que se ejecuta como respuesta cuando el bot es nombrado
   def nombrado(self, c, e):
      respuesta = re.sub("____NICK____", e.source.nick,
         choice(open('textos/nombrado.txt').readlines()))
      c.privmsg(conf["canal"],
         respuesta.rstrip('\n').decode("utf-8", "replace"))

   # función que se ejecuta cuando es detectada una url. Devuelve el título de
   # la url indicada
   def titulo_url(self, c, nick, url):
      try:
         titulo = requests.post("http://url-to-title.herokuapp.com/",
            data = {"url": url})
      except Exception, e:
         print e
         titulo = ("Hubo un problema al intentar acceder al servicio. Intenta"
                   " más tarde.")
      parser = HTMLParser.HTMLParser()
      c.privmsg(conf["canal"], "%s: %s" % (nick,
         parser.unescape(str(titulo.content))))

   # función para registrar los eventos del canal
   def logear (self, nick, msg):
      print "%s: %s" % (nick, msg)

   # función para interpretar y ejecutar comandos
   def ejecutar(self, nick, cmd, arg):
      c = self.connection
      if cmd == "r":
         if self.channels[conf["canal"]].is_oper(nick):
            self.disconnect("Vuelvo en ~%d segundos" % conf["reconexion"])
# Funcion deshabilitada, si es que hay operadores troles que haran cerrar al Gnoll o_O
#      elif cmd == "salir":
#         if self.channels[conf["canal"]].is_oper(nick):
#            self.die("init 0")
      elif cmd == "comandos" or (cmd == "ayuda" and arg == ""):
         ayuda = json.loads(open("textos/ayuda.json").read())
         c.privmsg(conf["canal"], "%s: Los comandos que de vaina me sé: %s" \
            % (nick, ayuda["comandos"]))
         c.privmsg(conf["canal"], "Para más detalles, !ayuda comando, p.ej. "
            "!ayuda url")
         if self.channels[conf["canal"]].is_oper(nick):
            c.privmsg(nick, "Comandos para OPs: %s. Puedo escuchar estos mismos"
            " comandos aquí, sin agregar '!', p.ej. sonando" \
               % ayuda["comandos_op"])
      elif cmd == "ayuda" and arg != "":
         ayuda = json.loads(open("textos/ayuda.json").read())
         if arg == "salir" or arg == "r":
            if self.channels[conf["canal"]].is_oper(nick):
               c.privmsg(nick, ayuda[arg])
         else:
            c.privmsg(conf["canal"],
               ayuda.get(arg, "Creo que ese comando no existe..."))
      elif cmd == "hablaclaro":
         if arg != "":
            if arg in self.channels[conf["canal"]].users():
               hablaclaro = choice(open('textos/hablaclaro.txt').readlines()) \
                  .rstrip("\n")
               c.privmsg(conf["canal"], "%s: HABLA CLARO %s" \
                  % (arg, hablaclaro))
            else:
               c.privmsg(conf["canal"], "%s: ¿%s? ¿Y ése/a quién es?" \
                  % (nick, arg))
      elif cmd == "sonando":
         peticion = requests.get('http://radiognu.org/api/?no_cover')
         datos = peticion.json()
         if datos['isLive']:
            sonando = "EN VIVO: «%s» de %s transmite “%s” de ‘%s’" \
               % (datos['show'].encode("utf-8", "replace"),
                  datos['broadcaster'].encode("utf-8", "replace"),
                  datos['title'].encode("utf-8", "replace"),
                  datos['artist'].encode("utf-8", "replace"))
            c.privmsg(conf["canal"], sonando.decode("utf-8", "replace"))
         else:
            sonando = "SONANDO EN DIFERIDO: “%s” de ‘%s’ del álbum «%s» " \
               "(%s, %s%s)" % (datos['title'].encode("utf-8", "replace"),
                  datos['artist'].encode("utf-8", "replace"),
                  datos['album'].encode("utf-8", "replace"),
                  datos['country'].encode("utf-8", "replace"), datos['year'],
                  ", " + datos['license']['shortname'] if datos["license"]
                  != "" else "")
            c.privmsg(conf["canal"], sonando.decode("utf-8", "replace"))
      elif cmd == "cuantos":
         peticion = requests.get('http://radiognu.org/api/?no_cover')
         datos = peticion.json()
         archivo = open('textos/cuantos.txt').readlines()
         salida = re.sub('____NICK____', nick, re.sub('_X_',
            str(datos['listeners']), choice(archivo))).rstrip('\n')
         c.privmsg(conf["canal"], salida.decode("utf-8", "replace"))
      elif cmd == "chucknorris":
         c.privmsg(conf["canal"],
            choice(open("textos/chucknorris.txt").readlines()).rstrip("\n"))
      elif cmd == "sl":
         c.privmsg(conf["canal"],
            choice(open("textos/rms.txt").readlines()).rstrip("\n"))
def main():
   bot = pyGnoll(conf["canal"], conf["nick"], conf["servidor"],
      u"El bot troll de RadioÑú", conf["puerto"])
   bot.start()

if __name__ == "__main__":
   main()