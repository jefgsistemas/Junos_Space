##Este script solicita interfaz loopback valida si es protect-vrf
#Numero de incidente para modificar
#Escrito por: Jorge fernandez 
#Empresa QyC Ingenieria
#Version 1.0
import yaml
from pprint import pprint
from jnpr.junos import *
from getpass import getpass
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from lxml import etree
import sys
import os
import time

os.system('cls')
devcom = Device(host='192.168.0.253', user='root', passwd='juniper1')
try:
	devcom.open()
except ConnectError as err:
	print "Cannot connect to device: {0}".format(err)
	sys.exit(1)

command = devcom.cli("show configuration interfaces em0 unit 0 family inet filter") #OJO se comentario la libreria Lib\jnpr\junos\device.py line 652
devcom.close()
#print command.strip(); strip elimina espacios al principio y fin de la cadena command

if command.strip()=='input protect-vrf;':
	print "la Politica de la interfaz es protect-vrf";
else:
	print "la Politica de la interfaz no es protect-vrf";

print "recuerde en el equipo ejecutar el comando: set system services netconf ssh"
dev = Device(host='192.168.0.253', user='root', passwd='juniper1') #construye la instancia para la conexion con el dispositivo


try: #abre la conexion netconf con el dispositivo
	dev.open()
except Exception as Err:
	print "Error al conectarse al dispositivo: ", Err
	sys.exit(1)

print "CARACTERISTICAS DEL EQUIPO CONECTADO"
pprint(dev.facts) #imprime las propiedades del dispositivo	
dev.bind( cu=Config )
print ""
interface = raw_input("Ingrese nombre de la interfaz em: ")
incidente = raw_input("Ingrese numero de incidente: ")
opcion = raw_input("Esta seguro de aplicar en interfaz em" + interface + " con incidente " + incidente + " y/n: ")

def commandset(config): #funcion que ejecuta el comando enviado
	try:
		dev.cu.load(config, format="set", merge=True)
		print "Ejecutando configuracion 100%"
	except ValueError as err:
		print "Error en la ejecucion del comando", err.message
		dev.close()

def commit_verifica(): 				# funcion que valida la configuracion
	print "Verificando configuracion"
	try:
		dev.cu.commit_check()
		result = dev.cu.commit_check() # si result es true la configuracion es valida
		print "Configuracion valida 100%"
		time.sleep(5)
		commit() 					#llama la funcion commit
		dev.close() 				#cierra la sesion netconf 
	except CommitError:
		print "Error: Verificando la configuracion"
		dev.close()	
		
def commit(): 						# funcion que guarda la configuracion en el dispositivo
	try:
		#dev.cu.commit(comment='cambio fltro', sync=True)
		comentario = "cambio de filtro loopback por usuario root " + incidente
		dev.cu.commit(comment=comentario) #run show system commit para ver cambio
		print "Guardando la configuracion 100%"
	except CommitError:
		print "Error: Habiilite para desbloquear la configuracion"
		print "Desbloquee la configuracion"
		try:
			dev.cu.unlock()
		except UnlockError:
			print "Error: Habilite para desbloquear la configuracion"
			dev.close()	

commandset("""set interfaces em0 unit 0 family inet filter input protect-vrf""")
#commandset("""show version""")
commit_verifica()
