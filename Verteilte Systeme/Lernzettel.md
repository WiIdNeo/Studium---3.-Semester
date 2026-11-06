# Lernzettel: Verteilte Systeme (WS 2026)

> Grundlage: Vorlesungen 1–6 (Dr. M. Hofmann, DHSN Glauchau) und die 5. Übungsserie mit den klausurrelevanten Themen.
> Klausur: nur **Theoriefragen**, keine praktischen Aufgaben (Code, Rechnen am Rechner o. ä.). Die Formeln unten (NTP, Lamport) solltest du trotzdem können.

---

## 0. So benutzt du diesen Lernzettel

### Legende

| Marker | Bedeutung | Was du tun solltest |
|---|---|---|
| 🎯 | **Klausurrelevant.** Steht ausdrücklich in der Themenliste der 5. Übungsserie (Aufgabe 1 oder 2). | Auswendig/sicher können, so dass du es in eigenen Worten erklären kannst |
| 🟡 | **Grenzfall.** Nicht wörtlich gelistet, aber nötiger Hintergrund zu einem 🎯-Thema oder direkt daneben. | Verstehen, bei Zeit lernen |
| ⚪ | **Nicht gelistet.** Kam in der Vorlesung vor, steht aber nicht in der Klausurthemenliste. | Nur überfliegen. Ich habe es der Vollständigkeit halber kompakt aufbereitet |

### Die Klausurthemen laut 5. Übungsserie (Aufgabe 2)

| Kapitel | Klausurrelevant (🎯) |
|---|---|
| 1 Einführung | Begriffsdefinitionen, Ziele, Eigenschaften |
| 2 Architekturen | Architekturstile und ihre Eigenschaften; Schichtenarchitektur für interaktive Anwendungen |
| 3 Prozesse | Einsatz von Threads in verteilten Systemen; Server und Zustände |
| 4 Kommunikation | Arten von Kommunikation; Remote Procedure Call |
| 5 Synchronisation | Uhrensynchronisation; NTP |
| 6 Replikation | Einsatzgründe |
| 7 Fehlertoleranz | Begriffsdefinitionen; Ansätze zum Erreichen von Fehlertoleranz |

Dazu kommen die **Probeklausuraufgaben (Aufgabe 1, Architekturen)**:
a) zwei Architekturstile nennen und erklären, b) das zugrunde liegende Rollenmodell, c) vertikale vs. horizontale Verteilung mit Beispielen, d) Middleware. Musterlösungen findest du in **Abschnitt 8**.

### Prüfungsstrategie in einem Satz
Bei Theoriefragen punkten **saubere Definitionen + je ein Beispiel + Vor-/Nachteil**. Bei jedem Begriff: *Was ist es? Wozu gibt es das? Beispiel? Nachteil/Grenze?*

---

## Inhaltsverzeichnis

