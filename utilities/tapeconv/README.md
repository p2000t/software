## P2000T Tape Converter

To convert P2000T tapes to program files on your PC, do the following:
* Run [`SERIAL.BAS`](/utilities/tapeconv/SERIAL.BAS) on your P2000. This will send all bytes of one side of the currently inserted tape through the P2000's serial port, at a baudrate of 2400Bd with 1 startbit and 1 stopbit
* Then run splitape.exe to split the full tape file into individual `.cas` programs

### Detailed instructions (in Dutch)

Dit is de hardware en software die ik heb gebruikt om P2000T programma's vanaf mini-cassettes om te zetten naar bestanden onder Windows:

* Een USB naar 9-pin RS-232 adapter. Te vinden op bijv. https://www.onlinekabelshop.nl/usb-naar-9-pins-serieel-rs-232-adapter-0-80-meter \
De driver voor deze adapter kun je hier vinden: https://files-onlinekabelshop.nl/Handleidingen/OKS-27684_Drivers.zip
 
* Een adapter van 25 pin (m) naar 9 pin (v) RS-232:  https://www.onlinekabelshop.nl/adapter-db25-m-db9-v \
Trouwens: kabel en adapter kun je ook veel goedkoper op AliExpress bestellen, maar dan moet je wel rekenen op langere wachttijd.
 
* M.b.v. de kabel en adapter maak je dan een verbinding tussen de P2000T (seriele poort) en je laptop (USB poort).
 
* Tik dan (eenmalig) het programma [`SERIAL.BAS`](/utilities/tapeconv/SERIAL.BAS) over op de P2000T en bewaar deze op een cassette. \
Als je dit programma al eerder had ingetikt, dan kun je het gewoon laden uiteraard.
 
* Na het intikken/inladen van `SERIAL.BAS` (let op: run deze nog niet!), doe je de cassette in de P2000T die je wil gaan archiveren. Het archiveren gaat per kant van de cassette, dus je moet zowel de voor- als achterkant doen.
 
* Op Windows (ik gebruik Windows 10) kun je bij Device Manager zien op welke COM-poort de USB-adapter is gemapt. Dat was in mijn geval COM4. Als het COM-nummer bij jou anders is, vervang in de instructies hieronder `COM4` voor het andere COM poort nummer.
 
* Daarna op je PC een Command Prompt openen en de baudrate (2400), stopbits (1), databits (8) en parity (geen) zetten voor de betreffende COM poort:
  ``` 
  mode COM4 BAUD=2400 PARITY=n DATA=8
  ```
 
* Daarna op je PC het volgende commando uitvoeren om inkomende data van de COM-poort te bewaren in een tape image file
  ```
  type com4: >> mijntape.cas
  ```

* Daarna op de P2000T het commando `RUN` geven, waardoor het programma SERIAL.BAS uitgevoerd wordt, die de gehele inhoud van één kant van de cassette via RS-232 naar je PC verstuurt.
 
* Na verloop van tijd is het programma SERIAL.BAS klaar (duurt maximaal 4-5 minuten per kant van een cassette), waarna je Ctrl-C doet in de Windows Command Prompt, zodat het archief bestand wordt gesloten.

* [Optioneel] Gebruik het programma `splittape.exe` om de tape image file (bijv. `Basic Demo blauw A.cas`) op te splitsen in losse `.cas` programma's: \
![Example usage of splitape.exe](/utilities/tapeconv/splitape_example.png)
