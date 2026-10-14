---
title: IPv6
author: Jasper Bauerschaper, Felix Luderer, Niclas Böhme
---

Übersicht
-

# Übersicht über IPv6

- Internet Protocol Version 6
- Entwicklung wurde 1994 beschlossen (von IETF)
- Kernspezifikation 1998 festgelegt
- 2017 mit STD 86 als Internetstandard definiert in RFC 8200
- Zugriff via IPv6 laut Google Statistiken:
  global ~50%, Deutschland ~75%
- als AAAA Einträge in DNS geführt

# Geschichte

- verschiedene Protokolle Anfang der 1990er Jahre
- entstand aus dem IETF-Prozess zur Findung eines neuen, besseren Protokolls
  (IPng)
- SIPP setze sich gegen Konkurrenten (TP/IX, PIP, TUBA, CLNP) durch
- Ziel war auch Features von proprietären Protokollen (DECNET, Novell Netware)
  zu übernehmen

<!-- end_slide -->

<!-- jump_to_middle -->

Motivation für IPv6
---

<!-- end_slide -->

Motivation für IPv6 (1)
-
# Grenzen von IPv4
<!-- pause -->
## Probleme der Zeit
- in 1992 noch klassifizierte Netze
- Anzahl freie Class B Netze (255.255.0.0) zeitnah erschöpft
  - Wenn mehr als 256 benötigt, müssen mehrere Class C Netze eingerichtet werden

<!-- pause -->

## Routing

- Routing Probleme aufgrund der hohen Anzahl der Netze
- große Menge an Routinginformationen überlasten Speicher der Router
- alte Routingprotokolle nehmen Bandbreite in Anspruch
- regelmäßig neue Hardware nötig
- Überwachung und Konfiguration der Netze aufwendiger ↪ Einführung von
  Klassenlosen Netzen (CIDR) 1993

<!-- end_slide -->

Motivation für IPv6 (2)
-

## IP-Adressen

- 32 Bit Adresslänge beschränkt Anzahl der IP-Adressen auf rund vier Milliarden
- Nutzung von NAT zur Wiederverwendung von IP-Adressen
- Einschränkung der Ende-zu-Ende-Verbindungen durch NAT bei Peer-to-Peer
- NAT verhindert, dass Geräte direkt im Internet sind
- Self-Hosting durch Port-Forwarding nicht mehr ohne weiteres möglich

<!-- end_slide -->

Motivation für IPv6 (3)
-
# NAT

- In RFC 1631 als „kurzfristige Lösung“ eingeführt
- Trennung von öffentlichem und lokalem Netz
- mehrere Geräte hinter einer öffentlichen IPv4 Adresse (NPAT)
- Status der Verbindung muss von Router gespeichert werden
- Adressumsetzung

<!-- pause -->

## SNAT

→ Source NAT

- mehrere Geräte nutzen die gleiche öffentliche IP als Source IP
- in Heim- und Unternehmensnetzen in Verwendung
<!-- pause -->

## DNAT

→ Destination NAT

- Ziel IP-Adresse eines Pakets wird auf private IP einer Maschine geändert
- Anwendung in Port-Forwarding
- Port-Forwarding nicht nutzbar, wenn CGNAT seitens Provider genutzt wird

<!-- end_slide -->

<!-- jump_to_middle -->

Adressierung
---

<!-- end_slide -->

Adressierung (1)
--
# Grundlagen

- Definiert in RFC 4291 in 2006
- jedes Interface wird adressiert
- jedes Interface muss mindestens eine Link-Local Adresse besitzen

<!-- pause -->

**fe80:0000:0000:0000:0233:54ff:fe5b:869d**

- Hexadezimal

- Länge:
  128 Bit

- aufgeteilt in acht 16 Bitblöcke

- führende Nullen in jedem Block müssen nicht geschrieben werden

  - **fe80:0:0:0:233:54ff:fe5b:869d**

- Mehrere aufeinander folgende Nullblöcke durch ::
  ersetzt werden (nur einmal)

  - **fe80::233:54ff:fe5b:869d**

- URL in eckigen Klammern

  - **http://\[fe80::233:54ff:fe5b:869d\]:80**

<!-- end_slide -->

Adressierung (2)
--

