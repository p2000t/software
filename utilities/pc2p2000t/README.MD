## PC2P2000T - loading `.cas` programs from PC to P2000T

Dit is een utility gemaakt voor de P2000T waarmee je via de seriële poort `.cas` programma's en games vanaf een PC naar de P2000T kunt laden. Na het inladen van een game op je P2000T kun je deze spelen (`RUN`), maar ook wegschrijven naar mini-cassette (`CSAVE`). \
Er bestond al een utility (SERIAL.BAS van Marcel de Kogel) waarmee je een complete mini-cassette vanaf de P2000T naar een PC kan wegschrijven via de seriële poort, maar PC2P2000T werkt dus precies de andere kant op.

Ik heb de overdrachtssnelheid van deze utility kunnen 'opvoeren' tot 9600 baud, waarmee het zelfs sneller is dan laden van een cassette (dat op de P2000T met ongeveer 6000 baud gaat).

De utility werkt voor P2000T machines met 16K, 32K of 48K aan RAM geheugen. Ik heb zelf een geheugen-uitbreiding tot 32K, dus ik heb niet kunnen testen of het werkt op een 48K machine.

Om dit programma te gebruiken heb je de volgende hardware nodig:
* Een P2000T;
* Een PC met daarop de `.cas` bestanden die je wilt laden naar je P2000T;
* Een kabel en adapter waarmee je de 25-pins seriële poort van de P2000T aan de USB-ingang van je PC kunt koppelen. \
  Als je zo'n kabel zoekt: online kun je het vinden door te zoeken op "USB naar 25-pin RS-232 adapter". De kabel en adapter kosten bij elkaar ongeveer 12 euro. Ik heb ze hier gekocht:
  * De USB naar 25-pin RS-232 adapter: https://www.onlinekabelshop.nl/usb-a-m-naar-9-pins-sub-d-25-pins-sub-d-m-seriele.html
  * De Windows driver voor deze adapter: https://files-onlinekabelshop.nl/Handleidingen/Drivers%20OKS-45902.zip
  ![USB to RS232 cable](/utilities/pc2p2000t/usb2rs232.png)

Als je alle hardware beschikbaar hebt, tik dan deze 32 regels BASIC code op je P2000T:
```
10 REM P2000 programma laden via RS232
20 REM Versie 0.3 door Dion Olsthoorn
30 CLEAR 50,&H9DFF+256*32*(PEEK(&H605C)+(PEEK(&H605C)=1))
40 M=PEEK(&H605C) : Z = 32*(M+(M=1))
50 BASE = &H9E00 + 256*Z
60 T=0 : I=0 : PRINT CHR$(12)
70 READ P$ : IF P$="stop" THEN GOTO 110
80 P=VAL("&H"+P$) : POKE BASE+I,P
90 IF P=&H9E OR P=&H9F THEN POKE BASE+I,P+Z
100 I=I+1 : T=T+P : GOTO 70
110 IF T=11963 THEN GOTO 130
120 PRINT "Typefout gemaakt in DATA" : END
130 DEF USR1=BASE + &H1D
131 DEF USR2=BASE + &H6C
140 PRINT "Start ontvanger op P2000T met ?USR1(0)"
141 PRINT "of ?USR2(0) voor ontvang-bewaar modus"
150 PRINT "Dan op PC .cas bestand zenden naar COM"
160 PRINT "9600 baud, geen parity en 8 data bits"
200 DATA C5,DB,20,E6,01,20,FA,06,15,10
210 DATA FE,06,08,DB,20,1F,CB,19,C5,06
220 DATA 10,10,FE,C1,10,F3,79,C1,C9,F3
230 DATA 06,00,21,00,9F,CD,00,9E,77,23
240 DATA 10,F9,21,4F,9F,4E,2A,30,9F,18
250 DATA 07,06,00,CD,00,9E,10,FB,11,00
260 DATA 04,CD,00,9E,77,23,1B,7A,B3,20
270 DATA F6,0D,20,E9,11,47,65,2A,34,9F
280 DATA 19,22,05,64,22,07,64,22,09,64
290 DATA 3A,B9,63,C6,02,32,B9,63,32,59
300 DATA 62,3E,07,CD,4A,10,FB,C9,CD,1D
310 DATA 9E,21,30,9F,11,30,60,01,20,00
320 DATA ED,B0,3E,05,CD,18,00,C3,6C,9E
330 DATA stop
```
Bewaar dit vervolgens op een P2000T cassette (noem het bijvoorbeeld `pc2p2000.bas`), zodat je het de volgende keer weer kunt gebruiken.

