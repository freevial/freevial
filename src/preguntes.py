# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Preguntes
#
# Carles 24/08/2007
#

textpreguntes = (
#inici_importació

( 1, u"On es va fer la Guadec de l'any 2006?", u"Chicago",u"Vilanova i la Geltrú",u"Sao Paulo", 2, u"Un",u"18/08/07",u"", 1 ), 
( 2, u"Quins mesos de l'any surt cada#versió nova d'ubuntu?", u"Febrer i novembre",u"Març i setembre",u"Abril i octubre", 3, u"Un",u"18/08/07",u"El nombre de la versió correspon amb l'any i el mes. (7.10=2007 octubre)", 2 ), 
( 3, u"Qui va crear el format HTML?", u"Tim Berners-Lee",u"Wim Mertens",u"Manuel de Icaza", 1, u"Dos",u"18/08/07",u"", 3 ), 
( 4, u"El wesnoth és un joc de tipus", u"Arcade Shooter",u"Aventura gràfica",u"Estratègia per torns", 3, u"Nil",u"18/08/07",u"", 4 ), 
( 5, u"Per trinxar ben trinxat l'ordinador farem:", u"sudo rm -d -f -r /",u"sudo cp /dev/hdb1 > aixo.iso",u"echo destroy computer contents", 1, u"Carles",u"18/08/07",u"", 5 ), 
( 6, u"El millor editor lliure d'imatges matricials és:", u"gimp",u"gaim",u"gcc", 1, u"Nil",u"18/08/07",u"El gimp és un programa de tractament d'imatges, el gaim de missatgeria instantània (ara rebatejat com a pidgin) i el gcc el compilador de llenguatge c i c++. ", 6 ), 
( 4, u"Quin personatge de videojoc considerava#que els noms no eren importants?", u"Lara Croft",u"Guybrush Threepwood",u"Larry Laffer", 2, u"Carles",u"18/08/07",u"En Guybrush Threepod. Protagonista de la saga monkey island que podem jugar amb el scummvm. Quan els dissenyadors van crear el personatge el programa que usaven per fer-ho s'anomenava brush i no van decidir el nom fins al final. Ells l'anomenaven el “tio” del brush (Guy_Brush) i així és com es va dir. En tota la saga monkey island els personatges se'n foten continuament del seu nom", 7 ), 
( 1, u"Qui va dir#'Don't think free as in free beer;#think free as in free speech.'", u"Richard Stallman",u"Linus Torvalds",u"Mark Shuttlework", 1, u"Marta Ferrussola",u"18/08/07",u"Richard Stallman per referir-se que el programari hauria de ser lliure referint-se a llibertat. (És un error de polisemia en anglès al ser lliure i gratuit la mateixa paraula: free)", 8 ), 
( 1, u"Quants anys ha fet l'escriptori gnome?#(2007)", u"10",u"15",u"20", 1, u"Carles",u"18/08/07",u"", 9 ), 
( 1, u"Qui va fundar el projecte gnome?", u"Mark Shuttlework",u"Manuel de Icaza",u"George Moustaki", 2, u"Altre",u"18/08/07",u"", 10 ), 

#fi_importació
)


##########################################
# RainCT

from freevialglob import *

preguntes = []
preguntes_autors = {}

def shuffleQuestions( questions ):
	""" Returns the given questions list, but shuffled. """
	
	for num in range(0, 6):
		random.shuffle( questions[num] )
	
	return questions

for num in range(0, 6):
	preguntes.append( [] )

for element in textpreguntes:

	preguntes_autors[element[6]] = element[6]
	preguntes[ element[0] - 1 ].append( element )

# Copy the questions to get them back if a categories gets empty
preguntes_backup = preguntes

preguntes = shuffleQuestions(preguntes)
