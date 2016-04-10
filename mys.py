#!/usr/bin/
# -*- coding: latin-1 -*-

import urllib2, httplib
from time import gmtime, strftime

DATENOW = strftime("%d/%m", gmtime())

ERROR = {
	200 : "SE CONECTO A LA PAGINA",
	404 : "NO SE ENCONTRO PAGINA",
}


def getUrlDownload(date):
	URL = "http://www.famaf.unc.edu.ar/academico/carreras-de-grado/licenciatura-en-computacion/modelos-y-simulacion/"

	try:
		response = urllib2.urlopen(URL)

	except urllib2.URLError as e:
		print e
		return -1, -1

	except ValueError as e:
		print e
		return -1, -1

	print ERROR[response.getcode()]

	if response.getcode() != 200:
		return -1, -1

	html = response.read()
	pos = html.find(date + ' ' + '&#8211')

	if pos == -1:
		return -1, -1

	else:
		html = html[pos:]
		pos = html.find('<a href=')
		posUntilURL = html.find('">pdf</a>)')
		theoricURL = html[pos: posUntilURL].split('="', 1)[1]
		html = html[posUntilURL:]

		pos = html.find('<li><strong>Pr')

		if pos == -1:
			return theoricURL, -1

		else:
			html = html[pos:]
			pos = html.find('(<a href=')
			posUntilURL = html.find('">pdf</a>)')
			practicURL = html[pos:posUntilURL].split('="', 1)[1]
			return theoricURL, practicURL

def downloadFiles(URL):
	newURL = URL[0:len(URL) - 1] + str(1) + "&pv=1"
	response = urllib2.urlopen(newURL)

	fileName = URL.split('/') [-1].split('?') [0].split('_') [0] + '.pdf'
	f = open(fileName, 'wb')
	# HACERLO DE A PEDAZOOOS
	f.write(response.read())

	f.close()


if __name__ == "__main__":
	resp = '\0'

	while resp != 'y' and resp != 'n': 
		resp = raw_input('Quiere día actual? y/n ')

		if resp == 'n':
			date = raw_input('Ingrese día formato dia/mes ')

		elif resp == 'y':
			date = DATENOW

		else:
			print "Respuesta no permitida, por favor ingrese nuevamente: y/n (y o n))"

	theoricURL, practicURL = getUrlDownload(date)

	if theoricURL == -1:
		print "NO SE ENCONTRO CONTENIDO EN LA PAGINA"
		exit()

	downloadFiles(theoricURL)
	print "CONTENIDO TEORICO LISTO..."

	if practicURL == -1:
		print "CONTENIDO PRÁCTICO NO ESTA"
		exit()

	downloadFiles(practicURL)
	print "CONTENIDO PRACTICO LISTO..."
	exit()

