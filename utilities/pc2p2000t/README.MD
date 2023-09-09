## PC2P2000T (PC to P2000T)

Dit is een klein programma/utility gemaakt voor de P2000T waarmee je via de seriële poort **.cas** programma's en games naar je P2000T kunt sturen vanaf een Windows PC. Na het inladen van een game kun je deze spelen, maar ook wegschrijven naar mini-cassette.
Er bestond al een utility (SERIAL.BAS van Marcel de Kogel) waarmee je een complete mini-cassette naar de PC kan wegschrijven via de seriële poort, maar PC2P2000T werkt dus precies de andere kant op.

Ik heb de overdrachtssnelheid van deze utility kunnen 'opvoeren' tot 9600 baud, waarmee het zelfs sneller is dan laden van een cassette (dat op de P2000T met ongeveer 6000 baud gaat).

De utility zou moeten werken voor P2000T machines met 16K, 32K of 48K aan RAM geheugen. Ik heb zelf een geheugen-uitbreiding tot 32K, dus ik heb niet kunnen testen of het werkt op een 48K machine.

Om dit programma te gebruiken heb je de volgende hardware nodig:
* Een P2000T
* Een PC met daarop de .cas bestanden die je wilt laden naar je P2000T
* Een kabel waarmee je de 25-pins seriële poort van de P2000T aan de USB-ingang van je PC kunt koppelen \
  Als je zo'n kabel zoekt: online kun je het vinden door te zoeken op "USB naar 9-pin RS-232 adapter" en "Seriële adapter 25p SUB-D (m) - 9p SUB-D (v) RS232". \ 
  De kabel en adapter kosten bij elkaar ongeveer 10 euro. \
  ![USB to RS232 cable](/utilities/pc2p2000t/usb2rs232.png)

Als alle hardware beschikbaar is, tik dan deze 27 regels BASIC code op je P2000T:
```
10 REM P2000T programma laden via RS232
20 REM Versie 0.2 door Dion Olsthoorn
30 CLEAR 50,&H9DFF+256*32*(PEEK(&H605C)+(PEEK(&H605C)=1))
40 M=PEEK(&H605C) : Z = 32*(M+(M=1))
50 BASE = &H9E00 + 256*Z
60 T=0 : I=0 : PRINT CHR$(12)
70 READ P$ : IF P$="stop" THEN GOTO 110
80 P=VAL("&H"+P$) : POKE BASE+I,P
90 IF P=&H9E OR P=&H9F THEN POKE BASE+I,P+Z
100 I=I+1 : T=T+P : GOTO 70
110 IF T=9923 THEN GOTO 130
120 PRINT "Typefout gemaakt in DATA" : END
130 DEF USR1=BASE + &H1D
140 PRINT "Start ontvanger op P2000T met ?USR1(0)"
150 PRINT "Dan op PC .cas bestand zenden naar COM"
160 PRINT "9600 baud, geen parity en 8 data bits"
200 DATA C5,DB,20,E6,01,20,FA,06,15,10
210 DATA FE,06,08,DB,20,1F,CB,19,C5,06
220 DATA 10,10,FE,C1,10,F3,79,C1,C9,F3
230 DATA 06,00,21,00,9F,CD,00,9E,77,23
240 DATA 10,F9,21,4F,9F,4E,21,47,65,18
250 DATA 07,06,00,CD,00,9E,10,FB,11,00
260 DATA 04,CD,00,9E,77,23,1B,7A,B3,20
270 DATA F6,0D,20,E9,11,47,65,2A,34,9F
280 DATA 19,22,05,64,22,07,64,22,09,64
290 DATA 3A,B9,63,C6,02,32,B9,63,32,59
300 DATA 62,3E,07,CD,4A,10,FB,C9,stop
```
Bewaar dit vervolgens op een P2000T cassette (noem het bijv. pc2p2000.bas), zodat je het de volgende keer weer kunt gebruiken.

Daarna de PC koppelen aan de seriële poort van de P2000T (via het RS232-to-USB adapter kabeltje).
Op Windows kun je bij de Device Manager kijken op welke COM-poort de USB adapter is gemapt. In mijn geval is dat COM5. In de voorbeelden hieronder moet je dus jouw eigen COM-poort nummer gebruiken.

Dan op de PC een command prompt openen om voor deze COM poort de juiste baudrate etc. instellen (9600 baud, geen parity en 8 data bits):
```
mode com5 baud=9600 parity=n data=8 stop=1
```
Dan op de P2000T de pc2p2000 utility laden en "installeren" door RUN te doen. Daarna het volgende commando geven om de P2000T te laten luisteren naar de seriële poort:
```
?usr1(0)
```
En vervolgens op de PC een .cas bestand sturen naar de juiste COM poort (bijv. het bestand BrickWall.cas)
```
copy BrickWall.cas \\.\com5
```
Daarna wachten op de pieptoon, waarna de cursor weer te zien is op zowel de P2000T als je PC. Dit betekent dat het programma succesvol is ingeladen.\
Hierna kun je het ingeladen spel bewaren op cassette met CSAVE of direct kunt spelen met RUN.

Op github zijn trouwens veel **.cas** bestanden te vinden: https://github.com/p2000t/software/tree/master/tapes/games \
Voor grote spellen (zoals 'Fraxxon.cas') heeft je P2000T mimaal 32K RAM nodig, en voor 'VluchtSimulator.cas' zelfs 48K RAM.

### Tips:
* Om te testen of de kabel werkt, kun je in een Windows command box de baudrate van de COM-poort op 1200 zetten en dan TYPE COM5 doen (gebruik ipv '5' jouw eigen COM nummer), waarna je op de P2000T <shift><00> (de printer-key) indrukt. Dit stuurt alles op het scherm van je P2000T naar je PC, dus als het goed is zie je dat.
* Ook heb ik gemerkt dat de 'mode' instellingen die je op de PC doet weer worden gereset naar de standaard waarden als je de USB stekker los- en daarna weer vastmaakt.
