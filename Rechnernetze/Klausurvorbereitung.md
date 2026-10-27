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

Alle Systeme werden über einen zentralen Bus verbunden. Wenn dieser kaputgeht, bricht die Verbrindung ab. Dafür einfache Verkabelung.

#### Baum

hirachische Weiterwntwicklung des Sterns, einfache Erweiterbarkeit und übersichtliches Routing. Nur Hirachisch geringere Knoten und verbindungen sind nur von Ausfällen eines Knoten betroffen.
-
#### (Voll-)Vermascht

Jedes Gerät ist mit mehreren anderen Verbunden. So haben Ausfälle kaum auswirkungen, dafür ist es schwierig zu warten und kostet viel Kabel.

### Technologien

Eingesetzte Medien oder Protokolle

### Administrative Verantwortung

- Zentrale Verantwortung
- Verteilte Verwaltung

### Architekturen

#### Monolithische Anwendungssysteme

- Zentraler Großrechner, an den mehrere Terminals angesschlossen sind
- schlechte erweiterbarkeit und einbindung

#### Cloud-Computing

- Verteilt Anwendung und Ressourcen
- Servicemodelle
  - SaaS: Fertige Softwarelösung
  - IaaS: RAM/VRAM 
  - PaaS: Entwicklungsplattformen für eigene Anwendungen
  - Public Cloud
  - Private Cloud
  - Hybrid Cloud


# Herausforderungen

## Verzögerung

### Verarbeitungsverzögerung

- Zeit, die ein Router benötigt, um zu empfangen, zu analysieren und weiterzuleiten
- Eintreffrate: $\alpha$ (Pakete pro Sekunde)
- Übertragungsgeschwindigkeit des Mediums $R$
- Bits pro Paket: $L$ und mittlere Bitmenge pro Paket $L_\alpha$

|$L / R$ (Verkehrswert)|Verzögerung|
|-|-|
|>1|gering|
|>1 && ~1|stark|
|<1|endlos|

![alt text](Verkehrswert.png)

### Warteschlangenverzögerung

- wenn mehrere Pakete zeitgleich beim Router ankommen und in eine Warteschlange gestellt werden müssen.
- ein Router kann nur sequenziell weiterleiten

### Übertragungsverzögerung

- Zeit, die benötigt wird, ein Paket vollständig auf das Medium übertragen (Also das reine Senden?)
- $\text{Ausbreitungsgeschwindigkeit} = \frac{\text{Paketgröße}}{\text{Datenrate}}$

### Ausbreitungsverzögerung

- Die Zeit, die ein Signal vom Sender zu Empfänger braucht
- $\text{Ausbreitungsgeschwindigkeit} = \frac{Strecke}{Ausbreitungsgeschwindigkeit}$

## Durchsatz

- momentan: Geschwindigkeit, mit der der Host empfängt
- durchschnittlich: $R = \frac{\text{Datenmenge F}}{t}$
- maximale Durchsatzrate: $R = \min(\text{R_S Geschwindigkeit der Datenübertragung des Servers}, \text{R_C Geschwindigkeit der Datenübertragung des Clients})$
  - Wenn $R_S > R_C$, entstehen Engpässe

## Skalierbarkeit

Skalierbarkeit beschreibt die Fähigkeit selbst bei zunehmender Größe stabil und leistungsfähig zu bleiben.

### Horizontale Skalierung

- Erweiterung um physische Komponenten
- Erhöhung der Fehlertoleranz
- Ermöglichen von Rolling Updates

### vertikale Skalierung

- Bestehende Komponenten leistungsfähiger machen
- stößt schneller an physikalische oder wirtschaftliche Komponenten

## Verfügbarkeit

Beschreibt die Betriebsbereitschaft eines Netzwerks. 

### Redundanz

- multible Verkabelung

### Failover-Mechanismen

- Automatisches Umschalten auf Ersatzsysteme

### Fehlertolerante Protokolle

### Monitoring und Frühwarnsysteme

- Bestimmte Protokolle und Tests wie Pings sind oft Frühwarnungen

## Sicherheit und Datenschutz (CIA)

### Vertraulichkeit (Confidential)

Nur berechtigte Personen dürfen auf Informationen zugreifen.

### Integrität (Integrity)

Daten dürfen nicht unbemerkt manipuliert/beschädigt werden.

### Verfügbarkeit (Availability)

Systeme und Daten müssen zuverlässig nutzbar sein

### Wege dorthin

- Zugriffs- und Rechteverwaltung: Rollenbasierte Zugriffskonzepte
- Verschlüsselung der Daten: Technologien wie HTTPS oder TLS
- Firewall-, Intrusion Detection/Prevention Systeme (IDS/IPS): Kontrollieren des Datenverkehrs und erkennen von verdächtigen Mustern
- Physische Sicherheit der Netzwerk-Komponten.

# ISO/OSI-Modell

![alt text](ISOOSI.png)

![alt text](PDU.png)

## Ein- und Entkapselung

Jede Schicht fügt einen Header mit für die Schicht relevanten Metadaten hinzu. Bei der Entkapselung werden die Header von ihren Schichten wieder entfernt.

![alt text](Kapselung.png)

## Bitübertragungsschicht

- Physikalische Übertragung der Bitfolgen
- Wandelt die Bits basieren auf den Anforderungen der Übertragungsinfrastruktur um
  - Kupfer: Elektrisches Signal
  - Glasfaser: optisches Signal
  - drahtlos: Funk- oder Lichtwellen
- definiert Bitlaufzeiten und Aufbau, Erhalt und Rücksetzbarkeit der physikalischen Verbindung
- keine Fehlerprüfung, lediglich Übertragung

## Sicherungsschicht

- sorgt für die fehlerfreie Datenübertragung innerhalb von lokalen Netzwerken. 
- physikalische (MAC-)Adressen für die Identifikation
  
### Media Access Control (MAC)

Steuert den Zugriff auf das Übertragungsmedium und regelt, welches Gerät wann senden darf.

### Logical Link Control (LLC)

- Erkennt und behebt Übertragungsdehler
- verwaltet logische Verbindungen und Gruppiert Bits in Frames

## Vermittlungsschicht

- logische Addressierung und Routing zwischen Netzwerken
- IP-Adressen

### Routing

- **Statisches Routing**: Vordefinierte Routen, unabhängig der aktuellen Netzwerksituation
- **Dynamisches Routing**: Routen werden für jede Übertragung neu bestimmt - je anch Auslastung, Verzögerung und Verbindungsstatus

### MTU (Maximum Transmission Unit)

- Maximale Größe von IP-Paketen
- Wenn Überschritten, dann Fragmentiert

### Übertragung über Router

![alt text](Layer3Uebertragung.png)

## Transportschicht