## Aufbau

<!-- column_layout: [1, 3, 1] -->

<!-- column: 1 -->

| Präfix | Interface-ID |
| :-: | :-: |
| 64 Bit | 64 Bit |
| Netzwerk | Host |

<!-- reset_layout -->

## Präfix

- bestimmt die Route und das Subnetz
- in CIDR Notation geschrieben:
  IPv6-Adresse/Präfixlänge
- Präfixlänge entspricht der Anzahl der zusammenhängenden Bits von links

## Interface-ID

- letzten 64 Bit (best practice)
- individuell für jedes Netzwerkinterface

<!-- end_slide -->

Adressierung (3)
--

# Unicast-Adressen

- eindeutige Identifizierung einer Maschine

## Link-Local Unicast-Adresse

- lokales Layer 2 Netz
- wird von jedem Interface benötigt
- genutzt für Adresskonfiguration und Neighbor Discovery (NDP)
- Präfix:
  `fe80::/10`
- IPv4:
  `169.254.0.0/16`
  - Notfalllösung, wenn kein DHCP verfügbar

<!-- end_slide -->

Adressierung (4)
--

## Globale Unicast-Adresse

- weltweit gültig
- über das Internet geroutet
- Präfix:
  `2000::/3`
  - Standort Präfix
    - ersten 48 Bit
    - kennzeichnet den Adressraum
    - vom Internetprovider zugewiesen
  - Teilnetz-ID
    - 16 Bit
    - Unterteilung von Subnetzen
- entspricht öffentlichen Adressen IPv4

<!-- pause -->
## Unique-Local Adresse

- nur im LAN geroutet
- 40 Bit von IID werden (pseudo)zufällig generiert
- Präfix:
  `fd00::/8`
- Äquivalent zu privaten IPv4 Adressen (10.0.0.0/8, 172.16.0.0/12,
  192.168.0.0/16)

<!-- end_slide -->

Adressierung (5)
--

# Anycast-Adresse

- einer Unicast-Adresse werden mehreren Netzwerkinterfaces zugewiesen
- Lastverteilung und Bildung von Redundanz
- aus Unicast-Adressbereich entnommen und gleiches Präfix
- bei mehreren Routern mit gleicher Anycast-Adresse wird der nächste verwendet

<!-- pause -->

# Multicast-Adresse

- gleichzeitig mehrere Geräte ansprechen
- Paket erreicht alle Interfaces mit dieser Adresse
- ein Interface kann mehrere Multicast Adressen besitzen
- Broadcast von IPv4 entfällt, stattdessen Mulitcast-Gruppen
- besitzen Group Identifier anstatt Interface Identifier
- Präfix:
  `ff00::/8`

<!-- end_slide -->

Adressierung (6)
--

# Loopback-Adresse

- Äquivalent zu 127.0.0.1
- Notation:
  `::1/128`

<!-- pause -->

# Unspecified Address

- als Absenderadresse beim Adresskonfiguration genutzt
- zeigt an, dass Maschine noch keine gültige IPv6 Adresse hat
- Notation:
  `::/128`
- IPv4:
  `0.0.0.0/32`

<!-- end_slide -->

<!-- jump_to_middle -->
Header
---
<!-- end_slide -->

Header (1)
-

- Deutlich vereinfachter Header im Vergleich zu IPv4
- Viele IPv4 Felder wurden umbenannt, ausgelagert oder vollständig entfernt
<!-- pause -->
| Größe | Name | Bedeutung |
| :-: | :-: | :-: |
| 4 Bit | Version | Version des Internetprotokolls |
| 8 Bit | Class | Verkehrsklasse des Pakets |
| 20 Bit | Flow-Label | Markiert alle Pakete eines Kommunikationstyps |
| 16 Bit | Payload-Length | Größe des verbleibenden Pakets nach dem ersten Header |
| 8 Bit | Next | Gibt den Typ des nächsten Headers an |
| 8 Bit | Hop-Limit | Anzahl der verbleibenden Übertragungen |
| 128 Bit | Source Adress | IPv6-Adresse des Senders |
| 128 Bit | Destination Adress | IPv6-Adresse des Empfängers |

