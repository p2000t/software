## P2000T Cassette Dumper

To archive/dump P2000T tapes to files on your PC, do the following:
* Connect the P2000T to your PC using a serial cross cable or USB-to-serial adapter cable;
* Run [Cassette Dumper.bas](<Cassette Dumper.bas>) on your P2000T. This will read all data on (one side of) the inserted cassette and send them via the P2000T's serial port at a baudrate of 9600 with no parity, 8 data bits, 1 startbit and 1 stopbit. 
* On the PC you'll need to receive and store the bytes into a .cas dump file;
* [Optional] Run splitape.exe to split the full tape dump file into individual .cas program files.

### Detailed instructions (in Dutch)

Dit is de hardware en software die ik heb gebruikt om P2000T cassettes te archiveren/dumpen naar .cas bestanden onder Windows:

* Een USB naar 25-pin RS-232 seriele adapter. \
Dit soort adapter kabels zijn relatief goedkoop (rond €15) en hebben meestal een CH340 of FTDI chipset. Voor de CH340 chipset moet in Windows een extra driver geinstalleerd worden; bij een FTDI chipset is dat meestal niet nodig.
 
* M.b.v. de kabel/adapter maak je dan een verbinding tussen de P2000T (seriele poort) en je laptop (USB poort).
 
* Tik dan (eenmalig) het programma [Cassette Dumper.bas](<Cassette Dumper.bas>) over op je P2000T en bewaar deze m.b.v. `CSAVE "Cassette Dumper"` op een cassette voor de volgende keer. Als je dit programma al eerder had ingetikt, dan kun je het uiteraard gewoon inladen. \
En mocht je de utility [pc2p2000t.bas](../pc2p2000t/pc2p2000t.bas) hebben, dan kun je daarmee direct [Cassette Dumper.cas](<../../cassettes/utilities/Cassette Dumper.cas>) vanaf je PC inladen op je P2000T.
 
* Na het intikken/inladen van Cassette Dumper.bas run je deze d.m.v. `RUN` en doe je de cassette in de P2000T die je wilt gaan archiveren. Let op: druk nog niet op een toets! \
 Een cassette heeft twee zijden, dus je moet zowel de voor- als achterkant los archiveren.
 
* Op Windows (ik gebruik Windows 10) kun je bij Device Manager zien op welke COM-poort de USB-adapter is gemapt. Dat was in mijn geval COM4. Als het COM-nummer bij jou anders is, vervang in de instructies hieronder `COM4` voor het andere COM poort nummer.

* [eenmalig] Zorg dat je een recente versie van Python hebt geinstalleerd. Python kun hier downloaden: https://www.python.org/downloads/

* [eenmalig] Open een Command Prompt (of Terminal) window en installeer de Python library PySerial (dit hoef je slechts eenmalig te doen):
  ```
  pip install pyserial
  ```

* [eenmalig] Download het Python script [serial_to_file.py](serial_to_file.py) naar je computer.

* Navigeer vanuit een Command Prompt window naar de map waarin je serial_to_file.py hebt gedownload. Indien je deze naar de standaard Downloads map hebt gedownload, dan doe je:
  ```
  cd C:\Users\%USERNAME%\Downloads
  ```

* Vervolgens start je in hetzelfde Command Prompt window het Python script [serial_to_file.py](serial_to_file.py), waarbij je de juiste COM poort en het doel bestand opgeeft, bijv:
  ```
  python serial_to_file.py COM4 bandje-1A.cas
  ```

* Dan op de P2000T een toets indrukken, waarmee het archiveren/dumpen gaat beginnen. De gehele inhoud van één kant van de cassette wordt via RS-232 naar je PC verstuurd.
 
* Na verloop van tijd (maximaal 3 minuten) is het archiveren klaar, waarna je Ctrl-C doet in de Command Prompt, zodat het .cas archief bestand wordt gesloten.

* [Optioneel] Gebruik het Windows programma `splittape.exe` om de programma's in het cassette dump bestand op te splitsen in losse .cas bestanden: \
![Example usage of splitape.exe](splitape_example.png)
