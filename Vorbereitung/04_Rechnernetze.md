# Rechnernetze

*Modulcode 4TI-RN-30, 5 ECTS, Klausur 120 Min. im 3. Theoriesemester, keine Zugangsvoraussetzung. Bildet die Basis für die späteren Wahlmodule "Kommunikationstechnik" und "Spezielle Netze und Netzwerk-Engineering".*

Da du hier bei null anfängst: Diese Datei enthält gezielt viele Grundlagen-Ressourcen, bevor es in die eigentlichen Vorlesungsinhalte geht. Am besten von unten (Grundlagen) nach oben (Vorlesungsinhalte) durcharbeiten.

## Offizielle Lerninhalte (lt. Modulbeschreibung)
- Grundkonzepte, Topologien, OSI/ISO-Basisreferenzmodell, Standardisierungsorganisationen
- Bitübertragungsschicht: Signaldarstellung/-codierung, Übertragungsmedien, Verkabelung
- Verbindungsschicht: Ethernet (IEEE 802), Rahmenaufbau, Switching, VLANs (IEEE 802.1q), Spanning Tree
- Netzwerkschicht: IPv4-Adressierung, statisches/dynamisches Routing (RIP, OSPF), Subnetting/Supernetting, NAT, Ausblick IPv6
- Transportschicht: UDP, TCP, Socket-Schnittstelle
- Anwendungsschicht: DNS, SMTP/POP3, einfaches Netzwerkmanagement mit SNMP

## Inhaltliche Schwerpunkte
- Schichtenmodelle: OSI-Modell (7 Schichten) und TCP/IP-Modell (4 Schichten) im Vergleich
- Physikalische Schicht & Sicherungsschicht: Übertragungsmedien, Ethernet, MAC-Adressen, Switches
- Vermittlungsschicht: IP-Adressierung (IPv4/IPv6), Subnetting, Routing
- Transportschicht: TCP vs. UDP, Ports, Verbindungsaufbau (3-Way-Handshake), Flusskontrolle
- Anwendungsschicht: DNS, HTTP, DHCP, ARP
- Fehlererkennung/-behandlung, Stau- und Überlastkontrolle

## Absolute Grundlagen zuerst (empfohlen bei "kein Plan")

| Ressource | Beschreibung | Link |
|---|---|---|
| TCP/IP MODELL einfach erklärt (deutsch) | Kurzes, verständliches Einstiegsvideo zum TCP/IP-Modell | https://www.youtube.com/watch?v=lDYgCAwY8V4 |
| Studyflix – TCP/IP (mit Video) | Guter schriftlicher Einstieg inkl. eingebettetem Erklärvideo, ordnet Begriffe wie Protokolle, Schichten, Adressen, Ports ein | https://studyflix.de/informatik/tcp-ip-5692 |
| NetworkChuck – FREE CCNA 200-301 Complete Course (Playlist, englisch) | Sehr unterhaltsam und anschaulich erklärter Praxiskurs zu Netzwerkgrundlagen (Switches, Router, TCP/IP, OSI, Subnetting); deckt deutlich mehr als nötig ab, aber die ersten Folgen sind ideal für absolute Einsteiger | https://www.youtube.com/playlist?list=PLIhvC56v63IJVXv0GJcl9vO5Z6znCVb1P |

## Vertiefende YouTube-Ressourcen
- NetworkChuck Kanal (weitere Einzelvideos, z. B. "What is a Switch?", "What is an IP Address?"): https://www.youtube.com/@NetworkChuck
- Grundlagen Rechnernetze und Verteilte Systeme (TUM, Kapitel 0 – Einführung & Schichtenmodelle, als Foliensatz, aber inhaltlich sehr strukturiert): https://www.net.in.tum.de

## Dokumentationen & Nachschlagewerke
- StudySmarter – Netzwerkstandardisierung: OSI-Modell & TCP/IP (kompakte Übersicht beider Modelle im Vergleich): https://www.studysmarter.de/schule/informatik/technische-informatik/netzwerkstandardisierung/
- Hagel-IT – TCP/IP, OSI, Subnetting & Ethernet einfach erklärt (gute Alltagssprache, hilfreich für den ersten Überblick): https://www.hagel-it.de/it-insights/netzwerk-technologie-tcp-ip-osi-subnetting-erklaert
- Cisco Networking Basics (offizielle, sehr saubere Einführung, englisch): https://www.cisco.com/c/en/us/solutions/small-business/resource-center/networking/networking-basics.html

## Basisliteratur laut Modulbeschreibung (prüfungsrelevant)
- TANENBAUM, A. S.; WETHERALL, D. J.: *Computernetzwerke*, Pearson Studium IT
- SCHERFF, J.: *Grundkurs Computernetze: Eine kompakte Einführung in die Rechnerkommunikation*, Vieweg
- Vertiefend: SCHREINER, R.: *Computernetzwerke. Von den Grundlagen zur Funktion und Anwendung*, Hanser

## Empfohlene Vorgehensweise (für absolute Einsteiger)
1. Erst ein Mal ein Erklärvideo zum TCP/IP-Modell ansehen, um ein grobes Bild zu bekommen ("was passiert, wenn ich eine Webseite aufrufe").
2. Danach OSI-Modell und TCP/IP-Modell gegenüberstellen und die 4–7 Schichten mit ihren Aufgaben auswendig lernen – das ist die Basis für fast alles Weitere.
3. IP-Adressierung und Subnetting selbst mit Beispielaufgaben üben (z. B. "Wie viele Hosts passen in ein /26-Netz?").
4. TCP vs. UDP im Detail verstehen (Verbindungsaufbau, wann welches Protokoll sinnvoll ist).
5. Erst danach Anwendungsprotokolle (DNS, HTTP, DHCP) und Routing vertiefen.

## Ergänzend: Netzwerk-Grundlagen als eigenes Thema
Da hier explizit Nachholbedarf besteht, lohnt sich ein kompletter, geführter Grundkurs mehr als einzelne Erklärvideos:
- NetworkChuck FREE CCNA 200-301 (Playlist, komplett kostenlos, sehr praxisnah mit echten Geräten): https://www.youtube.com/playlist?list=PLIhvC56v63IJVXv0GJcl9vO5Z6znCVb1P

**Tipp:** Wireshark installieren und den eigenen Internetverkehr (z. B. beim Öffnen einer Webseite) mitschneiden – das macht Schichtenmodell und Protokolle "greifbar" statt nur abstrakt.
