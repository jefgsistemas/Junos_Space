from jnpr.junos import *
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from lxml import etree
import sys
import os
import smtplib
import time
from pprint import pprint

os.system('cls') #limpia pantalla
dev = Device(host='192.168.0.253', user='root', passwd='juniper1') #construye la instancia para la conexion con el dispositivo (clase device.py)
#dev = Device(mode='serial', port='port', user=usuario, passwd=contrasena, gather_facts=True)

try: 
	dev.open()
	pprint(dev.facts)
	command_hostname = dev.cli("show configuration system host-name") #show chassis hardware | match Chassis"
	time.sleep(5)
	command_conf = dev.cli("show configuration | display set")
	time.sleep(5)
	command_hostname_ss = command_hostname.replace('\n', '').replace(';', '')
	resultado_txtconf = open('dispositivos_recibidos/' + command_hostname_ss.rstrip() + '.txt','a')
	resultado_txtconf.write("<nombre>" + command_hostname_ss + "</nombre>")
	resultado_txtconf.write("\n")
	resultado_txtconf.write(command_conf)
	resultado_txtconf.write("\n")
	resultado_txtconf.close
	
	print "Se exporto la configuracion del equipo con serial " + command_hostname.rstrip()
	dev.close() #cierra la sesion netconf
	
except Exception as Err: #si no se conecta imprime el error
	print "Error al conectarse al dispositivo: ", Err
	#sys.exit(1)		

		
gmail_user = 'jefgsistemas@gmail.com'  
gmail_password = 'VwAjLd2016pc..'
fromt = gmail_user
to = ['jfernandez@qcingenieria.com.co', 'jefgsistemas@gmail.com']  
subject = 'equipo recibido'  
body = 'CONFIGURACION\n\n- You'
email_text = "INICIO VENTANA \n" + command_hostname + "\n" + command_conf + "\n" 
try:  
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(gmail_user, gmail_password)
	server.sendmail(fromt, to, email_text)
	server.close()

	print 'Email enviado!'
except:  
	print 'Error al enviar e-mail'
