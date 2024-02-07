## P2000T Cassette Dumper

To archive/dump P2000T tapes to files on your PC, do the following:
* Connect the P2000T to your PC using a serial cross cable or USB-to-serial adapter cable;
* Run [Cassette Dumper.bas](<Cassette Dumper.bas>) on your P2000T. This will read all data on (one side of) the inserted cassette and send them via the P2000T's serial port at a baudrate of 9600 with no parity, 8 data bits, 1 startbit and 1 stopbit. 
* On the PC you'll need to receive and store the bytes into a .cas dump file;
* [Optional] Run splitape.exe to split the full tape dump file into individual .cas program files.

### Detailed instructions (in Dutch)

Dit is de hardware en software die ik heb gebruikt om P2000T cassettes te archiveren/dumpen naar .cas bestanden onder Windows:

* Een USB naar 25-pin RS-232 adapter. \
Te vinden op bijv. https://www.onlinekabelshop.nl/usb-a-m-naar-9-pins-sub-d-25-pins-sub-d-m-seriele.html \
De drivers voor deze CH340-kloon adapter kun je hier vinden: https://files-onlinekabelshop.nl/Handleidingen/Drivers%20OKS-45902.zip \
Deze adapter/kabel kun je trouwens voor minder geld op AliExpress kopen, maar dan moet je wel rekenen op een langere wachttijd.
 
* M.b.v. de kabel/adapter maak je dan een verbinding tussen de P2000T (seriele poort) en je laptop (USB poort).
 
* Tik dan (eenmalig) het programma [Cassette Dumper.bas](<Cassette Dumper.bas>) over op je P2000T en bewaar deze m.b.v. `CSAVE "Cassette Dumper"` op een cassette voor de volgende keer. Als je dit programma al eerder had ingetikt, dan kun je het uiteraard gewoon inladen. \
En mocht je de utility [pc2p2000t.bas](../pc2p2000t/pc2p2000t.bas) hebben, dan kun je daarmee direct [Cassette Dumper.cas](<../../cassettes/utilities/Cassette Dumper.cas>) vanaf je PC inladen op je P2000T.
 
* Na het intikken/inladen van Cassette Dumper.bas run je deze d.m.v. `RUN` en doe je de cassette in de P2000T die je wilt gaan archiveren. Let op: druk nog niet op een toets! \
 Een cassette heeft twee zijden, dus je moet zowel de voor- als achterkant los archiveren.
 
* Op Windows (ik gebruik Windows 10) kun je bij Device Manager zien op welke COM-poort de USB-adapter is gemapt. Dat was in mijn geval COM4. Als het COM-nummer bij jou anders is, vervang in de instructies hieronder `COM4` voor het andere COM poort nummer.

* Zorg dat je een recente versie van Python hebt geinstalleerd. Python kun hier downloaden: https://www.python.org/downloads/

* Daarna op je PC een Command Prompt (of terminal window) openen en het Python script [serial_to_file.py](serial_to_file.py) starten, waarbij je de juiste COM poort en het doel bestand opgeeft, bijv:
  ```
  python serial_to_file.py COM4 bandje-1A.cas
  ```
  N.B. dit Python script heeft de library PySerial nodig, die je installeert met `pip install pyserial`.

* Dan op de P2000T een toets indrukken, waarmee het archiveren/dumpen gaat beginnen. De gehele inhoud van één kant van de cassette wordt via RS-232 naar je PC verstuurd.
 
* Na verloop van tijd (maximaal 3 minuten) is het archiveren klaar, waarna je Ctrl-C doet in de Command Prompt, zodat het .cas archief bestand wordt gesloten.

* [Optioneel] Gebruik het Windows programma `splittape.exe` om de programma's in het cassette dump bestand op te splitsen in losse .cas bestanden: \
![Example usage of splitape.exe](splitape_example.png)
