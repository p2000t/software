## P2000T programma's laden vanaf PC via een seriële verbinding

[pc2p2000t](pc2p2000t.bas) is een utility gemaakt voor de P2000T waarmee je via de seriële poort .cas programma's direct vanaf een PC kunt inladen. Na het laden van een programma naar de P2000T kun je deze dan starten d.m.v. `RUN`, maar ook wegschrijven naar mini-cassette d.m.v. `CSAVE`.

Er bestaat trouwens ook een utility die precies de andere kant op werkt, dus waarmee je een complete mini-cassette in binair formaat vanaf de P2000T naar een .cas bestand op je PC kan "dumpen" via de seriële poort. Dit is de [Cassette Dumper](../cassette-dumper) (voorheen: SERIAL.BAS) van Marcel de Kogel.

De pc2p2000t utility werkt voor alle P2000T modellen, dus met 16K, 32K of >48K aan RAM geheugen. De overdrachtssnelheid van de utility is 9600 baud (9600 bits per seconde), waarmee het zelfs sneller is dan het laden van een cassette op een originele P2000T, dat met ongeveer 6000 baud gaat.

Om deze utility te gebruiken heb je de volgende software en hardware nodig:
* Een P2000T;
* Een PC met waarop [Python](https://www.python.org/downloads/) staat geinstalleerd, met  ook de .cas bestanden die je wilt laden naar je P2000T;
* Een crossover kabel/adapter waarmee je de 25-pins seriële poort van de P2000T aan je PC kunt koppelen. \
Omdat de meeste PC's tegenwoordig geen seriële poort meer hebben, kun je in dat geval een USB-naar-serieel adapter kabel gebruiken. Adapters met FTDI-chip hebben op Windows geen extra drivers nodig, maar zijn wel duurder dan adapters met bijv. een CH340-kloon chip.  \
  Online kun je zo'n kabel vinden door te zoeken op "USB to serial RS-232 adapter". Hieronder een paar voorbeelden van hoe zo'n kabel/adapter eruit kan zien:\
  ![RS-232 USB to DB9 adapter](img/USB2DB9.png) ![RS-232 USB to DB25 adapter](img/USB2DB25.jpg)

Als je alle hardware beschikbaar hebt, tik dan deze 29 regels BASIC code op je P2000T:
```
10 REM pc2p2000t v0.4
20 CLEAR 50,&H9DFF+256*32*(PEEK(&H605C)+(PEEK(&H605C)=1))
30 M=PEEK(&H605C) : Z = 32*(M+(M=1))
40 BASE = &H9E00 + 256*Z
50 T=0 : I=0 : PRINT CHR$(12)
60 READ P$ : IF P$="stop" THEN GOTO 100
70 P=VAL("&H"+P$) : POKE BASE+I,P
80 IF P=&H9E OR P=&H9F THEN POKE BASE+I,P+Z
90 I=I+1 : T=T+P : GOTO 60
100 IF T=10839 THEN GOTO 120
110 PRINT "Typfout in DATA" : END
120 DEF USR1=BASE + &H1D
130 DEF USR2=BASE + &H61
140 PRINT "Start ontvanger op P2000T met ?USR1(0)"
150 PRINT "of ?USR2(0) voor ontvang-bewaar modus"
160 PRINT "Dan op PC .cas bestand zenden naar COM"
170 PRINT "9600 baud, geen parity en 8 data bits"
200 DATA C5,DB,20,E6,01,20,FA,06,15,10
210 DATA FE,06,08,DB,20,1F,CB,19,C5,06
220 DATA 10,10,FE,C1,10,F3,79,C1,C9,F3
230 DATA 06,00,21,00,9F,CD,00,9E,77,23
240 DATA 10,F9,21,4F,9F,4E,2A,30,9F,18
250 DATA 07,06,00,CD,00,9E,10,FB,11,00
260 DATA 04,CD,00,9E,77,23,1B,7A,B3,20
270 DATA F6,0D,20,E9,11,47,65,2A,34,9F
280 DATA 19,22,05,64,22,07,64,22,09,64
290 DATA 3E,07,CD,4A,10,FB,C9,CD,1D,9E
300 DATA 21,30,9F,11,30,60,01,20,00,ED
310 DATA B0,3E,05,CD,18,00,C3,61,9E,stop
```
Bewaar dit vervolgens op een P2000T cassette, zodat je het de volgende keer weer kunt gebruiken. Noem het bijvoorbeeld `pc2p2000t.bas`.

Daarna de PC koppelen aan de seriële poort van de P2000T (via het RS232-to-USB adapter kabeltje).
Op Windows kun je bij de Device Manager kijken op welke COM-poort de USB adapter is gemapt. In mijn geval is dat COM5. In de voorbeelden hieronder moet je dus jouw eigen COM-poort nummer gebruiken i.p.v. `COM5`.

### Losse .cas programma's zenden naar je P2000T

Laad op je P2000T de `pc2p2000t.bas` utility en "installeer" het door `RUN` te doen. Geef daarna het volgende commando op de P2000T om pc2p2000t te starten en te laten luisteren naar de seriële poort:
```
?USR1(0)
```
Nu kun je vanaf je PC een .cas bestand sturen via de juiste COM poort m.b.v. het [pc_to_p2000t.py](pc_to_p2000t.py) script. Als voorbeeld hieronder hoe je het bestand BrickWall.cas verstuurt via COM5:
```
python pc_to_p2000t.py COM5 ..\..\cassettes\games\Fraxxon.cas
```
Als alle bytes ontvangen zijn, dan hoor je een pieptoon op je P2000T, waarna de cursor weer te zien is. Dit betekent dat het programma succesvol is ingeladen.
Hierna kun je het ingeladen spel bewaren op cassette met `CSAVE` of direct spelen met `RUN`.

### Ontvang-bewaar modus

De meest recente versie van de pc2p2000t utility heeft nu ook een **ontvang-bewaar modus**, die te activeren is d.m.v. `?USR2(0)` i.p.v. `?USR1(0)`. Hierbij kun je vanaf de PC iedere keer een los .cas bestand naar de P2000T sturen, die dan direct na ontvangst op cassette wordt bewaard, waarna de P2000T dan weer gaat wachten op het volgende .cas bestand. Zo kun je dus een hele reeks .cas bestanden achter elkaar naar cassette wegschrijven.

Vanaf je PC gebruik je hiervoor dezelde [pc_to_p2000t.py](pc_to_p2000t.py) Python utility, waarmee je meerdere .cas programma's kunt versturen. Hiermee kun je ook niet-gesplitste cassette dump bestanden zoals [Basic Demo cassette (kant A).cas](<../../cassettes/demos/Basic Demo cassette (kant A).cas>) of [ErrorSoft.cas](../../cassettes/games/ErrorSoft.cas) in één keer correct overzetten. 
Als voorbeeld:
```
python pc_to_p2000t.py COM4 ..\..\cassettes\games\Fraxxon.cas ..\..\cassettes\games\Brick-Wall.cas
```

Zorg bij het gebruik van de ontvang-bewaar modus wel voor dat:
* De cassette waarnaar je wilt schrijven leeg is;
* Alle programma's bij elkaar maximaal 42 blokken zijn, want meer past er niet op een originele P2000T cassette.
* De eerste letter van iedere bestandsnaam (zoals te vinden in de .cas header) uniek is; dit geldt trouwens niet voor "stand-alone" machinetaalprogramma's.

### Op zoek naar .cas games?

Op github zijn veel .cas games te vinden: https://github.com/p2000t/software/tree/master/tapes/games \
Voor grote spellen zoals [Fraxxon.cas](../../cassettes/games/Fraxxon.cas) heeft je P2000T mimaal een 16K RAM geheugenuitbreiding nodig. Als je zo'n geheugenuitbreiding zoekt, kijk dan eens op marktplaats bij gebruiker [ifilot](https://www.marktplaats.nl/u/ifilot/15277239/) die ze zelf maakt!

### Tips:
* Om te testen of de kabel werkt, kun je in een Windows command prompt de baudrate van de COM-poort op 1200 zetten d.m.v.   
  ```
  mode com5 baud=1200 parity=n data=8 stop=1
  ```
  en daarna het `TYPE COM5` commando geven (gebruik ipv '5' jouw eigen COM nummer), waarna je op de P2000T `<shift><00>` (de printer-key) indrukt. Dit stuurt alle tekst op het scherm van je P2000T naar je PC, dus als het goed is zie je die tekst verschijnen in de command prompt.
* De `MODE` instellingen die je in Windows doet, worden weer gereset naar de standaard waarden als je de USB stekker los- en daarna weer vastmaakt.
