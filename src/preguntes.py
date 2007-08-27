# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Preguntes
#
# Carles 24/8/2007
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
( 4, u"Quin personatge de videojoc considerava#que els noms no eren importants?", u"Lara Croft",u"Guybrush Threepwood",u"Larry Laffer", 2, u"Carles",u"18/08/07",u"En Guybrush Threepod. Protagonista de la saga monkey island que podem jugar amb el scummvm. Quan els dissenyadors van crear el personatge el programa que usaven per fer-ho s'anomenava brush i no van decidir el nom fins al final. Ells l'anomenaven el “tio” del brush (Guy_Brush) i així és com es va dir. En tota la saga monkey island els personatges se'n foten continuament del seu nom", 7 ), 
( 1, u"Qui va dir#'Don't think free as in free beer;#think free as in free speech.'", u"Richard Stallman",u"Linus Torvalds",u"Mark Shuttlework", 1, u"Carles",u"18/08/07",u"Richard Stallman per referir-se que el programari hauria de ser lliure referint-se a llibertat. (És un error de polisemia en anglès al ser lliure i gratuit la mateixa paraula: free)", 8 ), 
( 1, u"Quants anys ha fet l'escriptori gnome?#(2007)", u"10",u"15",u"20", 1, u"Carles",u"18/08/07",u"", 9 ), 
( 1, u"Qui va fundar el projecte gnome?", u"Mark Shuttlework",u"Manuel de Icaza",u"George Moustaki", 2, u"Carles",u"18/08/07",u"", 10 ), 
( 1, u"Quan em Mark Shuttleworth va fer# la seva fortuna venent#una empresa de claus va anar de viatge a:", u"Vilanova i la Geltrú",u"L'espai",u"Everest", 2, u"Carles",u"18/08/07",u"Mark Shuttleworth va ser el 2on turista espacial de la història de la humanitat. Després d'aconseguir la seva fortuna va fer un viatge a l'estació espacial internacional amb un grup de científics per tal de realitzar investigacions amb celules mare.", 11 ), 
( 2, u"Canonical és una empresa situada a:", u"Zimbawe",u"Sud africa",u"Illa de man", 3, u"Carles",u"18/08/07",u"", 12 ), 
( 3, u"El fòrum de l'equip Català d'ubuntaires#el podem trobar a:", u"ubuntuforums.org",u"forum.ubuntu.pl",u"ubuntu-fr.org", 1, u"Carles",u"18/08/07",u"Concretament a http://ubuntuforums.org/forumdisplay.php?f=206. També podem anar-hi desde el portal www.ubuntu.cat", 13 ), 
( 5, u"Una mica de C.#Si: define MAX(A,B) ( ((A) > B) ? (A) : (B) )#i assignem x = 1; y = 2; #el resultat de MAX( ++x, ++y ) és?", u"2",u"3",u"4", 3, u"Carles",u"18/08/07",u"Ja que al ser una macro i no una funció al substituir paràmetres es realitza 2 cops el preincrement de y (++y)", 14 ), 
( 4, u"Quina versió del wine esta especialitzada#per fer rutllar jocs?", u"CrossOver",u"Cedega",u"xmame", 2, u"Carles",u"18/08/07",u"El xmame és un emulador de màquines de videjocs i no una versió del wine", 15 ), 
( 4, u"Quina eina usa la Trinity a Matrix Reloaded#per petar l'ordinador.", u"nmap",u"aircrack",u"el càssic dir c:\ de totes les pelis", 1, u"Carles",u"18/08/07",u"En la película Matrix Reloaded podem veure a Trinity petant un ordinador i a la pantalla es veu com realitza un escaneig de seguretat amb l'eina nmap!!! Un com fet això és mostra una vulnerabilitat real (exploit SSHv1 CRC32) un error de buffer, que amb una eina fingida sshnuke aprofita.", 16 ), 
( 4, u"Com avisa Maurice Moss als bombers#quan es crema el seu despatx?", u"IRC",u"Missatgeria instantània",u"correu electrònic", 3, u"Carles",u"18/08/07",u"A la serie IT crowd quan s'estan cremant les oficinies i devant l'impossibilitat de recordar el telèfon dels bombers en Maurice Moss envia un mail per avisar-los. ( Fire... exclamation mark.)", 17 ), 
( 1, u"L'any 1977 la policia d'alburquerque va#detenir i fitxar a Bill Gates per", u"Tenir drogues",u"Robar una pastisseria",u"Fer curses amb un 911 al desert", 3, u"Carles",u"18/08/07",u"A la xarxa podem trobar la foto d'un jove Bill amb la seva fitxa policial... una monada. http://news.bbc.co.uk/1/hi/sci/tech/152803.stm", 18 ), 
( 5, u"Quin d'aquests llenguatges no funciona#sobre una màquina virtual", u"java",u"python",u"c#", 2, u"Carles",u"18/08/07",u"És un llenguatge semi-interpretat", 19 ), 
( 5, u"GTK Vol dir", u"Gimp ToolKit",u"Graphics Team Kit",u"Gnome Toolkit", 1, u"carles",u"18/08/07",u"Les llibreries GTK sobre les que després es va basar el gnome  van crear-se per realitzar el programa gimp", 20 ), 
( 1, u"Com es diu l'associació d'usuaris de linux#més important de Catalunya", u"Cobrem",u"Caliu",u"Carlux", 3, u"carles",u"18/08/07",u"I el seu Secretari Rafael Carreras és un dels fundadors del LoCo Català d'ubuntaires", 21 ), 
( 6, u"El mythtv no permet", u"Veure i enregistrar la tele",u"Fer video trucades",u"Fer PDFs", 3, u"carles",u"18/08/07",u"És un sistema media center collonut però no serveix per fer PDFs", 22 ), 
( 2, u"Quin d'aquests formats es pot llegir#amb la instaŀlació predeterminada#d'ubuntu", u"mp3",u"dvd",u"ogg", 3, u"carles",u"18/08/07",u"Els formats mp3 i dvd (mpeg) son formats restrictius, un protegit per patents i l'altre en alguns països no es pot ni mostrar les fonts ja que implica el rebentar la protecció dels dvds. Malgrat tot no hi ha cap problema per usar qualsevol d'ells un cop instaŀlat el sistema", 23 ), 
( 1, u"Que va patentar Microsoft#el 24 de setembre del 96", u"El CD parcialment reescribible",u"El doble click",u"La bola del mouse", 2, u"carles",u"18/08/07",u"Patent number: 5559943", 24 ), 
( 1, u"Què es va patentar el 2006", u"El teletransport",u"La inserció de xips al cervell humà",u"El windows segur", 1, u"carles",u"18/08/07",u"United States Patent 20060071122. Brutal no!!!", 25 ), 
( 6, u"Quin animal d'aquests és germà#però no amic de la guineu de foc", u"L'escarabat de neu",u"La llúdriga de gel",u"La gavina de foc", 2, u"carles",u"18/08/07",u"L'any 2006 l'equip de debian va fer una separació de la versió oficial del firefox per que l'equip de treball de mozilla no incorporava les seves actualitzacions a temps. Al fer-ho van haver de canviar el logotip d'aquest per un altre ja que estava protegit per drets d'autor.", 26 ), 
( 1, u"Qui ha estat un l'abanderat de la traducció#del programari al català?", u"softcatalà",u"la generalitat",u"microsoft", 1, u"carles",u"18/08/07",u"Per cert... el clic dels nois de redmon ja s'a convertit en clico.", 27 ), 
( 2, u"L'ubuntu és un sistema operatiu del tipus", u"Unix",u"Linux",u"GNU amb Linux", 3, u"carles",u"18/08/07",u"EL sistema operatiu és GNU amb Linux. Linux sols és el nucli d'aquest i es un component més tant important com qualsevol altre", 28 ), 
( 2, u"En Mark Shuttleworth va considerar#que el LoCo Català era", u"Una colla de merdetes",u"Una llàstima",u"Un exemple a seguir", 3, u"carles",u"18/08/07",u"sabdfl  this is pretty fantastic - i love the fact that there is participation from cultural, artistic, development, linguisitic and educational sources", 29 ), 
( 6, u"Quin d'aquests no és un gestor#de finestres en ubuntu", u"openbox",u"fartbox",u"fluxbox", 2, u"carles",u"18/08/07",u"fartbox vol dir la capsa dels pets", 30 ), 
( 2, u"Quin d'aquests sistema d'arxius no es#pot llegir i escriure en ubuntu", u"ext3",u"ntfs",u"sata", 3, u"carles",u"18/08/07",u"sata no és un sistema d'arxius", 31 ), 
( 1, u"Què es va celebrar el passat abril al#Centre cultural de les Corts??", u"Una reunió tupperware",u"L'RMS hi va fer una conferència",u"La Festa Feisty del CatalanTeam", 3, u"papapep",u"18/08/07",u"", 32 ), 
( 2, u"Quin és el nick a l'irc#d'en Mark Shuttleworth?", u"sabdfl",u"sticsis",u"rtfm", 1, u"papapep",u"18/08/07",u"Self-Appointed Benevolent Dictator For Life", 33 ), 
( 4, u"En un capítol de la sèria 'Porca missèria'#es veu un entorn gràfic de Linux, quin?", u"KDE",u"Gnome",u"XFCE", 1, u"papapep",u"18/08/07",u"", 34 ), 
( 1, u"Qui son Dennis Ritchie i Keneth Thompson?", u"Els desenvolupadors del C i del unix",u"Els pares d'internet",u"Els creadors del projecte GNU", 1, u"carles",u"24/08/07",u"De l'any 1969 al 1971 Dennis Ritchie i Keneth Thompson ven desenvolupar el sistema unix. Per fer-ho van haver de millorar el lleguatge B creat per Ritchie convertint-lo en C ", 35 ), 
( 5, u"Per què el C++ s'anomena així?", u"Per que és un C millorat#(més i millor ++)",u"Per què C + 1 en C s'escriu C++",u"Les dues creus son en memòria#dels desenvolupadors del C", 2, u"carles",u"24/08/07",u"Abans hi havia el B després va venir el C (B+1) i C + 1 en C s'escriu C++", 36 ), 
( 4, u"De què és acrònim HAL a la película 2001#(tot i que ho negui Arthur C Clarck) ", u"Hardware Adapter Layer",u"Home and leisure",u"International Busines Machines", 2, u"carles",u"24/08/07",u"IBM = I - 1 = H, B - 1 = A, M - 1 = L", 37 ), 
( 3, u"Existeix una entrada explicant#la viquipèdia a la viquièdia?", u"Clar",u"No.",u"Sols si cerquem wikipedia", 1, u"carles",u"24/08/07",u"I doncs que us pensàveu?", 38 ), 
( 3, u"Quin any es va fundar google?", u"1995",u"1998",u"2000", 2, u"carles",u"24/08/07",u"Oi que sembla que fes més temps?", 39 ), 
( 3, u"Quina d'aquestes xarxes#no existia abans d'internet?", u"fidonet",u"compuserve",u"comnet", 3, u"carles",u"24/08/07",u"Compuserve va ser la primera xarxa pública mundial d'accés públic. Fidonet (anterior a compuserve) era una xarxa d'enllaços entre les anteriors BBS.", 40 ), 
( 5, u"A què anomenem hacker?", u"Expert",u"Persona que trenca#els sistemes de seguretat",u"Pirata", 1, u"carles",u"24/08/07",u"Un hacker és un expert ... pot ser-ho en art (japó) o en en nucli del linux o en el funcionament d'un programa. Cal no confondre-ho com fan els mitjans amb els crackers o els pirates.", 41 ), 
( 3, u"Quin d'aquests no és un “hoax”?", u"La llet es repasteuritza segons#el nombre inferior del tetrabrick",u"Un nombre fa que la facturació#del telèfon d'un altre te la cobrin a tu",u"El microsoft vista fa que l'ordinador#vagi malament si detecta un dispositiu#que permet copiar películes", 3, u"carles",u"24/08/07",u".... si... lamentable. Si el sistema de control de copies DRM detecta que tens algun mitjà que permet realitzar copies de peŀlicules o videos aquest baixarà la qualitat per que no ho puguis fer correctament. A l'hora totes aquestes comprovacions fan que l'ordinador funcioni molt més lent.", 42 ), 
( 1, u"Hans Reiser, creador del sistema#d'arxius ReiserFS, va ser acusat#l'any passat de:", u"Signar un acord amb Microsoft",u"Matar la seva dona",u"Violar la GPLv3", 2, u"lluisanunez",u"24/08/07",u"http://en.wikipedia.org/wiki/Hans_Reiser", 43 ), 
( 2, u"GoBUNTU és:", u"Una versió d'Ubuntu amb#només Gnome",u"Una versió d'UBUNTU amb#només programari lliure",u"La distribució, basada en#UBUNTU, dels aficionats al GO", 2, u"lluisanunez",u"24/08/07",u"http://en.wikipedia.org/wiki/Gobuntu", 44 ), 
( 3, u"La tecnologia que fa possible l'alimentació#automàtica de notícies web es diu:", u"CSS",u"RSS",u"SMS", 2, u"lluisanunez",u"24/08/07",u"", 45 ), 
( 4, u"El clon per linux dels famosos#Lemmings es diu:", u"SuperTux",u"Tux Race",u"Pingus", 3, u"lluisanunez",u"25/08/07",u"Supertux és un clon de Super Mario, Tux Racer és un joc d'animació 3D ", 46 ), 
( 5, u"La combinació control+C, en un terminal,#serveix per a:", u"Aturar el procés en marxa",u"Copiar",u"Compilar", 1, u"lluisanunez",u"24/08/07",u"https://wiki.ubuntu.com/JosepS%c3%a0nchez/documentaci%c3%b3/interpret_comandes :-)", 47 ), 
( 6, u"Quina de les següents aplicacions#NO es troba als repositoris d'Ubuntu?", u"Karacul",u"Caca",u"Moc", 1, u"lluisanunez",u"24/08/07",u"Kalcul és una aplicació de KDE, Karacul és inventat ", 48 ), 
( 6, u"Quin animal és la mascota del kde?", u"Un drac",u"Una salamandra",u"Un pingüí", 1, u"carles",u"25/08/07",u"", 49 ), 
( 1, u"Quan Mark Shuttleworth va ser a Catalunya#Quina televisió el va entrevistar?", u"Barcelona TV",u"Mataró TV",u"TV3", 2, u"carles",u"25/08/07",u"", 50 ), 
( 4, u"En quina peli un ordinador deia:#Quin joc més extrany, la unica#manera de guanyar és no jugar.", u"Matrix",u"Tron",u"Jocs de guerra", 3, u"carles",u"25/08/07",u"Quan l'ordinador descrobria la insensatesa de la guerra", 51 ), 
( 4, u"Com es deia el noi que duia el#Mazinger Z?", u"Akira Toriyama",u"Koji Kabuto",u"Yawara Inokuma", 2, u"carles",u"25/08/07",u"", 52 ), 
( 1, u"Per què els errors informàtics es diuen 'bugs'?", u"Per què sona simpàtic",u"per que quan van engegar el primer#ordinador dins d'una valvula#hi havia un insecte",u"En honor a John Bughs", 2, u"carles",u"25/08/07",u"", 53 ), 
( 2, u"Quina d'aquestes funcions#no té el launchpad", u"Reportar bugs",u"Traduir programes",u"Descarregar actualitzacions", 3, u"carles",u"25/08/07",u"", 54 ), 
( 2, u"Quin d'aquests paquets no#serveix per instaŀlar programes", u"synaptic",u"ginstaller",u"adept", 2, u"carles",u"25/08/07",u"", 55 ), 
( 4, u"Quan es va fer la pelicula Tron#Què volia dir aquest comanda?", u"TRace ON. Per debugar",u"Transient on-line",u"TeRminal ON", 1, u"carles",u"25/08/07",u"", 56 ), 
( 3, u"Com es coneixen popularment#a la xarxa els jocs que han deixat#de comercialitzar-se.", u"oldwares",u"abandonwares",u"softdeads", 2, u"carles",u"25/08/07",u"", 57 ), 
( 1, u"Quans euros va recaptar l'sgae el 2005?", u"318.772.000",u"31.877.200",u"3.187.720", 1, u"carles",u"25/08/07",u"i encara no cobraven ni de bon tros tot el que cobren ara", 58 ), 
( 6, u"Quin d'aquests programes#no és un programa de diseny#vectorial", u"scribus",u"inkscape",u"xaralx", 1, u"carles",u"25/08/07",u"es un programa d'autoedició", 59 ), 
( 3, u"Quin ha estat considerat per omnium#cultural el#'Més gran cançoner català del mon '", u"cantar i xerinola",u"kumbaworld",u"yahoo lyrics", 2, u"carles",u"26/08/07",u"he he... ha estat superior a mi... ha havia de fer...", 60 ), 
( 3, u"Què vol dir CC?", u"CertifiCations",u"creative comons",u"computer case", 2, u"carles",u"26/08/07",u"", 61 ), 
( 4, u"Quin any es va fer el joc Pong?", u"1982",u"1978",u"1972", 3, u"carles",u"26/08/07",u"El 29 de novembre del 1972 atari va treure aquest joc. ", 62 ), 
( 5, u"ls serveix per:", u"llistar fitxers",u"comprimir arxius",u"veure l'espai lliure al disc", 1, u"carles",u"26/08/07",u"", 63 ), 
( 2, u"Quina d'aquestes característiques#no inclou l'edubuntu?", u"Gestionar horaris d'una escola",u"Iniciar ordinadors en xarxa#sense instaŀlar, ni posar CDs",u"Veure DVDs zona 2", 3, u"carles",u"26/08/07",u"", 64 ), 
( 5, u"Per veure el contingut d'un arxiu#de text, quina comanda NO serveix?", u"cat",u"less",u"type", 3, u"carles",u"26/08/07",u"Això no és dos company", 65 ), 
( 5, u"Per què serveix la comanda CD?", u"Per canviar de directori",u"Per copiar un directori",u"Per res en majúscules", 3, u"carles",u"26/08/07",u"", 66 ), 
( 5, u"Per què serveix la comanda md?", u"Per crear un directori",u"Per moure un arxiu",u"Per res", 3, u"carles",u"26/08/07",u"Evidenment. Per fer un directori farem mkdir. Això no és dos!", 67 ), 
( 5, u"Per veure tots els arxius que#comencin per s o t farem:", u"ls [st]*",u"ls st?",u"ls st[*]", 1, u"carles",u"26/08/07",u"", 68 ), 
( 5, u"cp serveix per a:", u"copiar arxius",u"coupé: pujar la prioritat#d'un procés",u"copy paste: duplcar el contingut#del portapapers", 1, u"carles",u"26/08/07",u"", 69 ), 
( 6, u"Quin d'aquests programes#que permeten accés remot#no està als repositoris d'ubuntu.", u"Les mateixes X",u"vnc",u"nx", 3, u"carles",u"26/08/07",u"", 70 ), 
( 5, u"Què passa quan copiem#cosa.txt i Cosa.TXT#en un disc en fat32", u"Que es copien",u"Que esborrem el primer",u"Que es sumen", 2, u"carles",u"26/08/07",u"", 71 ), 
( 6, u"Quan l'equip de traductors del#KDE ens parlen de la mida#de la caixa. Es refereixen a:", u"Majúscules / minúscules",u"Marges de les finestres",u"Tipus de monitor", 1, u"carles",u"26/08/07",u"Això que ens pot sonar estrany no és un error de traducció. Ve de la mida e les caselles (caixes) que s'usaven en les impremtes. On les majúscules eren més grans. ", 72 ), 
( 4, u"Quants jocs de cartes de solitari hi ha#als repositoris d'ubuntu?", u"3",u"12",u"Més de 100", 3, u"carles",u"26/08/07",u"", 73 ), 
( 4, u"Quin d'aquests ordinadors NO#duia el procesador Zilog Z80-A", u"ZX Spectrum",u"Commodore",u"MSX", 2, u"carles",u"26/08/07",u"Duia un MOS 6510", 74 ), 
( 2, u"En quina d'aquestes distribucions#està basat l'ubuntu?", u"Debian",u"Fedora",u"Suse", 1, u"carles",u"26/08/07",u"", 75 ), 
( 5, u"Quants processadors suporta#Debian directament al seu web#d'enllaços de descàrregues?", u"10",u"5",u"3", 1, u"carles",u"26/08/07",u"Tot i que al ser totalment obert és il·limitat en aquest sentit.", 76 ), 


#fi_importació
			)