<!-- end_slide -->
Header (2)
-
# Erweiterungheader
| Next ID | Name |
| :-: | :-: |
|0| Hop-by-Hop-Options |
|60| Destination Options (für jeden Router)|
|43| Routing |
|44| Fragment |
|51| AH (Authentication Header) |
|50| ESP (Encrypted Security Payload) |
|60| Destination Options (für Endgerät)|
|59| No-Next-Header |

<!-- end_slide -->
<!-- jump_to_middle -->

Unterschiede zwischen IPv4 und IPv6
---
<!-- end_slide -->

Unterschiede zwischen IPv4 und IPv6
-

- Adressgröße von 128 Bit
  - keine Adressknappheit -> erlaubt Struktur für besseres Aggregieren von
    Routen
  - kein NAT
- Modulare Header sorgen für eine allgmein vereinfachte Struktur
- Erlaubt das Verpacken und Transportieren beliebiger anderer Protokolle
- Fragmentierung auf Client, statt auf Router

<!-- end_slide -->
<!-- jump_to_middle -->
Adressauflösung
---
<!-- end_slide -->
Adressauflösung (1)
-


# Neighbor Discovery Protocol (NDP)
## Generell
- Equivalent zu ARP aus IPv4
- in ICMPv6, statt extra Schicht implementiert
- macht starke Nutzung von Multicast
<!-- pause -->
## Funktionsweise
### On-Link Determination
- Wenn Link-Local-Adresse
- Wenn Prefix in Router Advertisement (mit L-Bit)

<!-- end_slide -->
Adressauflösung (2)
-
### NDP
<!-- incremental_lists: true -->
- Über LL-Adressen
- Host 1 sendet Neighbor Solicitation (NS, ICMPv6 135) wird auf ff02::1
- Alle Hosts müssen auf ff02::1 hören
- Host 2 antwortet mit Neighbor Advertisenment (NA, ICMPv6 136)
  - beinhaltet Ebene-2-Addresse
- Host 1 speichert Host 2s Ebene-2-Adresse wird im Neighbor-Cache
<!-- incremental_lists: false -->

# Externe Adressen
- An Router
  - kann mit Redirect (ICMPv6 137) antworten um auf besseren 1.
    Hop hinzuweisen

<!-- end_slide -->
<!-- jump_to_middle -->
Adresskonfiguration
---
<!-- end_slide -->


Adresskonfiguration (1)
-

# SLAAC
-> StateLess Address AutoConfiguration
## Interface Identifier (IID) Generieren
- früher noch aus MAC (EUI-48)/geplant EUI-64 generiert
- heute pseudo-zufällig generiert
## Link-Local-Addresse
- Präfix fe80::/64
- IID generieren
  - hier manchmal auch statisch
## DAD
- NS an generierte Adresse
- Falls NA dazu kommt, ist sie schon belegt
- neue IID muss generiert werden

<!-- end_slide -->
Adresskonfiguration (2)
-
## Globale Unicast-Adresse
- Host schickt Router Solicitation (RS, ICMPv6 133) an ff02::2
- Jeder Router antwortet mit Router Advertisement (RA, ICMPv6 134)
  - beinhaltet Prefix(e), welche der Router anbietet
- Host generiert sich IID und erstellt mit erhaltenem Prefix eine GUA

<!-- newlines: 7 -->

> [!note]
> RA beinhaltet auch Flags dazu, ob diese Prefixe komplett auf dem lokalen Link
    liegen
>  RAs werden auch generell periodisch gesendet
>

<!-- end_slide -->

Adresskonfiguration (3)
-
# DHCPv6
- DHCPv4 sehr ähnlich
- Router und Prefixe können nur mit RAs ermittelt werden
- OPTION_IA_PD erlaubt es Prefixe dynamisch zu verteilen


<!-- end_slide -->
<!-- jump_to_middle -->

DNSv6
---
<!-- end_slide -->

DNSv6
-
- generell gleiche Funktionsweise wie mit IPv4
- AAAA Typ und IP6.ARPA.
  Reverse-Lookup-Zone
- neue C Funktionen um IPv6 Adressen anzubieten
  - Priorität verschiedener Adresstypen kann angepasst werden

<!-- end_slide -->
<!-- jump_to_middle -->

Übergang von IPv4 auf IPv6
---

