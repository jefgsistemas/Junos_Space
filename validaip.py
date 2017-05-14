#valida si la direccion IP enviada si tiene el patron correcto 
import re
	
def validacampos(ip):
	a = 0
	ip_patron = re.match('([0-2][0-9][0-9]|[0-9][0-9]|[0-9])(\.)([0-2][0-9][0-9]|[0-9][0-9]|[0-9])(\.)([0-2][0-9][0-9]|[0-9][0-9]|[0-9])(\.)([0-2][0-9][0-9]|[0-9][0-9]|[0-9])', ip)
	if not ip_patron:  #valida el patron ###.###.###.###
		return False
	#print(ip_patron.groups())
	patron = re.compile('\.')
	for num in patron.split(ip):
		a += 1
		if a > 4: # valida si excede el numero de octetos
			return False
		
		if int(num) > 255: #valida si cada octeto supera 255
			return False
	return True
			
print validacampos('192.0.290.2')
