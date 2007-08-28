# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Preguntes
#
# Carles 24/08/2007
#

global textpreguntes

textpreguntes = (
#inici_importació

( 1, u"On es va fer la Guadec de l'any 2006?", u"Chicago",u"Vilanova i la Geltrú",u"Sao Paulo", 2, u"Carles",u"18/08/07",u"", 1 ), 
( 2, u"Quins mesos de l'any surt cada#versió nova d'ubuntu?", u"Febrer i novembre",u"Març i setembre",u"Abril i octubre", 3, u"Carles",u"18/08/07",u"El nombre de la versió correspon amb l'any i el mes. (7.10=2007 octubre)", 2 ), 
( 3, u"Qui va crear el format HTML?", u"Tim Berners-Lee",u"Wim Mertens",u"Manuel de Icaza", 1, u"Carles",u"18/08/07",u"", 3 ), 
( 4, u"El wesnoth és un joc de tipus", u"Arcade Shooter",u"Aventura gràfica",u"Estratègia per torns", 3, u"Nil",u"18/08/07",u"", 4 ), 
( 5, u"Per trinxar ben trinxat l'ordinador farem:", u"sudo rm -d -f -r /",u"sudo cp /dev/hdb1 > aixo.iso",u"echo destroy computer contents", 1, u"Carles",u"18/08/07",u"", 5 ), 
( 6, u"El millor editor lliure d'imatges matricials és:", u"gimp",u"gaim",u"gcc", 1, u"Nil",u"18/08/07",u"El gimp és un programa de tractament d'imatges, el gaim de missatgeria instantània (ara rebatejat com a pidgin) i el gcc el compilador de llenguatge c i c++. ", 6 ), 

#fi_importació
)


##########################################
# RainCT

preguntes = []

for num in range(0,6):
	preguntes.append( [] )

for element in textpreguntes:
	preguntes[ element[0] - 1 ].append( element )

print preguntes[0]
