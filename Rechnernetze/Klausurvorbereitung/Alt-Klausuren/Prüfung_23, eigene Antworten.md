# 1

Ein Rechnernetz ist ein Zusammenschluss von Systemen zum Austausch von Daten.

# 2

```text
Schicht 7: Anwendungsschicht                            Applicationlayer
        |
        v
Schicht 6:
        |
        v
Schicht 5:
        |                                                       n
        v                                                       |
Schicht 7: Transportschicht                            Transportlayer
        |                                                       n
        v                                                       |
Schicht 7: Transferschicht                             Transferlayer
        |                                                       n
        v                                                       |
Schicht 7: Sicherungsschicht                           Controllayer
        |                                                       n
        v                                                       |
Schicht 1: Bitübertragungsschicht                      Bittransferlayer
        |                                                       |
        –––––––––––––––––––––––––––––––––––––––––––––––––––––––––

```

Das muss ich auf jeden Fall noch auswendig lernen

# 3

Jede Schicht fügt eigene Header/Trailer hinzu, die für die Darunterliegende Schicht zu den Nutzdaten gehören.
Diese Header/Trailer dienen der Interpretation, Kontrolle und Verarbeitung.

# 4

Das TCP/IP-Modell fässt die ersten beiden sowie die letzten drei Schichten des IOS/OSI-Modells zusammen.
Die Schichten 5 - 7 sind die Anwendungschicht und die ersten beiden die Physische bzw Übertragungsschicht

# 5

Layer 3: DNS, Routing, DHCP
Layer 2: Spanning-Tree, VLAN, MAC-Addressen, Disranzvektoralgorithmus, ICMP, Ethernet
Layer 1: Repeater, Hub, Manchester-Codierung

# 6

Die genauen NRZ-Algorithmen kann ich noch nicht ganz unterscheiden, ich gehe aber mal davon aus, dass Mark wechsel bei 1 war


_____
|    |_|
10000101

NRZ-M ist nicht selbsttaktend, wodurch der Takt anderweitig übermittelt werden muss.
In der Praxis wird das durch die Preamble gelöst, die eine lange folge von abwechselnd 1 und 0 hat, um den Takt anzugeben.

# 7

Mehrfachzugriffsprotokolle sind dazu da, dass es bei Übertragungsmedien, die von mehreren Systemen genutzt werden nicht zu Kollisionen kommt, bzw, bieten sie eine Bestimmung, wie das gehandhabt wird, wenn es dazu kommt.

- ALOHA bzw S-ALOHA
- ...

# 8

```crc
Generatorpolynom = 1011
Daten = 101010111101

101010111101000
1011    |
0001    |
   1101 |
   1011 |
   0110 |
    1100|
    1011
    0111
     1111
     1011
     0100
      1001
      1011
      0010
        1001
        1011
        0010
          1000
          1011
          0011
            110
CRC = 110

Übertragene Daten: 101010111101110
```

# 9

Subnetzmaske: 11111111.11111111.11111111.00000000
Broadcast-Addresse: 10.10.31.255

Wie geht das? Ich weiß nur, dass es 26er Netze werden.

# 10

10.
192.

privat, weil nicht aus dem Internet ROutbar

# 11

Uni: an einen
Broad: An alle
Multi: An eine GRuppe
Any: An einen zufälligen aus der Gruppe

# 12

ICMP ist wie DNS nur anders

# 13

Das eine ist für die Reihenfolge der Übertragenen Frames (Sequenz) und das andere für die Sequenzierung der ACKs

# 14

Nat dient zum erweitern des IPv4-Addressbereiches, indem es IP-Adressen nach Außen hin zur Netz-IP zusammenfasst

# 15

# 16

UDP prüft nicht auf Ankommen und besitzt keine Flowcontrolle

# 17

Es beschreibt wie zwei Armeen einen Angriff koordinieren wollen und man nie sicher sein kann, dass die Bestätigung angekommen ist, und man so in eine Schleife aus Bestätigungen kommt. Das ist auch bei verbindungsorientierten Verbindungen das Problem. In der Praxis wird der Three-Way-Handshake genutzt


