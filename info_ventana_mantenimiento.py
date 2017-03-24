from jnpr.junos import *
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from lxml import etree
import sys
import os
import smtplib

os.system('cls') #limpia pantalla
contip=0 #contador de direcciones ip
direcciones=[] #arreglo de direcciones ip
usuario="" #usuario de conexion al dispositivo
contrasena="" #contrasena de conexion al dispositivo

direccionesip_txt = open("ip.txt",'r')
for linea in direccionesip_txt.readlines(): 
	contip = contip + 1 #contador para identificar cantidad de ips
	linea = linea.strip('\n')
	direcciones = direcciones + [linea] #agrega al arreglo cada direccion ip del archivo

direccionesip_txt.close()

print "recuerde en el equipo ejecutar el comando: set system services netconf ssh"
usuario = raw_input("ingrese el usuario de los equipos: ")
contrasena = raw_input("ingrese la contrasena de los equipos: ")

def commandget(dev,hostip):
	hostc=hostip
	command_hostname = dev.cli("show configuration system-hostname")
	command_conf = dev.cli("show configuration | display set") 
	command_interfaces = dev.cli("show interfaces terse") 
	command_version = dev.cli("show version")
	command_system_alarms = dev.cli("show system alarms")
	command_chassis_alarms = dev.cli("show chassis alarms") 	
	dev.close() #cierra la sesion netconf 
	
	resultado_txtconf = open("show_configuration.txt",'a')
	resultado_txtconf.write("<host-ip>" + hostc + "</host-ip>")
	resultado_txtconf.write("\n")
	resultado_txtconf.write(command_conf)
	resultado_txtconf.write("\n")
	resultado_txtconf.close
	print "Se exporto la configuracion del equipo con IP " + hostc
	
	resultado_txtinterfaces = open("show_interfaces.txt", 'a')
	resultado_txtinterfaces.write("<host-ip>" + hostc + "</host-ip>")
	resultado_txtinterfaces.write("\n")
	resultado_txtinterfaces.write(command_interfaces)
	resultado_txtinterfaces.write("\n")
	resultado_txtinterfaces.close
	print "Se exporto el estado de las interfaces del equipo con IP " + hostc	
	
	resultado_txtver = open("show_version_and_state.txt", 'a')
	resultado_txtver.write("<host-ip>" + hostc + "</host-ip>")
	resultado_txtver.write("\n")
	resultado_txtver.write(command_version)
	resultado_txtver.write("\n")
	resultado_txtver.write("ALARMAS")
	resultado_txtver.write(command_system_alarms)
	resultado_txtver.write("\n")
	resultado_txtver.write("ALARMAS CHASSIS")	
	resultado_txtver.write(command_chassis_alarms)
	resultado_txtver.close
	print "Se exporto la version alarmas y estado de chassis del equipo con IP " + hostc	
	
	gmail_user = 'jefgsistemas@gmail.com'  
	gmail_password = 'pass'
	fromt = gmail_user
	to = ['jfernandez@qcingenieria.com.co', 'jefgsistemas@gmail.com']  
	subject = 'Configuracion ventana de mantenimiento'  
	body = 'CONFIGURACION\n\n- You'
	email_text = "INICIO VENTANA \n" + command_interfaces + "\n" + command_conf + "\n" + command_version + "\n" + command_system_alarms
	try:  
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(fromt, to, email_text)
		server.close()

		print 'Email enviado!'
	except:  
		print 'Error al enviar e-mail'
	
def verifica_conexiones(hostname,usuario,contrasena):
	dev = Device(host=hostname, user=usuario, passwd=contrasena) #construye la instancia para la conexion con el dispositivo
	try: #abre la conexion netconf con el dispositivo
		dev.open()
		commandget(dev, hostname)
	except Exception as Err: #si no se conecta imprime el error
		print "Error al conectarse al dispositivo: ", Err
		#sys.exit(1)
		
print "las direcciones ip del archivo ip.txt son:"
print ""
for j in range(contip):		
	print direcciones[j]
print ""

for j in range(contip): #envia las direcciones, usuario y contrasena para conectarse
	verifica_conexiones(direcciones[j],usuario,contrasena)