Daarna de PC koppelen aan de seriële poort van de P2000T (via het RS232-to-USB adapter kabeltje).
Op Windows kun je bij de Device Manager kijken op welke COM-poort de USB adapter is gemapt. In mijn geval is dat COM5. In de voorbeelden hieronder moet je dus jouw eigen COM-poort nummer gebruiken i.p.v. `com5`.

Dan op de PC een command prompt openen om voor deze COM poort de juiste baudrate etc. instellen (9600 baud, geen parity en 8 data bits):
```
mode com5 baud=9600 parity=n data=8 stop=1
```
Dan op de P2000T de pc2p2000 utility laden en "installeren" door RUN te doen. Daarna het volgende commando geven om de P2000T te laten luisteren naar de seriële poort:
```
?usr1(0)
```
En vervolgens op de PC een `.cas` bestand sturen naar de juiste COM poort (als voorbeeld hieronder het bestand `BrickWall.cas`)
```
copy BrickWall.cas \\.\com5
```
Daarna wachten op de pieptoon, waarna de cursor weer te zien is op zowel de P2000T als je PC. Dit betekent dat het programma succesvol is ingeladen.\
Hierna kun je het ingeladen spel bewaren op cassette met `CSAVE` of direct kunt spelen met `RUN`.

### Ontvang-bewaar modus

`pc2p2000` heeft ook een **ontvang-bewaar modus**, te activeren d.m.v. `?USR2(0)` i.p.v. `?USR1(0)`. Hierbij kun je vanaf de PC iedere keer een los .cas programma naar de P2000T sturen, die dan direct na ontvangst op cassette wordt bewaard, waarna de P2000T dan weer gaat wachten op het volgende .cas bestand. Hiermee kun je dus een hele reeks .cas bestanden in één keer naar cassette wegschrijven. \
Zorg er hierbij wel voor dat:
* De cassette waarnaar je wilt schrijven leeg is
* De eerste letter van iedere bestandsnaam (te vinden in de .cas header) uniek is
* De PC na het verzenden van ieder .cas bestand een tijdje wacht (afhankelijk van de grootte van het bestand) voordat het volgende .cas bestand weer wordt verzonden. Op die manier krijgt de P2000T genoeg tijd om het ontvangen bestand op cassette te bewaren voordat het klaar is voor het volgende bestand.

### Op zoek naar .cas bestanden?

Op github zijn trouwens veel `.cas` game bestanden te vinden: https://github.com/p2000t/software/tree/master/tapes/games \
Voor grote spellen (zoals `Fraxxon.cas`) heeft je P2000T mimaal een 16K RAM geheugenuitbreiding nodig. Als je zo'n geheugenuitbreiding zoekt, kijk dan eens op marktplaats. Gebruiker [ifilot](https://www.marktplaats.nl/u/ifilot/15277239/) maakt ze zelf nog gewoon nieuw!

### Tips:
* Om te testen of de kabel werkt, kun je in een Windows command box de baudrate van de COM-poort op 1200 zetten en dan TYPE COM5 doen (gebruik ipv '5' jouw eigen COM nummer), waarna je op de P2000T `<shift><00>` (de printer-key) indrukt. Dit stuurt alles op het scherm van je P2000T naar je PC, dus als het goed is zie je dat.
* Ook heb ik gemerkt dat de 'mode' instellingen die je op de PC doet weer worden gereset naar de standaard waarden als je de USB stekker los- en daarna weer vastmaakt.
