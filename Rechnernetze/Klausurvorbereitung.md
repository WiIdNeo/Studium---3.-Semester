# Allgemein

## Was sind Rechnernetze

Ein Rechnernetz ist ein Zusammenschluss mehrer Computer und anderer Digitaler Geräte, um Daten auszutauschen und Ressourcen gemeinsam zu nutzen.

Die Hauptziele eines Rechnernetzes:

- Kommunikation zwischen Geräten
- Austausch von Daten und Information
- gemeinsame Nutzung von Ressourcen
- Effizienzsteigerung durch optimierte Prozesse und Zusammenarbeit

## Bestandteile eines Rechnernetzes

Die Bestandteile eines Rechnernetzes lassen sich in drei grundlegende Kategorien unterteilen: **Hardware**, **Software** und **Protokolle**.

### Hardware

- Netzwerkendgeräte (Hosts, Clients, Knoten)
- Infrastrukturkomponenten
  - OSI-Layer 1: Hubs
  - OSI-Layer 2: Switches, Access Points, Modems
  - OSI-Layer 3: Router
  - OSI-Layer 4: Gateways und Firewalls
- Übertragungsmedien (physische Verbindungen: Kabel und Kabellose Varianten)
  - Twisted-Pair-Kabel
  - Glasfaserkabel
- Softwarekomponenten (Steuerung und Verwaltung der Hardware)
  - Betriebssysteme (Client und Server)
  - Netzwerkdienste und -anwendungen
    - Dateiserver
    - Webserver
    - E-Mail-Server
    - DNS- und DHCP-Server
    - VoIP-Software
- Protokolle


# OSI-Layer

|Layer|Name|Protokolle|Geräte|
|-|-|-|-|
|1|Bitübertragungsschicht|USB, DSL, ISDN|Kabel, Hubs|
|2||ARP, Ethernet, LLDP|Switches, Access Point, Modem|
|3||IP, RIP, OSPF, ICMP|Router
|4||TCP, UDP, TFTP|Gateway, Firewalls

## Netzwerkbereiche

### Geographischer Bereich (S. 7)

Beschreibt die Räumliche Audbreitung

- Personal Area Network (PAN): bis 10m, verbindet Geräte ohne Rounter oder Internetzugang. 1 - 10 Geräte
- Storage Area Network (SAN): Spezialisiertes Netzwerk, das Speichergeräte wie Festplatten oder Tape-Liberies mit Servern verbindet. Typische Technologien sind Fibre Channel (FC) oder Internet Small Computer System interface (iSCSI). 10 - 100 Systeme
- Local Area Network (LAN): kleiner geographischer Bereich, wie ein Gebäude oder ein Campus. 10 - 1000 Geräte
- Metropolitan Area Network (MAN): ein großflächiges Netzwerk, das sich über Länder oder Kontinente spannt. Tausende bis MIllionen von Geräten
- Global Area Network (GAN): ein Weltumspannendes Netz, dass mehrere WANs verbindet. Millionen von Geräte

### Topologie (S. 8)

Die physische oder Logische Struktur

#### Punkt-zu-Punkt

Zwei Systeme sind direkt verbunden, kein Routing nötig, kaum Skalierung.

#### Stern

Verbindet alle Systeme direkt mit einer zentralen aktiven Komponenten. Gute Erweiterbarkeit und einfaches Routing. Bei ausfall der mittleren Komponente ist das System down.

#### Ring

Alle Systeme sind RIngförmig miteinander verbunden. Sie können das Signal alle verstärken, doch wenn ein System ausfällt bricht die Verbindung ab. Außerdem kann immer nur ein Teilnehmer gleichzeitig senden.

#### Bus

Alle Systeme werden über einen zentralen Bus verbunden. Wenn dieser kaputgeht, bricht die 

### Technologie

Eingesetzte Medien oder Protokolle

### Administrative Verantwortung

- Zentrale Verantwortung
- Verteilte Verwaltung