1. [Einführung](#1-einführung)
2. [Architekturen](#2-architekturen)
3. [Prozesse](#3-prozesse)
4. [Kommunikation](#4-kommunikation)
5. [Synchronisation](#5-synchronisation)
6. [Konsistenz und Replikation](#6-konsistenz-und-replikation)
7. [Fehlertoleranz](#7-fehlertoleranz)
8. [Probeklausur Aufgabe 1: Musterlösungen und weitere Übungsfragen](#8-probeklausur-aufgabe-1-musterlösungen-und-weitere-übungsfragen)
9. [Glossar und Formelsammlung](#9-glossar-und-formelsammlung)

---

# 1. Einführung

## 1.1 Was ist ein verteiltes System? 🎯 (Begriffsdefinition)

> **Definition:** Ein verteiltes System ist eine **Ansammlung unabhängiger Computer**, die für ihre Nutzer **wie ein einziges zusammenhängendes System erscheint**.

Zwei Teile musst du erkennen:
- **Hardware-Sicht:** Die Computer sind autonom (jeder läuft für sich). Es gibt keine Vorgaben zu Art der Computer oder ihrer Verbindung.
- **Software-Sicht:** Nutzer sehen *ein* System. Die Zusammenarbeit der autonomen Komponenten ist genau die Herausforderung beim Entwickeln.

**Wichtige Eigenschaften** 🎯
- Unterschiede zwischen den Computern, ihre Kommunikation und die interne Organisation sind **vor dem Nutzer verborgen**.
- **Einheitliche Nutzung** unabhängig von Ort und Zeit.
- Gute **Erweiterbarkeit und Skalierbarkeit** (im Prinzip).
- **Kontinuierliche Verfügbarkeit** trotz (temporärer) Störungen, Erweiterungen oder Reparaturen.

**Middleware** 🎯: Softwareschicht, die zwischen Anwendungen und der verteilten Plattform (Betriebssysteme + Netzwerk der einzelnen Rechner) liegt und die „Verteiltheit“ behandelt. Ausführlich in Abschnitt 2.8.

```
 Rechner A          Rechner B          Rechner C
┌──────────┐      ┌──────────┐      ┌──────────┐
│ Anwend.  │      │ Anwend.  │      │ Anwend.  │
├──────────┴──────┴──────────┴──────┴──────────┤
│                 MIDDLEWARE                    │   ← verbirgt die Verteilung
├──────────┬──────┬──────────┬──────┬──────────┤
│ Betriebs-│      │ Betriebs-│      │ Betriebs-│
│ system A │      │ system B │      │ system C │
└────┬─────┘      └────┬─────┘      └────┬─────┘
     └────────────── Netzwerk ────────────┘
```

**Historisch (⚪):** 1945–1985 waren Computer groß, teuer und selten (isoliertes Arbeiten). Mitte der 1980er machten leistungsfähige, billige Mikroprozessoren und Netzwerke (LAN: hunderte Rechner im Gebäude, WAN: weltweit) den Zusammenschluss vieler Rechner möglich.

---

## 1.2 Die vier Ziele verteilter Systeme 🎯

Warum macht man sich den Aufwand? Ein verteiltes System soll:

| # | Ziel | Kernaussage |
|---|---|---|
| 1 | **Verfügbarmachung von Ressourcen** | Einfacher Zugriff auf und gemeinsame Nutzung von verteilten Ressourcen |
| 2 | **Verteilungstransparenz** | Die physische Verteilung auf mehrere Computer wird verborgen |
| 3 | **Offenheit** | Standardisierte Beschreibung von Syntax (*Wie?*) und Semantik (*Was?*) der Dienste |
| 4 | **Skalierbarkeit** | Erweiterbar bzgl. Nutzer-/Ressourcenzahl, geografischer Ausdehnung, Verwaltungsdomänen |

Merkhilfe: **V-T-O-S** (Verfügbarmachung, Transparenz, Offenheit, Skalierbarkeit).

### Ziel 1: Verfügbarmachung von Ressourcen 🎯
Typische Ressourcen: Computer, Speicher, Dateien, Webseiten, Netzwerke.

- **Gründe:** *Kosteneffizienz* (teure Hardware teilen, z. B. Drucker, Hochleistungsrechner), *Kollaboration* (Datenaustausch, Groupware), *Zugänglichkeit* (weniger physische Präsenz nötig, z. B. Online-Handel).
- **Herausforderungen:** Schutz vor Abhören und Eindringen, Schutz sensibler Daten (Passwörter, Zahlungsdaten), ständig wachsende Datenmengen.
- **Lösungsansätze:** starke Verschlüsselung, sichere Authentifizierung, intelligente Filterung und Suche.

### Ziel 2: Verteilungstransparenz 🎯
„Transparent“ kann zweierlei bedeuten: (1) *vorhanden, aber nicht wahrgenommen* oder (2) *durchsichtig, Verhalten nachvollziehbar*. Für verteilte Systeme ist **Bedeutung (1)** gewünscht: Der Nutzer soll die Verteilung **nicht bemerken**.

**Die 6 Arten von Transparenz** (Beispiele von mir ergänzt):

| Transparenzart | Bedeutung | Beispiel |
|---|---|---|
| **Zugriff** | Einheitlicher Zugriff, unabhängig von der technischen Repräsentation | Datei lesen: gleicher Aufruf, egal ob lokal oder auf Fileserver, egal ob Windows/Linux |
| **Verortung** | Physischer Ort ist irrelevant (logische Namen) | URL statt IP-Adresse/Standort des Servers |
| **Ortsveränderung** (Migration & Relocation) | Keine Beeinflussung nach/während der Verlagerung von Ressourcen | Server zieht in anderes Rechenzentrum, Nutzer merkt nichts |
| **Replikation** | Identischer Zugriff auf Original und Kopien | CDN: man weiß nicht, welche Kopie einer Webseite man bekommt |
| **Nebenläufigkeit** | Mehrere gleichzeitige Nutzer stören sich nicht | Zwei Nutzer buchen gleichzeitig, Ergebnis bleibt konsistent |
| **Störung** | Ausfall und Wiederherstellung bleiben verborgen | Ein Server fällt aus, ein Replikat übernimmt unbemerkt |

> Merke: Der Begriff „Ortsveränderung“ fasst *Migration* (Ressource zieht um) und *Relocation* (Umzug während der Nutzung) zusammen.

### Ziel 3: Offenheit 🎯
Ein verteiltes System besteht aus vielen **Diensten**, die sich nach definierten Syntax- und Semantikregeln verhalten und über **Protokolle** kommunizieren. Definiert werden sie über **Schnittstellen**, oft mit einer **Interface Definition Language (IDL)**.

- **Syntax** = Funktionsnamen, Parameter, Rückgabewerte, Fehler/Ausnahmen.
- **Semantik** = Bedeutung (meist in natürlicher Sprache).
- Eine **gute Spezifikation** ist **vollständig** und **neutral** (macht keine Implementierungsvorgaben).

**Ziele von Offenheit:**
- **Interoperabilität:** Systeme verschiedener Hersteller arbeiten zusammen.
- **Portabilität:** Anwendungen/Komponenten laufen auf verschiedenen Systemen.
- **Erweiterbarkeit:** Komponenten lassen sich leicht ersetzen oder hinzufügen.
- **Flexibilität:** Einbindung alternativer Betriebs- oder Subsysteme (z. B. Dateisysteme).

**Beispiele für Schnittstellenbeschreibungen** 🟡

| | **WSDL** | **OpenAPI (Swagger)** |
|---|---|---|
| Format | XML | JSON oder YAML |
| Fokus | Operationen/Methoden | Ressourcen/Endpunkte |
| Nutzung | SOAP-Webservices | RESTful APIs (HTTP, JSON) |
| Stil | sehr formell, stark typisiert, detaillierte Verträge | menschenlesbar, locker typisiert, interaktive Doku |
| + | standardisiert, formelle Verträge, viele Zusatzstandards | einfach, leichtgewichtig, gut für Webentwicklung |
| − | komplex, Overhead durch XML/SOAP-Header | weniger formelle Verträge, Sicherheit/Transaktionen nicht integriert |
| Einsatz | Unternehmen, Finanz-/Gesundheitswesen | moderne Web-APIs, Microservices, Mobile Apps, Cloud |

### Ziel 4: Skalierbarkeit 🎯
Skalierbarkeit bedeutet Erweiterbarkeit in **drei Dimensionen**:
1. **Größe:** Anzahl Nutzer und Ressourcen
2. **Geografie:** räumliche/physische Verteilung
3. **Verwaltung:** Anzahl unabhängiger Verwaltungsdomänen

#### (a) Skalierbarkeit bzgl. Nutzern/Ressourcen: Grenzen zentralisierter Lösungen
| Zentralisiert bei … | Problem | Beispiel |
|---|---|---|
| **Diensten** | Rechen-/Kommunikationskapazität des einen Servers begrenzt | Ein Server für alle Anfragen = Flaschenhals |
| **Daten** | Speicherung/Verwaltung an einem Ort begrenzt | DNS als eine einzige Tabelle ginge nicht |
| **Algorithmen** | Alle Informationen sammeln und verarbeiten ist unmöglich | Routing mit vollständiger Netzinfo |

**4 Eigenschaften dezentraler Algorithmen** 🎯 (gut merkbar, klausurtauglich)
1. Kein Computer hat komplettes Wissen über den Systemzustand.
2. Entscheidungen basieren auf lokalen Informationen.
3. Der Ausfall eines Computers stört den Algorithmus nicht.
4. Es wird kein global synchronisierter Takt (implizit) vorausgesetzt.

#### (b) Skalierbarkeit bzgl. Geografie: LAN → WAN
| | **LAN** | **WAN** |
|---|---|---|
| Antwortzeit | µs → synchrone Kommunikation okay | ms → synchrone Kommunikation **blockiert** |
| Broadcast | zuverlässig, z. B. für Dienstsuche | **nicht zuverlässig** → spezielle Ortungsdienste nötig |
| Kommunikation | zuverlässig | unzuverlässig, meist Punkt-zu-Punkt |

#### (c) Skalierbarkeit bzgl. Verwaltungsdomänen
Mehrere unabhängige Domänen führen zu Konflikten bei Ressourcennutzung, Verwaltung und Sicherheit. Man vertraut der eigenen Domäne, aber nicht automatisch über Grenzen hinweg. Folgen: Schutz vor Angriffen von außen (eingeschränkter Zugriff für Fremde) und Schutz der eigenen Domäne vor unsicherem fremdem Code.

#### Lösungsansätze für Skalierungsprobleme 🎯

| Ansatz | Idee | Beispiel |
|---|---|---|
| **Latenzen verstecken** | Statt zu warten, andere Arbeit erledigen: **asynchrone Kommunikation** (eigener Thread, Callback beim Antwortempfang). Oder Kommunikation **vermeiden**, indem man Verarbeitung nahe beim Nutzer macht | Formularprüfung **im Client** statt im Server |
| **Aufteilung** (Teile und herrsche) | Komponente zerteilen und über das System verteilen | **DNS** |
| **Replikation** | Kopien von Komponenten: mehr Verfügbarkeit, Lastverteilung, Kopie in Nutzernähe → geringere Latenz. Entscheidung trifft der **Ressourcenbesitzer**, meist im Voraus geplant | Mirror-Server |
| **Caching** | Kopie einer Ressource nahe beim Client. Entscheidung trifft der **Client**, auf Abruf | Browser-Cache |

**Herausforderung bei Replikation/Caching: Konsistenz.** Kopien können auseinanderlaufen. Wie viel Inkonsistenz erlaubt ist, hängt vom Typ ab: Webinhalte tolerieren leichte Verzögerung, Finanztransaktionen brauchen starke Konsistenz.

---

## 1.3 Die acht Fehlannahmen (nach Peter Deutsch) 🎯

Wer zum ersten Mal ein verteiltes System baut, nimmt oft fälschlich an:

1. Das Netzwerk ist **zuverlässig**.
2. Das Netzwerk ist **sicher**.
3. Das Netzwerk ist **homogen**.
4. Die Netzwerktopologie **ändert sich nicht**.
5. Die Latenz ist **0**.
6. Die Bandbreite ist **unendlich**.
7. Die Transportkosten sind **0**.
8. Es gibt **nur einen Administrator**.

Diese Fehlannahmen sind die **Ursache der Komplexität** verteilter Systeme.

---

## 1.4 Arten verteilter Systeme 🟡

```
Verteilte Systeme
├── 1. Verteilte Rechensysteme ......... Cluster Computing, Grid Computing
├── 2. Verteilte Informationssysteme ... Verteilte Transaktionssysteme, Enterprise Application Integration (EAI)
└── 3. Allgegenwärtiges (ubiquitous) verteiltes Computing ... Heimautomatisierung, E-Health, Sensornetze
```

### Verteilte Rechensysteme
| | **Cluster Computing** | **Grid Computing** |
|---|---|---|
| Idee | Supercomputer aus Standard-PCs + schnellem Netz | Mehrere Verwaltungsdomänen zu „virtuellen Organisationen“ zusammengefasst |
| Hardware/OS/Netz | **homogen** (gleich) | **heterogen** (unterschiedlich) |
| Ressourcen | Rechenleistung | Rechenleistung, Speicher, Datenbanken, Spezialgeräte |

**Grid-Schichtenarchitektur** (von unten nach oben): **Fabric** (Schnittstellen zu lokalen Ressourcen) → **Connectivity** (Kommunikations-/Sicherheitsprotokolle, Authentifizierung, Rechte-Delegation) → **Resource** (Verwaltung einzelner Ressourcen, Zugriffskontrolle) → **Collective** (Verwaltung mehrerer Ressourcen: Entdeckung, Aufgabenplanung, Datenreplikation) → **Application**. Die mittleren Schichten bilden die Grid-Middleware.

### Verteilte Informationssysteme
**Verteilte Transaktionssysteme**
- Unternehmensanwendungen basieren meist auf Datenbanken; Zugriffe laufen als **Transaktion** nach dem **Alles-oder-Nichts-Prinzip**.
- **ACID:** **A**tomar, **K**onsistent (engl. *Consistent*), **I**soliert, **D**auerhaft.
- Verteilte Transaktion: Eine Haupttransaktion wird in parallele **Subtransaktionen** aufgeteilt. Änderungen werden erst beim **Commit der Haupttransaktion** dauerhaft. Bricht sie ab, werden **alle Subtransaktionen zurückgenommen**.

**Enterprise Application Integration (EAI):** Anwendungen werden von Datenbanken entkoppelt, die Komponenten müssen direkt kommunizieren.

| | **RPC / RMI** | **Message-Oriented Middleware (MOM)** |
|---|---|---|
| Prinzip | Prozedur-/Methodenaufruf wird als Nachricht verschickt | Nachrichten an logische Kontaktpunkte (Topics), Abonnieren (Publish/Subscribe) |
| − | Aufrufer und Aufgerufener müssen **gleichzeitig verfügbar** sein, **enge Kopplung** | |
| + | | **entkoppelte** Sender/Empfänger, **asynchron** |

### Allgegenwärtiges verteiltes Computing
- Traditionell: feste Knoten, dauerhafte gute Netzverbindung. Hier dagegen: **Instabilität ist der Normalfall** (mobile, batteriebetriebene, drahtlose Geräte), wenig manuelle Kontrolle → **automatische Umgebungserkennung und Anpassung**.
- Anforderungen: Umgebung kann sich jederzeit ändern, Nutzungsarten wechseln (einfache/automatische Konfiguration), Fokus auf Informationsabfrage und -bereitstellung.
- **Verzicht auf Verteilungstransparenz:** Verteilung von Daten, Prozessen und Kontrolle wird **explizit behandelt statt versteckt**.
- **Sensornetze:** hunderte bis tausende kleine, batteriebetriebene Knoten mit Funk, ressourcenbeschränkt (Energie, Rechenleistung, Kommunikation). Extremfälle: *zentralisierte Datensammlung* (hoher Ressourcenverbrauch) vs. *vollständige Verteilung* (möglicher Datenverlust).

---

# 2. Architekturen

**Ziel von Architekturen:** Komplexität reduzieren. Eine Architektur gibt die Organisation des Systems vor, und zwar aus zwei Sichten:

| Sicht | Frage | Inhalt |
|---|---|---|
| **Softwarearchitektur** (logisch) | Aus welchen Softwarekomponenten besteht das System? | Aufteilungs- und Verortungsentscheidungen für Funktionalität. Hilfreiche Prinzipien: SOLID, KISS, DRY, YAGNI |
| **Systemarchitektur** (physisch) | Wie werden die Komponenten auf reale Computer verteilt? | Grundformen: **zentralisiert, dezentralisiert, hybrid** |

**Bestandteile einer Softwarearchitektur:** Komponenten (modulare Einheit mit definierten Schnittstellen), Verbindungen zwischen Komponenten (Kommunikation/Koordination), Datenaustausch (Kooperation), Konfiguration zu einem System.

---

## 2.1 Die vier Architekturstile 🎯

| Stil | Kernidee | Kommunikation / Kontrollfluss | Eigenschaften, Beispiel |
|---|---|---|---|
| **Schichtenarchitektur** | Komponenten in Schichten organisiert. Schicht L<sub>i</sub> ruft nur L<sub>i−1</sub> auf | Anfragen laufen **nach unten**, Antworten **nach oben** | Sehr verbreitet bei Netzwerken (OSI/TCP-IP) |
| **Objektbasierte Architektur** | Jede Komponente ist ein **Objekt** | (verteilter) **Prozeduraufruf** (RPC/RMI) | Passt zum **Client-Server-Modell** |
| **Ereignisbasierte Architektur** | Komponenten kommunizieren über **Ereignisse** (ggf. mit Daten) | **Publish/Subscribe**: Komponenten veröffentlichen und abonnieren Ereignisse, die **Middleware** ordnet zu und leitet weiter | Hauptvorteil: **lose Kopplung** |
| **Datenzentrierte Architektur** | Komponenten kommunizieren über einen **gemeinsamen Datenspeicher** (passiv oder aktiv) | Lesen/Schreiben im Speicher | z. B. Netzwerkanwendungen auf verteilten Dateisystemen |

**Shared Data Spaces** = Kombination aus ereignisbasiert + datenzentriert → zusätzlich **zeitliche Entkopplung**.

Merke dir pro Stil **ein Schlüsselwort**: Schichten → *Aufruf nur nach unten*; Objekte → *Prozeduraufruf*; Ereignisse → *Publish/Subscribe, lose Kopplung*; Daten → *gemeinsamer Speicher*.

---

## 2.2 Client-Server-Modell (zentralisierte Architektur) 🎯 (Probeklausur b)

Das **Rollenmodell** hinter vielen verteilten Systemen, um die Komplexität zu beherrschen. Die Prozesse/Komponenten werden in zwei Gruppen geteilt:
1. **Server** bieten bestimmte Dienste an (z. B. Dateisystem, Datenbank).
2. **Clients** fordern Dienste per **Anfrage** an und warten auf die **Antwort** → **Anfrage-Antwort-Verhalten** (Request/Reply).

| | **Verbindungslos** | **Verbindungsorientiert** |
|---|---|---|
| Geeignet für | zuverlässige Netze (LANs) | unsichere Netze (WANs), Internetprotokolle nutzen TCP |
| + | geringer Overhead, schnell | Performancegewinn durch Mehrfachnutzung der Verbindung und Kompression |
| − | Zusatzaufwand bei Verlust/Beschädigung von Nachrichten | Overhead durch Verbindungsaufbau |

**Rollen können sich überlagern:** Eine Komponente kann gleichzeitig Server *und* Client sein (z. B. Suchmaschinen-Server, der für die Datenbank Client ist).

---

## 2.3 Schichtenarchitektur für interaktive Anwendungen (Drei-Schichten-Architektur) 🎯

| Schicht | Rolle | Aufgabe |
|---|---|---|
| **1. Nutzerschnittstelle** (User Interface) | meist **Client** | Ein-/Ausgabe (textuell, grafisch). Kann bereits lokale Verarbeitung enthalten |
| **2. Verarbeitung** (Processing / Anwendungslogik) | meist **Server und Client** | **Kernfunktionalität** der Anwendung, wenig standardisiert (anwendungsabhängig) |
| **3. Datenhaltung** (Data) | meist **Server** | Verwaltung der Daten (Datenbank, Dateisystem), liefert **persistente** Informationen für die Verarbeitung |

```
  Client                         Server(s)
┌───────────────┐  Anfrage  ┌──────────────────┐  Anfrage  ┌────────────────┐
│ Nutzer-       │ ────────► │ Verarbeitung     │ ────────► │ Datenhaltung   │
│ schnittstelle │ ◄──────── │ (Anwendungslogik)│ ◄──────── │ (DB / Dateien) │
└───────────────┘  Antwort  └──────────────────┘  Antwort  └────────────────┘
```

Beispiel **Internetsuchmaschine**: Browser (UI) → Suchlogik, Query-Verarbeitung (Verarbeitung) → Index-/Dokumentdatenbank (Datenhaltung). Der Verarbeitungsserver ist dabei selbst **Client** der Datenhaltung.

### Thin vs. Fat Clients 🟡
(In den Folien „Fine Clients“, gemeint ist *Thin Client*.) Je nachdem, wie viel der drei Schichten auf den Client verlagert wird:

| Variante | Was macht der Client? |
|---|---|
| (a) | Teile der Nutzerschnittstelle; die Anwendung (Server) kann sie steuern |
| (b) | Komplettes grafisches Frontend, **keine Verarbeitung** |
| (c) | Frontend + z. B. **Prüfung von Nutzereingaben** |
| (d) | **Komplette grafische Anwendung**, spricht direkt mit der Datenbank |
| (e) | wie (d) + **lokale Datenspeicherung** |

Je weiter nach (e), desto „fetter“ der Client (mehr Last auf Clients, weniger auf dem Server, aber aufwändigere Verwaltung).

---

## 2.4 Vertikale vs. horizontale Verteilung 🎯 (Probeklausur c)

| | **Vertikale Verteilung** | **Horizontale Verteilung** |
|---|---|---|
| Idee | Logische **Schichten/Funktionen** auf verschiedene Computer verteilen (die Drei-Schicht-Architektur) | **Clients und Server selbst** werden verteilt: Aufspaltung in logisch **gleichwertige Teile** |
| Folge | **Spezialisierung** der Computer für jeweilige Funktionalität | Jeder Teil arbeitet auf **eigenem Datenausschnitt** → **Lastverteilung** |
| Führt zu | zentralisierter Architektur | **dezentralisierter** Architektur (z. B. Peer-to-Peer) |
| Beispiel | Webshop: Webserver, Anwendungsserver und Datenbankserver laufen auf getrennten Rechnern | Webserver-Farm hinter Lastverteiler; Datenbank-Sharding; Peer-to-Peer-Netz |

---

## 2.5 Peer-to-Peer und Hybride 🟡

**Peer-to-Peer (P2P):** Aufteilung in **gleichberechtigte Prozesse (Peers)**, die Client *und* Server gleichzeitig sind → **symmetrische Interaktion**. Kommunikation über **Overlay-Netzwerke** (Nachrichten werden weitergeleitet).

| | **Strukturiertes P2P** | **Unstrukturiertes P2P** |
|---|---|---|
| Overlay-Aufbau | **deterministisch** | **zufällige** Algorithmen |
| Datenzuordnung | **Verteilte Hashtabelle (DHT)**: Daten und Knoten erhalten Schlüssel aus großem Bereich (z. B. 160 Bit); Anfrage = **Routing** zum zuständigen Knoten | Daten werden **zufällig** auf Knoten verteilt |
| Suche | gezielt über Routing | meist **Flooding** (Nachbarn fragen) |
| Nachbarn | Routing-Tabellen | zufällig gebildete **Nachbarschaftsliste** (Teilsicht) |
| Probleme | dynamisches Hinzufügen von Daten und Knoten, große Daten | isolierte Gruppen, Lastungleichgewicht, Verwerfen alter Einträge |

**Mitgliedschaft (unstrukturiert):** Knoten betreten über bekannte Einstiegspunkte, verlassen das Netz jederzeit ohne Abmeldung; nicht mehr antwortende Nachbarn fliegen automatisch aus der Liste.

**Superpeers:** Skalierbarkeit unstrukturierter P2P-Netze ist beschränkt → Symmetrie wird aufgegeben, **Spezialknoten** speichern Indizes oder fungieren als Broker. Neues Problem: **Wer darf Superpeer sein?** (Leader-Election-Problem, siehe 5.8).

**Hybride Architekturen:** Kombination von Eigenschaften in der Praxis. Beispiel **Edge-Server-Systeme**: Server am Rand von (Sub-)Netzwerken (z. B. beim ISP), Clients verbinden sich mit dem Edge-Server ihres Netzes.

---

## 2.6 Middleware 🎯 (Probeklausur d)

> **Middleware** ist eine **Softwareschicht zwischen Anwendung und verteilter Plattform** (Betriebssystem/Netzwerk). **Ziel:** **Verteilungstransparenz** erreichen. Daten, Verarbeitung und Kontrolle werden vor der Anwendung verborgen.

**Wozu?** Ohne Middleware müsste jede Anwendung selbst Kommunikation, Heterogenität, Namensdienste usw. behandeln. Die Middleware bietet allgemeine Dienste (Authentifizierung, Autorisierung, Transaktionen, Locks, Kommunikation) und vereinfacht die Anwendungsentwicklung.

**Architekturstile von Middleware:**
- **objektbasiert**, z. B. **CORBA** (Common Object Request Broker Architecture)
- **ereignisbasiert**, z. B. **ROS** (Robot Operating System)

**Vorteil:** vereinfacht Anwendungsentwicklung. **Nachteil:** Einschränkungen, fehlende Flexibilität. Beispiel CORBA: zunächst nur Remote-Objektaufrufe, später um Nachrichtenübermittlung erweitert.

---

## 2.7 Adaptive Middleware und Selbstmanagement ⚪

- **Anpassung von Middleware:** *statisch* über Daten (Parameter, Spezifikationen) oder *dynamisch* über Code (**Interceptoren**, Callbacks).
- **Techniken adaptiver Software:** *Separation of Concerns* (Trennung der Verantwortlichkeiten, schwierig bei nicht-funktionalen Anforderungen wie Sicherheit/Performance), *Computational Reflection* (Programm inspiziert sich selbst und ändert Verhalten zur Laufzeit, nicht in jeder Sprache möglich), *komponentenbasierte Architektur* (Komposition statisch/dynamisch, erfordert **Late Binding**).
- **Selbstmanagement:** Systeme passen Verhalten/Verteilung selbstständig an Umgebungsänderungen an → **Regelkreismodell (Feedback Control Model)**: messen → vergleichen/analysieren → anpassen → wieder messen.

---

# 3. Prozesse

## 3.1 Prozesse vs. Threads (Grundlage) 🟡

| | **Prozess** | **Thread** |
|---|---|---|
| Zustand | **vollständig**: CPU-Kontext, Speicher, Ressourcen | **minimal**: nur CPU-Kontext |
| Isolation | voneinander **isoliert** | mehrere Threads **innerhalb eines Prozesses** |
| Kommunikation | aufwändig: **Interprozesskommunikation (IPC)** | über **gemeinsamen Speicher** → **Synchronisation notwendig** |
| Granularität | grob → **hoher Overhead** | fein → **hohe Performance** |

**Vorteile von Threads in normalen (nicht-verteilten) Systemen:**
- **Blockierende Operationen überbrücken** (GUI getrennt von Verarbeitung; blockierende Systemaufrufe überlagern)
- **Mehrere CPUs/Kerne nutzen** (rechenintensive Arbeit aufteilen, parallele Ausführung)
- **Große Anwendungen aufteilen** (Threads statt Prozesse mit IPC)
- **Implementierung strukturieren** (unabhängige Aufgaben)

---

## 3.2 Einsatz von Threads in verteilten Systemen 🎯

Kernidee: **Blockierende Systemaufrufe nutzen, ohne den ganzen Prozess zu blockieren**, und **mehrere logische Verbindungen** parallel verwalten.

### Multithreaded **Clients**
- Problem: In verteilten Systemen sind Nachrichtenlaufzeiten **lang** (hunderte Millisekunden bis Sekunden) und müssen **verborgen** werden.
- Ansatz: **Kommunikation starten und mit anderen Aufgaben fortfahren**.
- **Beispiel Webbrowser:** Seite wird geladen und angezeigt, während Bilder usw. **parallel** über **separate Verbindungen** von Threads nachgeladen werden.
  - ➕ Nutzer kann mit der Seite interagieren, während andere Inhalte noch laden
  - ➕ **Lastverteilung** auf replizierte Webserver durch parallele Verbindungen

### Multithreaded **Server** (Hauptnutzung von Multithreading!)
- Vereinfacht die **Server-Implementierung** und nutzt **Parallelisierung** zur Performanceverbesserung.
- Server sollen **mehrere Anfragen** gleichzeitig bearbeiten und müssen auf lokale Ressourcen (z. B. Festplatte) warten können.
- **Beispiel Dateiserver:**

| | **Single-threaded** | **Multi-threaded** |
|---|---|---|
| Aufbau | Hauptschleife arbeitet Anfragen **sequentiell** ab | **Dispatcher-Thread** nimmt Anfragen an und verteilt sie auf **Worker-Threads** |
| Konkurrierende Anfragen | ➖ hohe Wartezeiten | ➕ parallele Abarbeitung |
| Festplattenzugriff | ➖ CPU **idle** während des Wartens | ➕ CPU wird in der Zeit **weiter genutzt** (anderer Thread arbeitet) |

```
Anfragen ──► [Dispatcher-Thread] ──┬──► [Worker 1] ──► Festplatte
                                   ├──► [Worker 2] ──► Festplatte
                                   └──► [Worker 3] ──► Festplatte
```

---

## 3.3 Server und Zustände 🎯

| | **Zustandsloser Server (stateless)** | **Zustandsbehafteter Server (stateful)** |
|---|---|---|
| Speichert Client-Infos? | **Nein** | **Ja, persistent**. Muss explizit gelöscht werden |
| Eigener Zustand | ändert sich unabhängig, **ohne Clients zu informieren** | Server „kennt“ seine Clients |
| Verlust von Zustandsinfo | **stört den Dienst nicht** | Nach Absturz muss der Zustand **wiederhergestellt** werden |
| Vorteil | einfach, robust, leicht replizierbar | **Performance** |
| Beispiel | **Webserver**: beantwortet HTTP-Anfrage und vergisst den Client. Inhalte können sich ändern, ohne dass Clients informiert werden (Log-Daten sind kein Widerspruch) | **Dateiserver**: weiß, welcher Client welche Datei liest/schreibt → schnellere Lese-/Schreiboperationen; nach Absturz muss rekonstruiert werden, wer den aktuellen Stand einer Datei hat |

**Sonderfall Soft State:** Server hält Zustandsinformation nur **zeitlich begrenzt**. Läuft sie ab, wird sie verworfen (Rückfall auf zustandslos).

---

## 3.4 Server-Realisierungen 🟡

**Grundablauf eines Servers:** (1) auf eingehende Anfrage warten → (2) Anfrage bearbeiten + Antwort senden → (3) weiter warten.

| | **Iterativer Server** | **Nebenläufiger (concurrent) Server** |
|---|---|---|
| Prinzip | Server bearbeitet Anfrage **selbst**, sendet selbst die Antwort | Anfrage wird an **separaten Thread/Prozess** übergeben, Server wartet **sofort** auf die nächste Anfrage |
| Antwort durch | den Server | den verantwortlichen Thread/Prozess |
| Varianten | | **Multithreaded Server** (neuer oder vorhandener Thread); **Fork-Server** (UNIX/Linux: neuer Prozess per `fork`) |

---

## 3.5 Weiteres zu Prozessen ⚪

### Virtualisierung
Prozesse/Threads teilen sich *eine CPU*. **Virtualisierung** erweitert das Konzept auf **andere Ressourcen**, indem **Schnittstellen nachgeahmt** werden.
- **Warum in verteilten Systemen?** Legacy-Software auf neuen Plattformen, einfachere Verwaltung **heterogener** Systeme (jede Anwendung in eigener VM-Umgebung), **Portabilität/Flexibilität** (komplette Systeme replizieren und migrieren, z. B. für CDNs).
- **Vier Schnittstellen** eines Computersystems: (1) Bibliotheks-APIs (Anwendung ↔ Bibliothek), (2) Systemaufrufe (Bibliothek ↔ Betriebssystem), (3) privilegierte Instruktionen (OS ↔ Hardware), (4) allgemeine Instruktionen (Anwendung ↔ Hardware).
- **Drei Arten:**

| Art | Prinzip | Beispiele |
|---|---|---|
| **Process Virtual Machine** | Laufzeitsystem führt Anwendung mit abstrakten Instruktionen aus (interpretiert oder emuliert) | JRE (Interpretation), Windows-Programme unter Linux (Emulation) |
| **Virtual Machine Monitor (VMM)** | Schicht schirmt die **Hardware komplett ab**, mehrere verschiedene Betriebssysteme möglich | VMware vSphere, Hyper-V, KVM |
| **Containerization** | Vorhandenes OS wird als **isolierte Ausführungsumgebung** bereitgestellt. ➕ hohe Performance, geringer Overhead (OS wird wiederverwendet) | Docker, Kubernetes |

### Client-Realisierungen
Hauptaufgabe: **Nutzerschnittstelle** zur Interaktion mit einem Server. Anwendungsspezifisches Protokoll (z. B. Terminplaner ↔ Kalenderserver) oder anwendungsunabhängiges Protokoll (X Window System, Smartphone-Apps).
**Client-seitige Unterstützung für Transparenz:**
- *Zugriff*: **Client-Stubs** (Platzhalter für Server-Schnittstellen) verbergen Kommunikation und Server-Unterschiede
- *Verortung/Ortsveränderung*: ortsunabhängige Namen/Adressen
- *Replikation*: Anfragen an replizierte Server weiterleiten, mehrfache Antworten zu einer reduzieren
- *Störung*: Kommunikationsfehler maskieren (Wiederholen, Caching)

### Server-Kontaktpunkte
Server „hört“ an einem **Endpoint/Port**. Clients brauchen **Adresse** (fest, z. B. 8.8.8.8, oder dynamisch über DNS) **und Kontaktpunkt**.
| | **Statisch** (z. B. HTTP:80, HTTPS:443, SSH:22, DNS:UDP 53) | **Dynamisch** |
|---|---|---|
| | ➕ direkt nutzbar, schnell ➖ begrenzte Anzahl | ➖ nur indirekt (höhere Antwortzeit) ➕ flexibel für beliebige Dienste |

Dynamische Realisierungen: **Endpoint-Daemon** (separater Server mit festem Port und Verzeichnis; Server registrieren sich dort, Clients fragen dort nach; ➖ jeder Server muss separat laufen) und **Superserver** (hört auf vielen Ports und **startet** den passenden Server bei Anfrage, z. B. `inetd`; ➕ nur ein Prozess wartet, ressourceneffizient).

### Server-Cluster
Menge von Computern, die je einen oder mehrere Server ausführen. **Dreistufig:** (1) logischer **Switch** (routet Anfragen), (2) **Anwendungs-/Rechenserver**, (3) **Datenverarbeitungsserver** (Datei/DB).
**Management:** Mit wachsender Knotenzahl steigt die Fehlerwahrscheinlichkeit. Beispiel N = 1000 Server, Ausfallrate je Server p = 0,1 %: P(kein Ausfall) = (1 − p)<sup>N</sup> = 0,999<sup>1000</sup> ≈ **36 %**, also fällt mit ~64 % Wahrscheinlichkeit *mindestens ein* Server aus. Heute: Automatisierung, Container-Orchestrierung, serverlose Architekturen, **Self-healing**, Multi-Cloud.

### Code-Migration
Programme (teils während der Ausführung) verschieben statt nur Daten.
- **Gründe:** Leistung (von stark auf weniger ausgelastete Rechner), **Kommunikation minimieren** (Code zu den Daten), Flexibilität (Software bei Bedarf zum Client laden, dynamische Konfiguration).
- **Herausforderungen:** Sicherheit (Vertrauen in geladenen Code), standardisierte Protokolle.
- **Modelle:** *schwache Mobilität* (nur Code + ggf. Initialisierungsdaten, Start an vordefinierten Punkten) vs. *starke Mobilität* (Ausführungssegment wie Instruktionszeiger/Stack wandert mit, laufender Prozess kann gestoppt/verschoben/fortgesetzt werden). *Sender-initiiert* (z. B. Upload zu Rechenserver) vs. *Empfänger-initiiert* (z. B. Java-Applets).
- **Weitere Probleme:** Ressourcenzugriff (Ports/Dateien müssen angepasst werden), **Heterogenität** (Lösung: VMs wie die JVM oder Migration ganzer Ausführungsumgebungen; Live-Migration von VMs im VMware-Cluster).

---