<!-- end_slide -->

Übergang von IPv4 auf IPv6 (1)
-
# Generell
- Der Umstieg auf IPv6 erfolgt nur langsam
- Dementsprechend werden Verfahren benötigt, um während dem Übergang dennoch
  zwischen den Protokollen zu kommunizieren
<!-- pause -->

# Option 1: Dual-Stack
- Parallelbetrieb von IPv4 und IPv6 auf einem Gerät
- Gerät wählt Internetprotokoll basierend auf der DNS-Namensauflösung
<!-- pause -->

# Option 2: Tunneling
- Einbettung eines Netzwerkprotokolls in ein Anderes
- Erlaubt Netzprotokollen die Nutzung von Infrastruktur anderer
  Netzwerkprotokolle
- Beispiele von Tunneln:
  6in4, 6to4, 4in6, 6rd, ISATAP, Teredo
<!-- end_slide -->
Übergang von IPv4 auf IPv6 (2)
-

# Option 3: Protokollübersetzung
- Notwendig für Geräte die keinen Dual-Stack betreiben können
- IPv4-Adressen werden in der Art umgeschrieben, dass IPv4-Pakete über
  IPv6-Infrastruktur transportiert werden können
- Standards:
  Stateless IP/ICMP Translator (SIIT), NAT64

<!-- end_slide -->

<!-- jump_to_middle -->
Security
---
<!-- end_slide -->
Security
-
# Protokolle
- SEcure Neighbor Discovery (SEND)
	- analog ARP-Spoofing
- Source Address Validation Improvement (SAVI)
- RA-GUARD
	- stellt sicher, dass nur echte Router RA's senden dürfen
- DHCPv6-Shield
	- stellt sicher, dass nur echt Router DHCPv6 anbieten können

# DoS Probleme
- NS von Router

<!-- end_slide -->
<!-- jump_to_middle -->

DEMO
----

<!-- end_slide -->



<!-- jump_to_middle -->

Ende
----

<!-- end_slide -->

Quellen (1)
--

- https://ipv6textbook.com/files/ipv6textbook.pdf (07.10.2026)
- RFC 1380 - IESG Deliberations on Routing and Addressing
- RFC 1631 - The IP Network Address Translator (NAT)
- RFC 4291 - IP Version 6 Addressing Architecture
- RFC 4861 - Neighbor Discovery for IP version 6 (IPv6)
- RFC 4862 - IPv6 Stateless Address Autoconfiguration
- RFC 8200/STD 86 - Internet Protocol, Version 6 (IPv6) Specification
- Harald Zisler - Computer-Netzwerke - 2022
- https://www.google.com/intl/en/ipv6/statistics.html#tab=per-country-ipv6-adoption
  (09.10.2026)
- https://www.google.com/intl/en/ipv6/statistics.html#tab=ipv6-adoption
  (09.10.2026)
- https://de.wikipedia.org/wiki/Netzwerkadress%C3%BCbersetzung
- https://de.wikipedia.org/wiki/IPv6 (09.10.2026)
- https://de.wikipedia.org/wiki/Netzklasse (11.10.2026)

- https://www.google.com/intl/en/ipv6/statistics.html#tab=per-country-ipv6-adoption
- https://www.facebook.com/ipv6/?tab=ipv6_country
- https://web.archive.org/web/20250324111641/https://www.akamai.com/internet-station/cyber-attacks/state-of-the-internet-report/ipv6-adoption-visualization
<!-- end_slide -->
Quellen (2)
--

- https://radar.cloudflare.com/adoption-and-usage
- https://stats.labs.apnic.net/ipv6/
- https://www.employees.org/~dwing/aaaa-stats/
- Dittler, Hans Peter:
  IPv6 - das neue Internet-Protokoll:
  Technik, Anwendung, Migration; 2.
  aktualisierte und erweiterte Auflage, Heidelberg:
  dpunkt-Verlag, 2002
- Netzwerke:
  IPv6 - Internet Protocol Version 6 :
  HERDT BuchPlus/ Joachim Kohlmorgen, Klaus Fichtner, Daniel Hemmling, Andre
  Liesenfeld, Heinz Erich Lutz, Ralf Pohlmann, Mathias Schulze
