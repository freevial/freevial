#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

#cadena = u"On es va fer la Guadec#de l'any 2006?"
cadena2 = u"On es va fer la Guadec#de l'any 2006?"

#separador = re.compile('[#]*')
#cadenes = separador.findall( cadena2 );

cadenes = re.split( '#', cadena2 )

for cadena in cadenes:
	print cadena

pregunta = u"On es va fer la Guadec#de l'any 2006?"
cadenes = re.split( '#', pregunta )

for cadena in pregunta:
	print cadena
