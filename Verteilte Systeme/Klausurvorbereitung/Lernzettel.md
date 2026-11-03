# Lernzettel: Verteilte Systeme (Wintersemester 2026)

**Dozent:** Dr. M. Hofmann · DHSN Glauchau
**Grundlage:** 6 Vorlesungen (31.08. – 02.11.2026) und 5 Übungsserien
**Literatur:** Tanenbaum / van Steen: *Verteilte Systeme – Grundlagen und Paradigmen*, 2. Aufl., Addison Wesley, 2007

> **So benutzt du das Dokument:**
> Kapitel 1–7 fassen die Vorlesungen zusammen. Kapitel 8 ist der Fragenkatalog im Stil der Übungen (Übung 5 = Probeklausur) mit Musterantworten. Kapitel 9 passt die Übungsaufgaben auf **Linux** an. Kapitel 10 ist der Spickzettel, Kapitel 11 listet Fehler im Material.
> Beim Selbsttest die Antworten (die Zeilen mit `>`) einfach abdecken.

---

## Inhaltsverzeichnis

- [0. Überblick und Klausurinfos](#0-überblick-und-klausurinfos)
- [1. Einführung](#1-einführung)
- [2. Architekturen](#2-architekturen)
- [3. Prozesse](#3-prozesse)
- [4. Kommunikation](#4-kommunikation)
- [5. Synchronisation](#5-synchronisation)
- [6. Konsistenz und Replikation](#6-konsistenz-und-replikation)
- [7. Fehlertoleranz](#7-fehlertoleranz)
- [8. Fragenkatalog](#8-fragenkatalog)
- [9. Linux-Praxisteil](#9-linux-praxisteil)
- [10. Spickzettel](#10-spickzettel)
- [11. Korrekturen und Unstimmigkeiten im Material](#11-korrekturen-und-unstimmigkeiten-im-material)

---

## 0. Überblick und Klausurinfos

### Organisatorisches

| Punkt | Inhalt |
|---|---|
| Umfang | 6 Termine à 2×90 Minuten = 24 LVS |
| Klausur | **120 Minuten** (Modul „Theorie der Betriebssysteme und verteilten Systeme“), davon **⅓ Verteilte Systeme** (≈ 40 Minuten) |
| Materialien | OPAL: „Theorie der Betriebssysteme und verteilten Systeme“ |

### Was laut Übung 5 klausurrelevant ist

Die 5. Übungsserie listet die klausurrelevanten Themen ausdrücklich. Das ist deine Prioritätenliste:

| Thema | Explizit genannte Schwerpunkte | Kapitel |
|---|---|---|
| Einführung | Begriffsdefinitionen, Ziele, Eigenschaften | [1](#1-einführung) |
| Architekturen | Architekturstile und ihre Eigenschaften; Schichtenarchitektur für interaktive Anwendungen | [2](#2-architekturen) |
| Prozesse | Einsatz von Threads in verteilten Systemen; Server und Zustände | [3](#3-prozesse) |
| Kommunikation | Arten von Kommunikation; Remote Procedure Call | [4](#4-kommunikation) |
| Synchronisation | Uhrensynchronisation; NTP | [5](#5-synchronisation) |
| Replikation | Einsatzgründe | [6](#6-konsistenz-und-replikation) |
| Fehlertoleranz | Begriffsdefinitionen; Einsatz von Redundanz | [7](#7-fehlertoleranz) |

Zusätzlich stehen in der Probeklausur (Übung 5, Aufgabe 1): **Architekturstile, Rollenmodell (Client-Server), vertikale/horizontale Verteilung, Middleware.**

**Kennzeichnung in diesem Dokument:**

- `★★★` = in Übung 5 ausdrücklich als klausurrelevant genannt, zuerst lernen
- `★★` = Vorlesungsstoff, aber in Übung 5 nicht ausdrücklich genannt, danach lernen

> **Wichtig:** „Nicht ausdrücklich genannt“ heißt nicht „kommt garantiert nicht dran“. Es ist nur eine Priorisierung. Wenn die Zeit knapp ist, lerne zuerst alle `★★★`-Teile und die Probeklausur-Fragen.

### Die Vorlesungen im Überblick

| Nr. | Datum | Thema |
|---|---|---|
| 1 | 31.08.2026 | Einführung |
| 2 | 10.09.2026 | Architekturen |
| 3 | 14.09.2026 | Prozesse |
| 4 | 14.10.2026 | Kommunikation |
| 5 | 27.10.2026 | Synchronisation |
| 6 | 02.11.2026 | Konsistenz und Replikation · Fehlertoleranz · Wiederholung |

### Der rote Faden

Ein verteiltes System soll nach außen wie **ein** System wirken (Transparenz), obwohl es aus vielen unabhängigen, fehleranfälligen Rechnern besteht, die nur über ein unzuverlässiges Netzwerk kommunizieren. Daraus ergeben sich die Kapitel:

```
Ziele (Kap. 1)         -> was wollen wir erreichen?
Architekturen (Kap. 2) -> wie organisieren wir Komponenten und Rechner?
Prozesse (Kap. 3)      -> wie laufen Clients/Server, wie nutzen wir Threads?
Kommunikation (Kap. 4) -> wie tauschen Prozesse Daten aus? (RPC, Nachrichten, Streams)
Synchronisation (Kap. 5) -> wie einigen sich Prozesse (Zeit, Reihenfolge, Zugriff, Koordinator)?
Replikation (Kap. 6)   -> Kopien für Leistung/Zuverlässigkeit, aber: Konsistenz!
Fehlertoleranz (Kap. 7) -> wie überleben wir Teilausfälle?
```

---

## 1. Einführung

*(Vorlesung 1 · Übung 1, Übung 5)*

### 1.1 Historische Entwicklung `★★`

| Phase | Merkmale |
|---|---|
| **1945–1985** | Computer groß, teuer (teils > 10 Mio. $), selten. Wenige Rechner pro Organisation, keine Vernetzung, isoliertes Arbeiten. |
| **Mitte der 1980er** | Leistungsfähige Mikroprozessoren (8/16/32/64 Bit): Mainframe-Leistung zu einem Bruchteil der Kosten. Preis-/Leistungsgewinn etwa Faktor 10¹³ in 50 Jahren. |
| **Netzwerke** | **LAN** (hunderte Rechner in Gebäuden), **WAN** (global, Millionen Rechner). |
| **Ergebnis** | Viele Rechner über Hochgeschwindigkeitsnetze zu **verteilten Systemen** kombiniert (Gegensatz: zentralisiertes System = Einzelrechner mit Terminals). |

### 1.2 Definition und Eigenschaften `★★★`

> **Definition:** Ein **verteiltes System** ist eine Ansammlung **unabhängiger Computer**, die für ihre Nutzer wie ein **einziges zusammenhängendes System** erscheint.

- Keine Einschränkung, welche Art von Computern oder Verbindungen.
- Autonome Komponenten müssen zusammenarbeiten, das ist die zentrale Herausforderung.

**Wichtige Eigenschaften:**

1. Unterschiede zwischen den Computern, ihre Kommunikation und die interne Organisation sind **vor dem Nutzer verborgen**.
2. **Einheitliche Nutzung** unabhängig von Ort und Zeit.
3. Gute **Erweiterbarkeit und Skalierbarkeit** (im Prinzip).
4. **Kontinuierliche Verfügbarkeit** trotz (temporärer) Störungen, Erweiterungen oder Reparaturen.

### 1.3 Allgemeiner Aufbau: Middleware `★★★`

Um die Herausforderungen zu beherrschen, wird eine **Middleware-Softwareschicht** zur Behandlung der „Verteiltheit“ eingezogen. Sie liegt zwischen Anwendung und verteilter Plattform (Betriebssystem/Netzwerk). Details in [2.4](#23-middleware-).

```
 Rechner A            Rechner B            Rechner C
+-----------+        +-----------+        +-----------+
| Anwendung |        | Anwendung |        | Anwendung |
+-----------+--------+-----------+--------+-----------+
|             M I D D L E W A R E                      |
+-----------+        +-----------+        +-----------+
| Betriebs- |        | Betriebs- |        | Betriebs- |
| system    |        | system    |        | system    |
+-----------+--------+-----------+--------+-----------+
|                     Netzwerk                         |
+------------------------------------------------------+
```

### 1.4 Die vier Ziele verteilter Systeme `★★★`

Warum der Aufwand? Verteilte Systeme ermöglichen:

| # | Ziel | Kerngedanke |
|---|---|---|
| 1 | **Verfügbarmachung von Ressourcen** | Einfacher Zugriff und gemeinsame Nutzung verteilter Ressourcen |
| 2 | **Verteilungstransparenz** | Physische Verteilung auf mehrere Computer wird verborgen |
| 3 | **Offenheit** | Standardisierte Beschreibung von Syntax (*Wie?*) und Semantik (*Was?*) der Dienste |
| 4 | **Skalierbarkeit** | Erweiterbarkeit bzgl. Nutzer-/Ressourcenzahl, Geografie, Verwaltungsdomänen |

#### Ziel 1: Verfügbarmachung von Ressourcen

- Typische Ressourcen: Computer, Speicher, Dateien, Webseiten, Netzwerke.
- **Gründe:** Kosteneffizienz (teure Hardware teilen: Drucker, Hochleistungsrechner, Speichersysteme), Kollaboration (Datenaustausch, Groupware), Zugänglichkeit (weniger physische Präsenz, z. B. Online-Handel).
- **Herausforderungen:** Schutz vor Abhören und Eindringen, Schutz sensibler Daten (Passwörter, Zahlungsinformationen), ständig wachsende Datenmengen.
- **Lösungsansätze:** starke Verschlüsselung, sichere Authentifizierung, intelligente Filterung und Suche.

#### Ziel 2: Verteilungstransparenz

Transparent heißt für Computersysteme:

1. *vorhanden, aber vom Nutzer nicht wahrgenommen*, **oder**
2. *durchsichtig, sodass das Verhalten nachvollzogen werden kann*.

Für verteilte Systeme ist **Definition 1** gewünscht: Die Verteilung soll unsichtbar sein.

**Arten von Transparenz:**

| Art | Bedeutung | Beispiel (zur Orientierung) |
|---|---|---|
| **Zugriff** | Einheitlicher Zugriff unabhängig von technischer Repräsentation | Datei lesen, egal ob lokal oder auf fremdem Betriebssystem |
| **Verortung** (Location) | Physische Orte sind irrelevant, z. B. durch logische Benennung | URL statt IP-Adresse und Rechnerstandort |
| **Ortsveränderung** (Migration & Relocation) | Keine Beeinflussung nach/während der Verschiebung | Dienst zieht auf anderen Server um, Nutzer merken nichts |
| **Replikation** | Identischer Zugriff auf Original und Kopien | Mirror-Server |
| **Nebenläufigkeit** | Gleichzeitige Nutzer stören sich nicht | Viele Nutzer buchen gleichzeitig |
| **Störung** (Failure) | Ausfall und Wiederherstellung bleiben verborgen | Ausgefallener Server wird unbemerkt ersetzt |

> **Merkhilfe (Z-V-O-R-N-S):** **Z**ugriff, **V**erortung, **O**rtsveränderung, **R**eplikation, **N**ebenläufigkeit, **S**törung.

> **Achtung:** Vollständige Transparenz ist nicht immer erreichbar oder sinnvoll (z. B. Latenzen lassen sich nicht wegzaubern). Bei allgegenwärtigem Computing wird sie bewusst aufgegeben ([1.6](#16-arten-verteilter-systeme-)).

#### Ziel 3: Offenheit

- Verteilte Systeme sind eine **Vielzahl an Diensten**, die nach definierten Syntax- und Semantikregeln arbeiten und über **Protokolle** in Netzwerken kommunizieren.
- Definition über **Schnittstellen**, z. B. mit einer **Interface Definition Language (IDL)**.
- **Syntax:** Funktionsnamen, Parameter, Rückgabewerte, Fehler/Ausnahmen. **Semantik:** Bedeutung (oft in natürlicher Sprache).
- Gute Spezifikationen sind **vollständig und neutral** (keine Implementierungsvorgaben).

**Ziele von Offenheit:**

| Ziel | Bedeutung |
|---|---|
| **Interoperabilität** | Systeme verschiedener Hersteller arbeiten zusammen |
| **Portabilität** | Anwendungen/Komponenten laufen auf verschiedenen Systemen |
| **Erweiterbarkeit** | Komponenten leicht ersetzen oder hinzufügen |
| **Flexibilität** | Alternative Betriebs-/Subsysteme einbinden (z. B. Dateisysteme) |

**Beispiele für Schnittstellenbeschreibungen:**

| | **WSDL** | **OpenAPI (Swagger)** |
|---|---|---|
| Technologie | XML-basiert, formale Beschreibung | JSON- oder YAML-basiert |
| Fokus | Operationen/Methoden | Ressourcen/Endpunkte |
| Hauptnutzung | SOAP-Webservices | RESTful APIs (HTTP, JSON) |
| Stil | sehr formell, stark typisiert, detaillierte Verträge | menschenlesbar, locker typisiert, interaktive Doku |
| Vorteile | standardisiert, formelle Verträge, viele Zusatzstandards | einfach, leichtgewichtig, gut für Web |
| Nachteile | komplex, Overhead durch XML/SOAP-Header | weniger formelle Verträge, Sicherheit/Transaktionen nicht integriert |
| Einsatz | Unternehmen, Finanz-, Gesundheitswesen (starke Verträge, Transaktionen) | Web-APIs, Microservices, Mobile Apps, Cloud |

*(Demo aus der Vorlesung: Taschenrechner als Web-Service mit OpenAPI, Grundlage von Übung 1, siehe [9.1](#91-übung-1--openapi-taschenrechner).)*

#### Ziel 4: Skalierbarkeit `★★★`

Drei Dimensionen:

1. **Größe**: Anzahl Nutzer und Ressourcen
2. **Geografie**: Entfernung zwischen Nutzern/Ressourcen
3. **Verwaltung**: Anzahl unabhängiger Verwaltungsdomänen

**Probleme zentralisierter Lösungen (Größe):**

| Aspekt | Problem | Beispiel |
|---|---|---|
| **Dienste** | Lokale Rechen-/Kommunikationskapazität begrenzt | Ein Server für alle Anfragen wird zum **Flaschenhals** |
| **Daten** | Lokale Speicherung/Verwaltung begrenzt | DNS als Einzeltabelle funktioniert nicht |
| **Algorithmen** | Sammlung und Verarbeitung *aller* Informationen unmöglich | Routing mit vollständiger Information |

**Eigenschaften dezentraler Algorithmen:**

1. Kein Computer hat komplettes Wissen über den Systemzustand.
2. Entscheidungen basieren auf **lokalen Informationen**.
3. Ausfall eines Computers stört den Algorithmus nicht.
4. Es wird **kein global synchronisierter Takt** vorausgesetzt.

**Geografische Skalierung (LAN → WAN):**

| | LAN | WAN |
|---|---|---|
| Antwortzeit | µs → synchrone Kommunikation praktikabel | ms → synchrone Kommunikation **blockiert** |
| Broadcast | zuverlässig (z. B. Dienstsuche) | nicht zuverlässig, spezielle Ortungsdienste nötig |
| Kommunikation | zuverlässig | unzuverlässig, meist Point-to-Point |

**Verwaltungsdomänen:** Konflikte bei Ressourcennutzung, Verwaltung und Sicherheit. Vertrauen gilt in der eigenen Domäne, aber nicht automatisch über Domänengrenzen. Nötig sind Schutz vor Angriffen von außen (eingeschränkter Zugriff für Fremde) und Schutz der eigenen Domäne vor unsicherem fremden Code.

**Lösungsansätze für Skalierungsprobleme:**

| Ansatz | Idee | Beispiel |
|---|---|---|
| **Latenzen verstecken** | Während des Wartens andere Aufgaben erledigen: asynchrone Kommunikation (eigene Threads, **Callbacks**). Kommunikation vermeiden: Verarbeitung nahe beim Nutzer. | Formularprüfung **im Client** statt auf dem Server |
| **Aufteilung** (Teile und herrsche) | Komponente zerteilen und über das System verteilen | **DNS** |
| **Replikation** | Kopien von Komponenten: höhere Verfügbarkeit, Lastverteilung, Kopie in Nutzernähe. Entscheidung durch **Ressourcenbesitzer**, meist **im Voraus geplant** | Mirror-Server |
| **Caching** | Kopie einer Ressource nahe beim Client. Entscheidung durch den **Client**, **auf Abruf** | Browser-Cache |

> **Prüfungsklassiker: Replikation vs. Caching**
> Replikation: Besitzer entscheidet, geplant. Caching: Client entscheidet, auf Abruf. Beides erzeugt das Problem der **Konsistenz**: Kopien laufen auseinander, und je nach Ressource sind unterschiedliche Inkonsistenzen erlaubt (Webinhalte tolerieren leichte Verzögerung, Finanztransaktionen brauchen **starke Konsistenz**).

#### Fallstricke: Die 8 Fehlannahmen nach Peter Deutsch `★★★`

Entwickler machen beim ersten verteilten System (fälschlich) diese Annahmen:

1. Das Netzwerk ist **zuverlässig**.
2. Das Netzwerk ist **sicher**.
3. Das Netzwerk ist **homogen**.
4. Die **Topologie** ändert sich nicht.
5. Die **Latenz ist 0**.
6. Die **Bandbreite ist unendlich**.
7. Die **Transportkosten sind 0**.
8. Es gibt **nur einen Administrator**.

### 1.5 Ziel-Zusammenfassung als Kurzmerkzettel `★★★`

```
Ziele:        Ressourcen teilen | Transparenz | Offenheit | Skalierbarkeit
Transparenz:  Zugriff, Verortung, Ortsveränderung, Replikation, Nebenläufigkeit, Störung
Offenheit:    Interoperabilität, Portabilität, Erweiterbarkeit, Flexibilität (via IDL)
Skalierung:   Größe, Geografie, Verwaltung
Techniken:    Latenz verstecken | Aufteilen | Replizieren | Cachen  (-> Konsistenzproblem)
```

### 1.6 Arten verteilter Systeme `★★`

#### (1) Verteilte Rechensysteme

| | **Cluster Computing** | **Grid Computing** |
|---|---|---|
| Idee | Supercomputer aus Standard-PCs + Hochgeschwindigkeitsnetz | Rechner mehrerer Verwaltungsdomänen zu **virtuellen Organisationen** zusammengefasst |
| Hardware/OS/Netz | **homogen** | **heterogen** |
| Ressourcen | Rechenleistung | Rechenleistung, Speicher, Datenbanken, Spezialgeräte … |

**Schichtenarchitektur eines Grids** (unten → oben):

1. **Fabric**: Schnittstellen zu lokalen Ressourcen
2. **Connectivity**: Kommunikations-/Sicherheitsprotokolle, Authentifizierung, Rechte-Delegation
3. **Resource**: Verwaltung einzelner Ressourcen, Zugriffskontrolle
4. **Collective**: Verwaltung mehrerer Ressourcen (Entdeckung, Aufgabenplanung, Datenreplikation)
5. **Application**: Anwendungen innerhalb der virtuellen Organisationen

Die Schichten 2–4 bilden die **Middleware**.

#### (2) Verteilte Informationssysteme

**Verteilte Transaktionssysteme**

- Unternehmensanwendungen basieren meist auf Datenbanken. Zugriffe erfolgen als **Transaktion** nach dem **Alles-oder-Nichts-Prinzip**.
- **ACID:** **A**tomar, **K**onsistent (*Consistent*), **I**soliert, **D**auerhaft
- **Verteilte Transaktion:** Haupttransaktion wird in mehrere **parallele Subtransaktionen** zerlegt. Änderungen werden erst beim **Commit der Haupttransaktion** dauerhaft. Bei **Abbruch** werden **alle** Subtransaktionen zurückgenommen.

**Enterprise-Anwendungsintegration (EAI)**: Anwendungen und Datenbanken werden entkoppelt, die Komponenten müssen direkt kommunizieren:

| | **RPC / RMI** | **Message-Oriented Middleware (MOM)** |
|---|---|---|
| Idee | Lokaler Aufruf wird als Nachricht versendet | Nachrichten an logische Kontaktpunkte (Topics/Subjects), Abonnieren (Publish/Subscribe) |
| Vorteile | Zugriffstransparenz | Sender und Empfänger **entkoppelt**, **asynchron** |
| Nachteile | Aufrufer und Aufgerufener müssen **gleichzeitig verfügbar** sein, **enge Kopplung** | Kommunikation ist sichtbar (keine Zugriffstransparenz) |

#### (3) Allgegenwärtiges verteiltes Computing (Ubiquitous)

- Beispiele: Heimautomatisierung, elektronische Gesundheitssysteme, Sensornetzwerke.
- Klassische VS: feste Knoten, dauerhaft gute Verbindung, Transparenz und Fehlerbehandlung.
- Allgegenwärtige VS: **Instabilität ist der Normalfall** (mobil, batteriebetrieben, drahtlos), wenig manuelle Kontrolle → **automatische Umgebungsentdeckung und Anpassung**, einfache/automatische Konfiguration, Fokus auf Informationsabfrage und -bereitstellung.
- **Verzicht auf Verteilungstransparenz:** Verteilung von Daten, Prozessen und Kontrolle wird **explizit behandelt**, nicht versteckt.

**Beispiel Sensornetzwerk:** Hunderte bis Tausende kleine, meist batteriebetriebene Knoten mit kabelloser Kommunikation, **ressourcenbeschränkt** (Energie, Rechenleistung, Kommunikation). Zwei Extremfälle der Organisation:

| Extrem | Folge |
|---|---|
| **Zentralisierte** Datensammlung (alle Daten zu einem Punkt) | hoher Ressourcenverbrauch |
| **Vollständige Verteilung** (Daten bleiben auf den Knoten) | möglicher Datenverlust |

---

## 2. Architekturen

*(Vorlesung 2 · Übung 2, Übung 5)*

**Ziel von (IT-)Architekturen:** Reduktion von Komplexität. Sie geben die Organisation des verteilten Systems vor, und zwar aus zwei Sichten:

| Sicht | Frage | Entscheidungshilfen / Formen |
|---|---|---|
| **Softwarearchitektur** (logisch) | Aus welchen Softwarekomponenten besteht das System? Aufteilungs- und Verortungsentscheidungen für Funktionalitäten | Prinzipien: SOLID, KISS, DRY, YAGNI |
| **Systemarchitektur** (physisch) | Wie werden die Softwarekomponenten auf reale Computer verteilt? | zentralisiert, dezentralisiert, hybrid |

### 2.1 Architekturstile `★★★`

**Wozu Softwarearchitektur?** Sie ist entscheidend für die erfolgreiche Entwicklung großer Systeme.

**Bestandteile:**

- **Komponenten**: modulare Einheiten mit definierten Schnittstellen
- **Verbindungen** zwischen Komponenten: Kommunikation und Koordination
- **Datenaustausch** zwischen Komponenten: Kooperation
- **Konfiguration** der Komponenten zu einem System

**Die vier Architekturstile für verteilte Systeme:**

| Stil | Kernidee | Wichtige Eigenschaften | Beispiel |
|---|---|---|---|
| **1. Schichten** | Komponenten in Schichten organisiert. Komponente in Schicht L<sub>i</sub> ruft **nur** Schicht L<sub>i−1</sub> auf. Anfragen gehen **nach unten**, Antworten **nach oben**. | Kontrollfluss von Schicht zu Schicht; hohe Verbreitung bei Netzwerken | OSI-Modell, Drei-Schichten-Anwendung |
| **2. Objektbasiert** | Jede Komponente ist ein **Objekt**; Verbindung per **(verteiltem) Prozeduraufruf** | Passt zum **Client-Server-Modell** | CORBA, RPC/RMI |
| **3. Ereignisbasiert** | Komponenten kommunizieren durch **Ereignisse** (ggf. mit Daten) über **Publish/Subscribe**. Die Middleware ordnet Ereignisse zu und gibt sie weiter. | **Lockere Kopplung** (Hauptvorteil) | ROS |
| **4. Datenzentriert** | Komponenten kommunizieren über einen **gemeinsamen Datenspeicher** (passiv oder aktiv) | Datenspeicher als Kommunikationsmedium | Netzwerkanwendungen auf verteilten Dateisystemen |

**Shared Data Spaces** = Kombination aus ereignisbasiert + datenzentriert → **zeitliche Entkopplung** (Sender und Empfänger müssen nicht gleichzeitig aktiv sein).

> **Merke (Prüfungsfrage „Nenne zwei Architekturstile und ihre Eigenschaften“):** Nimm die zwei, die du am besten erklären kannst, z. B. *Schichten* (nur Aufruf der Schicht darunter, Anfragen runter, Antworten rauf) und *ereignisbasiert* (Publish/Subscribe, lockere Kopplung, Middleware verteilt Ereignisse).

### 2.2 Systemarchitekturen

Nach der Softwarearchitektur sind noch folgende Entscheidungen offen:

- Welche Softwarekomponenten werden konkret benötigt?
- Wie sollen sie interagieren?
- Wo werden sie **physisch platziert**?

Organisationsformen: **zentralisiert**, **dezentralisiert**, **hybrid**.

#### 2.2.1 Zentralisierte Architekturen: das Client-Server-Modell `★★★`

> **Rollenmodell:** Das **Client-Server-Modell** beherrscht die Komplexität verteilter Systeme durch Aufteilung der Prozesse in zwei Gruppen:
> 1. **Server** bieten bestimmte Dienste an (z. B. Dateisystem, Datenbank).
> 2. **Clients** fordern Dienste durch eine **Anfrage** an und **warten auf die Antwort** (Anfrage-Antwort-Verhalten).

```
 Client                         Server
   |  ---- Anfrage ------------>  |
   |       (wartet)               |  verarbeitet
   |  <---- Antwort ------------  |
```

**Verbindungslos vs. verbindungsorientiert:**

| | Verbindungslose Protokolle | Verbindungsorientierte Protokolle |
|---|---|---|
| Einsatz | zuverlässige Netzwerke (**LANs**) | unsichere Netzwerke (**WANs**), Internet nutzt **TCP** |
| Vorteile | geringer Overhead, schnell | Mehrfachnutzung der Verbindung, Kompression |
| Nachteile | Zusatzaufwand bei Verlust/Beschädigung von Nachrichten | Overhead durch Verbindungsaufbau |

**Rollen überlagern sich:** In komplexen Systemen kann eine Komponente zugleich **Server und Client** sein (z. B. Suchmaschine: Webserver ist Client der Index-/Datenbankserver).

#### Drei-Schichten-Architektur für (interaktive) Anwendungen `★★★`

Dies ist die in Übung 5 genannte „Schichtenarchitektur für interaktive Anwendungen“:

```
+----------------+      +-------------------+      +----------------+
| 1. Nutzer-     | ---> | 2. Verarbeitung   | ---> | 3. Daten-      |
|    schnittstelle| <--- |    (Kernlogik)    | <--- |    haltung     |
|  meist Client  |      | meist Server+Client|     |  meist Server  |
+----------------+      +-------------------+      +----------------+
```

| Schicht | Aufgabe | Rolle |
|---|---|---|
| **1. Nutzerschnittstelle** | Dateneingabe und -ausgabe (textuell, grafisch); kann schon lokale Verarbeitung enthalten | meist **Client** |
| **2. Verarbeitung** | Kernfunktionalität der Anwendung; wenig standardisiert, abhängig von der Anwendung | meist **Server & Client** |
| **3. Datenhaltung** | Verwaltung der eigentlichen Daten (Datenbank, Dateisystem), liefert persistente Informationen für die Verarbeitung | meist **Server** |

*Beispiel Internetsuchmaschine:* Nutzerschnittstelle = Eingabeformular/Ergebnisseite, Verarbeitung = Anfrageanalyse und Ranking, Datenhaltung = Index/Dokumentdatenbank.

**Thin vs. Fat Clients** (Folientitel „Fine Clients“, gemeint sind Thin Clients). Die Verteilung der Schichten auf Client und Server ist ein Spektrum:

| Variante | Was macht der Client? |
|---|---|
| (a) | Teile der Nutzerschnittstelle; die Anwendung (Server) kann sie steuern |
| (b) | komplettes grafisches Frontend, aber **keine** Verarbeitung |
| (c) | zusätzlich z. B. **Überprüfung von Nutzereingaben** |
| (d) | komplette grafische Anwendung, kommuniziert direkt mit der Datenbank |
| (e) | wie (d), speichert zusätzlich **Daten lokal** |

(a)–(b) = „dünner“ Client, (d)–(e) = „dicker“ (Fat) Client.

#### 2.2.2 Dezentralisierte Architekturen `★★★`

**Vertikale vs. horizontale Verteilung:**

| | **Vertikale Verteilung** | **Horizontale Verteilung** |
|---|---|---|
| Was wird verteilt? | **logische Komponenten/Schichten** auf verschiedene Computer | **Clients und Server selbst** werden verteilt |
| Aufteilung | nach **Funktion** (Schichten) | in **logisch äquivalente Teile** |
| Folge | **Spezialisierung** der Computer | jeder Teil arbeitet auf **eigenem Datenausschnitt** → **Lastverteilung** |
| Architektur | klassische **Drei-Schichten-Architektur** (zentralisiert) | **dezentralisierte** Architektur, z. B. **Peer-to-Peer** |
| Beispiel | UI-Rechner ↔ Anwendungsserver ↔ Datenbankserver | Webserver-Cluster mit Lastverteiler, P2P-Netz, DHT |

> **Eselsbrücke:** *Vertikal* = übereinander (Schichten auf verschiedene Rechner), *horizontal* = nebeneinander (gleichartige Rechner teilen sich die Arbeit).

**Peer-to-Peer (P2P):**

- Aufteilung in **gleichberechtigte Prozesse (Peers)**, die gleichzeitig **Client und Server** sind → **symmetrische Interaktion**.
- Kommunikation über **Overlay-Netzwerke**: Nachrichten werden weitergeleitet.
  - **Strukturierte** Netze: z. B. Routing-Tabellen
  - **Unstrukturierte** Netze: z. B. Flooding oder Suchen

**Strukturiertes P2P: Verteilte Hashtabelle (DHT)**

- Einsatz: dynamische Datenspeicherung verteilt über Peers.
- Overlay wird durch ein **deterministisches Verfahren** aufgebaut.
- Datenobjekte **und** Knoten erhalten **Schlüssel aus großem Bereich (z. B. 160 Bit)**. Ziel: effiziente, eindeutige Abbildung *Daten-Schlüssel → Knoten-Schlüssel*.
- Eine **Anfrage** entspricht **Routing zum zuständigen Knoten**.
- Herausforderungen: dynamisches Hinzufügen von Daten, dynamisches Hinzufügen/Entfernen von Knoten, Datenmengen größer als die Kapazität eines Knotens.
- *Normale Hashtabelle:* Schlüssel → Wert im lokalen Speicher. *Verteilte:* Schlüssel → zuständiger **Knoten**, der den Wert hält.

**Unstrukturiertes P2P:**

- Overlay durch **zufällige Algorithmen**; jeder Knoten führt eine **zufällig gebildete Nachbarschaftsliste** (Teilsicht).
- Daten werden **zufällig** auf Knoten verteilt; Suche meist per **Flooding** (Nachbarn fragen).
- **Mitgliedschaftsmanagement:** Einstieg über bekannte Einstiegspunkte; Verlassen jederzeit ohne Abmeldung → nicht antwortende Nachbarn fliegen automatisch aus der Liste.
- Herausforderungen: **isolierte Gruppen** verhindern, **Lastungleichgewicht**, Methoden zum Verwerfen alter Einträge beeinflussen die Netzwerkbalance.

**Superpeers:** Skalierbarkeit unstrukturierter P2P ist beschränkt → **Aufgabe der Symmetrie** durch Spezialknoten (speichern Indizes oder fungieren als Broker). Neues Problem: *Wer darf Superpeer sein?* → **Leader-Election-Problem** (siehe [Wahlalgorithmen](#54-wahlalgorithmen-)).

#### 2.2.3 Hybride Architekturen `★★`

Kombination verschiedener Architektureigenschaften in der Praxis, z. B. **Edge-Server-Systeme**: Server am **Rand von (Sub-)Netzwerken**, Clients verbinden sich mit dem Edge-Server ihres Netzes. Beispiel: **Internet Service Provider (ISP)**.

### 2.3 Middleware `★★★`

> **Definition:** Eine **Middleware** ist eine **Schicht zwischen Anwendung und verteilter Plattform**. Ziel: **Verteilungstransparenz**, d. h. Daten, Verarbeitung und Kontrolle werden vor der Anwendung verborgen.

**Architekturstile von Middlewares:**

| Stil | Beispiel |
|---|---|
| objektbasiert | **CORBA** (Common Object Request Broker Architecture) |
| eventbasiert | **ROS** (Robot Operating System) |

**Vor-/Nachteile spezifischer Stile:** Vorteil: Vereinfachung der Anwendungsentwicklung. Nachteil: Einschränkungen, fehlende Flexibilität (Beispiel CORBA: zunächst nur Remote-Objektaufrufe, später um Nachrichtenübermittlung erweitert).

**Demo Producer/Consumer (ROS, Publish/Subscribe):**

- Der **Producer** (Publisher) veröffentlicht Nachrichten (`String`) auf dem **Topic `chatter`** (1 Hz).
- Der **Consumer** (Subscriber) abonniert `chatter`; bei jeder Nachricht wird ein **Callback** aufgerufen.
- Beide kennen sich **nicht direkt**, sie kennen nur das Topic → lockere Kopplung (ereignisbasierter Stil).
- *Achtung:* Die Folie nutzt **ROS 1** (`rospy`), Übung 2 nutzt **ROS 2** (`rclpy`). Das Konzept ist gleich, die API unterscheidet sich (siehe [9.2](#92-übung-2--ros-2-publishsubscribe)).

**Anpassung von Middleware-Verhalten:**

| Art | Anpassung durch |
|---|---|
| **statisch** | **Daten**: Parameter, Spezifikationen |
| **dynamisch** | **Code**: Interceptoren, Callbacks |

**Adaptive Software:** Die Umgebung ändert sich ständig → Adaption soll die **Middleware** übernehmen, nicht die Anwendung. **Interceptoren** (fangen Aufrufe ab und erweitern sie) sind ein Mechanismus dafür. Techniken:

| Technik | Idee | Schwierigkeit |
|---|---|---|
| **Separation of Concerns** | Trennung der Verantwortlichkeiten, modulare Software | nicht-funktionale Anforderungen (Sicherheit, Performance, Zuverlässigkeit) lassen sich schlecht trennen |
| **Computational Reflection** | Programme inspizieren sich selbst und ändern ihr Verhalten **zur Laufzeit** | nicht von jeder Sprache unterstützt |
| **Komponentenbasierte Architektur** | gezielte (statische/dynamische) Komposition von Einzelkomponenten | erfordert **Late Binding** (Nachladen von Modulen) |

**Selbstmanagement:** Verteilte Systeme müssen auf Umgebungsänderungen reagieren, Ausführungsverhalten und -verteilung passen sich selbstständig an. Modell: **Regelkreis (Feedback Control Model)**: Messen → Vergleichen mit Soll → Anpassen.

---

## 3. Prozesse

*(Vorlesung 3 · Übung 3, Übung 5)*

**Betriebssystemsicht:** Prozess = Programm in Ausführung; Herausforderungen sind Verwaltung und Scheduling.
**Verteilte Systeme** ergänzen:

| Thema | Zweck |
|---|---|
| **Threads** | Überlagerung von Kommunikation und lokaler Verarbeitung |
| **Virtualisierung** | Portabilität und Fehlerisolierung |
| **Clients** | Nutzerschnittstellen und Verteilungstransparenz |
| **Server** | generelle Implementierungsaspekte |
| **Migration** | von Prozessen bzw. Code |

### 3.1 Threads `★★★`

**Prozess vs. Thread:**

| | **Prozess** | **Thread** |
|---|---|---|
| Zustand | **vollständig**: CPU-Kontext, Speicher, Ressourcen … | **minimal**: nur CPU-Kontext |
| Isolation | **voneinander isoliert** | mehrere Threads **innerhalb eines Prozesses** |
| Kommunikation | aufwändig → **Interprozesskommunikation (IPC)** | über **gemeinsamen Speicher** → **Synchronisation notwendig** |
| Granularität | grob → **hoher Overhead** | fein → **hohe Performance** |

**Vorteile von Threads in normalen (nicht-verteilten) Systemen:**

1. **Überbrückung blockierender Operationen:** GUI und Verarbeitung trennen, blockierende Systemaufrufe überlagern.
2. **Nutzung mehrerer CPUs/Kerne:** rechenintensive Operationen aufteilen, parallele Ausführung.
3. **Aufteilung „großer“ Anwendungen:** kooperierende Programmteile als Threads statt Prozesse mit IPC.
4. **Strukturierung:** unabhängige Aufgaben getrennt ausführen.

#### Threads in verteilten Systemen `★★★`

Kernnutzen: **blockierende Systemaufrufe nutzen, ohne den Prozess zu blockieren**, und **mehrere logische Verbindungen** verwalten.

**Multi-threaded Clients:**

- Verteilte Systeme müssen **lange Nachrichtenlaufzeiten verbergen** (hunderte ms bis Sekunden).
- Ansatz: Kommunikation starten und mit anderen Aufgaben fortfahren.
- **Beispiel Webbrowser:** Seite laden und anzeigen, während Bilder usw. **parallel über separate Verbindungen** nachgeladen werden.
  - Nutzer können mit der Seite interagieren, während andere Inhalte laden.
  - Lastverteilung auf **replizierte Webserver** durch parallele Verbindungen.

**Multi-threaded Server (Hauptnutzung von Multithreading):**

- Vereinfacht die Server-Implementierung und nutzt Parallelisierung für Performance.
- Server sollen **mehrere Anfragen** verarbeiten und auf **lokale Ressourcen warten** können.

| Beispiel Dateiserver | Eigenschaften |
|---|---|
| **Single-threaded:** Hauptschleife arbeitet Anfragen **sequentiell** ab | − hohe Wartezeiten bei konkurrierenden Anfragen; − CPU **inaktiv** während Festplattenzugriffen |
| **Multi-threaded:** **Dispatcher-Thread** verteilt Anfragen an **Worker-Threads** | + parallele Abarbeitung; + CPU **aktiv genutzt**, während andere Threads auf die Platte warten |

```
          +------------+        +-----------+
Anfragen->| Dispatcher |------->| Worker 1  |--> Datei lesen (blockiert nur diesen Thread)
          |  (Thread)  |------->| Worker 2  |--> Datei lesen
          +------------+------->| Worker 3  |--> antwortet bereits
                                +-----------+
```

> **Prüfungsantwort „Einsatz von Threads in verteilten Systemen“:** (1) Clients: Latenzen verbergen, parallele Verbindungen (Browser). (2) Server: mehrere Anfragen gleichzeitig (Dispatcher/Worker), CPU wird während Wartezeiten genutzt. (3) Vorteil gegenüber Prozessen: weniger Overhead, gemeinsamer Speicher (aber Synchronisation nötig).

### 3.2 Virtualisierung `★★`

- Prozesse/Threads ermöglichen die gemeinsame Nutzung **einer CPU**. **Virtualisierung** erweitert das Konzept auf **andere Ressourcen**.
- Programmausführung (a) **direkt** auf System A, (b) **virtualisiert** in System A auf System B.

**Entwicklung:**

- *Früh:* Unterstützung von **Legacy-Software** auf teuren Mainframes (später weniger relevant durch billige Hardware).
- *Ab den 1990ern:* Legacy-Unterstützung auf neuen Plattformen; **Vielfalt von Netzwerken/Servern** → heterogene Systeme einfacher verwaltbar, da Anwendungen in **eigenen VM-Umgebungen** laufen; **Portabilität & Flexibilität**: komplette Systeme (inkl. Anwendung und Betriebssystem) lassen sich replizieren/migrieren (z. B. für **CDNs**).

**Prinzip:** Virtualisierung = **Nachahmung von Schnittstellen**. Ein Computersystem hat **vier Schnittstellen**:

| # | Schnittstelle | zwischen |
|---|---|---|
| 1 | **Bibliotheksfunktionen (APIs)** | Anwendungen ↔ Bibliotheken |
| 2 | **Systemaufrufe** | Bibliotheken ↔ Betriebssystem |
| 3 | **Privilegierte Instruktionen** | Betriebssystem ↔ Hardware |
| 4 | **Allgemeine Instruktionen** | Anwendung ↔ Hardware |

**Drei Arten der Virtualisierung:**

| Art | Idee | Beispiele |
|---|---|---|
| **Process Virtual Machine** | Laufzeitsystem führt Anwendungen mit **abstrahierten Instruktionen** aus (interpretiert oder emuliert) | Java Runtime (**Interpretation**), Windows-Anwendungen unter Linux (**Emulation**) |
| **Virtual Machine Monitor (VMM)** | Schicht, die die **Hardware komplett abschirmt**; mehrere **unterschiedliche Betriebssysteme** möglich | VMware vSphere, Microsoft Hyper-V, **Linux KVM** |
| **Containerization** | Vorhandenes **Betriebssystem** wird als **isolierte Ausführungsumgebung (Container)** bereitgestellt. + hohe Performance (Maschineninstruktionen direkt), + geringer Overhead (OS wiederverwendet) | **Docker**, **Kubernetes** |

### 3.3 Client-Realisierungen `★★`

- **Hauptaufgabe:** Nutzerschnittstelle zur Interaktion mit einem Server.
- **Anwendungsspezifisches Protokoll:** z. B. Terminplaner via Kalender-Server.
- **Anwendungsunabhängiges Protokoll:** z. B. **X Window System**, Smartphone-Apps.

**Client-seitige Unterstützung für Verteilungstransparenz:**

| Transparenz | Umsetzung im Client / in der Middleware |
|---|---|
| **Zugriff** | **Client-Stubs** (Platzhalter) der Server-Schnittstellen verbergen Kommunikation und Server-Unterschiede |
| **Verortung / Ortsveränderung** | **ortsunabhängige Namen/Adressen**; Server-Ort und Umzug bleiben in der Middleware verborgen |
| **Replikation** | Anfragen an **replizierte Server** weiterleiten; mehrere Antworten zu **einer** Antwort reduzieren |
| **Störung** | Kommunikationsstörungen **maskieren**, z. B. durch **wiederholte Verbindungsaufnahme** oder **Caching** |

### 3.4 Server-Realisierungen `★★★`

**Generelle Ablaufschleife eines Servers:**

1. Warte auf eingehende Anfrage von Clients
2. Bearbeite die Anfrage und sende die Antwort
3. Setze das Warten fort

**Iterativer vs. nebenläufiger Server:**

| | **Iterativer Server** | **Nebenläufiger Server** |
|---|---|---|
| Behandlung | Anfragen werden **vom Server selbst** behandelt | Anfragen werden an **separate Threads/Prozesse** weitergegeben |
| Folge | ein Client nach dem anderen | Server kann **sofort** auf weitere Anfragen warten |
| Antwort | vom Server | vom **verantwortlichen Thread/Prozess** |
| Varianten | – | **Multithreaded Server** (neuer oder vorhandener Thread), **Fork-Server** (UNIX/Linux, neuer Prozess per `fork`) |

*Demo (Python, Port 12345, `common.py` + drei Server-Varianten):* `iterative.py` (`accept()` → `handle_client()` nacheinander), `concurrent_threads.py` (pro Verbindung ein `Thread`), `concurrent_fork.py` (pro Verbindung `os.fork()`; Kindprozess schließt die Server-Socket-Kopie, Elternprozess schließt die Client-Verbindung). Ausprobieren unter Linux siehe [9.5](#95-vorlesungsdemos-unter-linux).

**Server-Kontaktpunkte:**

- Server „hört“ (`listen`) an einem **Kontaktpunkt (Endpoint/Port)**. Clients adressieren *Server-Adresse + Kontaktpunkt*.
- **Adresse:** fest (z. B. Nameserver 1.1.1.1 / 8.8.8.8) oder dynamisch (**DNS**).
- **Kontaktpunkt:** **statisch** (HTTP → TCP 80, HTTPS → TCP 443, SSH → TCP 22, DNS → UDP 53) oder **dynamisch** (via **Endpoint-Daemon** oder **Superserver**).

| | Statische Kontaktpunkte | Dynamische Kontaktpunkte |
|---|---|---|
| + | direkt nutzbar → effizient, schnell | flexibel für beliebige Dienste |
| − | begrenzte Anzahl, Standardisierung nötig | nur indirekt nutzbar → höhere Antwortzeit |

- **Endpoint-Daemon:** separater Server mit **festem Port** und **Verzeichnis** der Kontaktpunkte. Server registrieren sich, Clients fragen nach. − Jeder Server muss separat implementiert und ausgeführt werden.
- **Superserver:** hört an **mehreren Kontaktpunkten** und **startet** den passenden Server erst bei eintreffender Anfrage (z. B. **inetd** unter UNIX/Linux). + Nur **ein** Server wartet → ressourceneffizient.

#### Server und Zustände `★★★`

| | **Zustandsloser Server (stateless)** | **Zustandsbehafteter Server (stateful)** |
|---|---|---|
| Informationen über Clients | **keine** gespeichert | **persistent** gespeichert; müssen **explizit gelöscht** werden |
| Zustandsverlust | stört den Dienst **nicht** | nach Absturz muss der Zustand **wiederhergestellt** werden |
| Eigener Zustand | ändert sich **unabhängig**, ohne Clients zu informieren | – |
| Vorteil | einfach, robust | **Performance** |
| Sonderfall | **Soft State**: Zustand nur **zeitlich begrenzt** gehalten | – |
| Beispiel | **Webserver** (beantwortet HTTP-Anfrage und vergisst den Client; Inhalte ändern sich ohne Info an Clients) | **Dateiserver**, der speichert, welcher Client eine Datei gerade liest/schreibt (schnellere Lese-/Schreiboperationen; nach Absturz muss ermittelt werden, welcher Client den aktuellen Stand hat) |

> **Merke:** Zustandslos = einfach & ausfallsicher, zustandsbehaftet = schneller, aber Wiederherstellungsaufwand. Der Webserver darf Log-Daten führen und bleibt trotzdem „zustandslos“ bzgl. Clients.

**Server-Cluster:** Menge von Computern im Netz, jeder führt einen oder mehrere Server aus.

*Dreistufiger Cluster:*

```
Clients -> [1. Switch (Routing der Anfragen)]
              -> [2. Anwendungs-/Rechenserver]
                    -> [3. Datenverarbeitungsserver (Datei-/DB-Server)]
```

- **Management:** einfach = Admins loggen sich auf einzelnen Knoten ein; fortgeschritten = zentrale Verwaltungsoberflächen. Für **sehr große Cluster** (Tausende Knoten) ungeeignet, weil mit der Knotenzahl die Fehlerwahrscheinlichkeit steigt.
- **Rechenbeispiel:** N = 1000 Server, Fehlerrate p = 0,1 % →
  P(kein Server fällt aus) = (1 − p)<sup>N</sup> = 0,999<sup>1000</sup> ≈ **36,8 %** → in ca. **63 %** der Zeit ist mindestens ein Server ausgefallen.
- **Heutige Realität:** Automatisierung, **Container-Orchestrierung**, serverlose Architekturen, **Self-healing** (autonome Fehlererkennung und Reparatur), Hybrid-/Multi-Cloud, Fernverwaltung.

### 3.5 Code-Migration `★★`

> **Code-Migration** = Verschieben von Programmen, z. T. **während der Ausführung**.

**Gründe:**

1. **Leistung:** Prozesse von stark auf weniger ausgelastete Maschinen verschieben.
2. **Weniger Kommunikation:** Code zu den **Daten** bringen (Client → Server oder umgekehrt).
3. **Flexibilität:** Software bei Bedarf zum Client laden (statt vorab installieren); dynamische Konfiguration zur Laufzeit.

**Herausforderungen:** **Sicherheit** (Vertrauen in dynamisch geladenen Code), standardisierte Protokolle für Download und Ausführung.

**Modelle:**

| | Bedeutung |
|---|---|
| **Schwache Mobilität** | nur **Code + ggf. Initialisierungsdaten**; Programm startet von **vordefinierten Startpunkten** |
| **Starke Mobilität** | zusätzlich **Ausführungssegment** (Instruktionszeiger, Stack): laufender Prozess wird gestoppt, verschoben, **fortgesetzt** |
| **Sender-initiiert** | der Rechner, der den Code hat, startet die Migration (z. B. Upload zu einem Rechenserver) |
| **Empfänger-initiiert** | der Rechner, der den Code will, startet sie (z. B. Download von Java-Applets) |

**Weitere Herausforderungen:**

- **Ressourcenzugriff:** Code und Daten lassen sich meist unverändert migrieren, aber die **Ressourcennutzung** (Netzwerkports, Dateizugriffe) muss angepasst werden.
- **Heterogene Systeme:** Lösung per **VM** (z. B. JVM) oder Migration ganzer **Ausführungsumgebungen** (Prozesseigenschaften und Ressourcenbindungen bleiben erhalten).
- **Betriebssystemumgebungen:** Virtualisierung per VMM, z. B. **Live-Migration** von VMs in einem VMware-Cluster.

---

## 4. Kommunikation

*(Vorlesung 4 · Übung 2, Übung 4, Übung 5)*

Verteilte Systeme brauchen **Interprozesskommunikation (IPC)**. Sie läuft als primitiver **Nachrichtenaustausch über das Netzwerk**.

**Herausforderungen:** tausende bis Millionen Prozesse; unzuverlässige Netzwerke (z. B. Internet).
**Lösungsansätze:** **Protokolle** (Regeln) und **Kommunikationsmodelle** als Ersatz für primitiven Nachrichtenaustausch:

| Modell | Kurzbeschreibung |
|---|---|
| **RPC** (Remote Procedure Call) | entfernter Prozeduraufruf |
| **MOM** (Message-Oriented Middleware) | nachrichtenorientiert, Warteschlangen |
| **Datenströme** (Streaming) | zeitkritische, kontinuierliche Daten |
| **Multicasting** | ein Sender, mehrere Empfänger |

### 4.1 Protokolle `★★★`

**Welche Aspekte regelt ein Protokoll?** Beispiele: Spannung für 0-/1-Bit, Erkennen des letzten Bits einer Nachricht, Erkennen beschädigter/verlorener Nachrichten, Format von Zahlen/Strings/Datenelementen.

> **Definition: Protokoll** = standardisierte Menge von Regeln, die festlegt, wie Daten zwischen Rechnern oder Prozessen **ausgetauscht, formatiert und verarbeitet** werden.

- **Verbindungsorientiert:** Sender und Empfänger **arrangieren eine Verbindung**, bevor Daten übertragen werden.
- **Verbindungslos:** Sender überträgt, **sobald er bereit ist**.

**ISO/OSI-Referenzmodell:** standardisierte Ebenen und Verantwortungen, Schnittstellen mit Operationen zwischen den Schichten. Ablauf bei Prozess A → B: Anwendungsschicht fügt **Header** hinzu und reicht an die Darstellungsschicht … bis zur Bitübertragung; beim Empfänger analysiert jede Schicht ihren Header und gibt den Inhalt **nach oben** weiter.

| Schicht | Verantwortung | Beispiele |
|---|---|---|
| **7 Anwendung** | konkrete Anwendungen | HTTP, FTP |
| **6 Darstellung** | Bedeutung der Bits (Datenformate) | |
| **5 Sitzung** | verbesserte Transportschicht | |
| **4 Transport** | **Paketierung** (Reihenfolge), **Integrität** (Vollständigkeit) | **TCP, UDP** |
| **3 Vermittlung** | Wegfindung/**Routing** | **IP** |
| **2 Sicherung** | **Frames**, Fehlererkennung durch Prüfsummen | |
| **1 Bitübertragung** | Übertragung der Bits | |

Schichten 1–3 = *Lower-level*, 5–7 = *Higher-level*, 4 = Transport.

**Middleware-Protokolle:** Middleware sitzt (hauptsächlich) in der **Anwendungsschicht** und stellt **allgemeine Dienste** über eigene Protokolle bereit (Authentifizierung, Autorisierung, Transaktionen, Locks) → angepasstes Schichtenmodell **mit Middleware-Schicht**.

#### Arten von Kommunikation `★★★`

Drei Achsen, jeweils mit zwei Ausprägungen:

| Achse | Variante A | Variante B |
|---|---|---|
| **Speicherung** | **Persistent:** Kommunikationssystem speichert Nachrichten **so lange wie nötig** → Sender kann vorzeitig **beendet** werden | **Transient:** speichert nur, **solange Sender und Empfänger ausgeführt werden** → keiner darf vorzeitig enden |
| **Synchronisation** | **Asynchron:** Sender **fährt fort**, das Kommunikationssystem speichert die Nachricht | **Synchron:** Sender **blockiert**; verschiedene Synchronisationspunkte möglich |
| **Struktur** | **Diskret:** jede Nachricht ist eine **vollständige Informationseinheit** | **Streaming:** mehrere **kontinuierliche Nachrichten gehören zusammen** |

> **Typische Kombinationen:** E-Mail = persistent + asynchron. RPC = (meist) transient + synchron. Audio-Stream = transient + Streaming.

### 4.2 Remote Procedure Call (RPC) `★★★`

**Problem:** Expliziter Nachrichtenaustausch verhindert **Zugriffstransparenz**.
**Grundidee:** Ein Prozess auf Maschine A ruft eine Prozedur auf Maschine B auf. A wird **angehalten**, solange B die Prozedur ausführt. Parameter gehen vom **Caller** zum **Callee**, Ergebnisse zurück.

**Herausforderungen:**

- **Verschiedene Adressräume** (Hauptspeicher) der Maschinen
- Parameter und Ergebnisse müssen ausgetauscht werden → **unterschiedliche Datenformate**
- **Beide Seiten können ausfallen**

**Lokaler Prozeduraufruf (zum Vergleich), z. B. `count = read(fd, buf, nbytes)`:**
Parameter und **Rücksprungadresse** auf den **Stack** → Sprung zur Prozedur → Parameter vom Stack lesen → Ergebnis in Register/Stack → Rücksprung zur Rücksprungadresse.

**Client-Stub und Server-Stub:**

- **Client-Stub:** **Platzhalterprozedur** auf Client-Seite mit **gleicher Schnittstelle** wie die Originalprozedur; verpackt Parameter und sendet sie an den Server.
- **Server-Stub:** entpackt Parameter, ruft die Originalprozedur auf und sendet das Ergebnis zurück.
- Für Client und Server sieht es aus wie ein **regulärer lokaler Aufruf**.

**Gesamtablauf (10 Schritte) `★★★`:**

```
 Client-Prozess   Client-Stub   Client-OS        Server-OS   Server-Stub   Server
      |  1 Aufruf     |             |                |            |           |
      |-------------->| 2 packt     |                |            |           |
      |               |  (Marshaling)                |            |           |
      |               |------------>| 3 sendet ----->| 4 liefert  |           |
      |               |             |   (Netzwerk)   |----------->| 5 packt   |
      |               |             |                |            |  aus, ruft|
      |               |             |                |            |---------->|
      |               |             |                |            | 6 Ergebnis|
      |               |             |                |            |<----------|
      |               |             |<----- 8 -------| 7 packt    |           |
      |               |<------------| 9 liefert      |   ein      |           |
      |<--------------| 10 packt    |                |            |           |
      |  Ergebnis     |    aus      |                |            |           |
```

In Worten: 1. Client ruft Client-Stub. 2. Stub baut Nachricht, ruft OS. 3. OS des Clients sendet an OS des Servers. 4. OS des Servers übergibt an Server-Stub. 5. Server-Stub packt Parameter aus, ruft Server. 6. Server arbeitet, gibt Ergebnis an Stub. 7. Stub packt Ergebnis in Nachricht, ruft OS. 8. OS des Servers sendet an OS des Clients. 9. OS des Clients übergibt an Client-Stub. 10. Stub packt aus und gibt das Ergebnis an den Client.

**Übergabe von Werte-Parametern:**

- Parameter in eine **Nachricht verpacken** = **Parameter Marshaling**, plus **Prozedurname** (damit der Server die Prozedur auswählen kann). Aufbau der Nachricht legt das **RPC-Protokoll** fest. Beispiel `k = add(i, j)`: Nachricht enthält „add“, i, j.
- **Hauptproblem: Heterogenität:**
  - unterschiedliche **Datentypen** (Bitgrößen/-formate von Integer, Float)
  - **Bitreihenfolge (Endianness):** Little vs. Big Endian
  - unterschiedliche **Zeichensätze** (ASCII vs. UTF)
  - unterschiedliche **Programmumgebungen** (Python-Client vs. C-Server)
  - **Lösung:** plattformunabhängige Formate, **Datenserialisierung**

**Übergabe von Referenz-Parametern:**

- **Grundproblem:** Pointer sind nur im **Adressraum ihres Prozesses** gültig. Man kann den Wert verschicken, aber am Ziel nicht auswerten.
- **Lösungsansätze:** Referenzen/Pointer **verbieten** (nicht immer praktikabel); **referenzierte Werte explizit übertragen** (einfach für skalare Werte, Arrays, Strukturen; **nicht** für komplexe Strukturen wie verkettete Listen); Parameter als **Input (konstant)** oder **Output (veränderlich)** markieren, um unnötige Übertragung zu vermeiden.

**Automatische Stub-Generierung:** Es werden zwei Informationen benötigt:

1. **RPC-Protokoll:** Nachrichtenformat und -verarbeitung, Verbindungsdetails (Anordnung der Parameter, Darstellung einfacher Datentypen, Netzwerkkommunikation).
2. **Schnittstellendefinition** per **Interface Definition Language (IDL):** Prozedurnamen, Parameter und Ergebnisse inkl. **Datentypen**.

**Beispiel gRPC (Google RPC):**

| Merkmal | Inhalt |
|---|---|
| Framework | Open Source (Google), auf **hohe Leistung** ausgelegt |
| Transport | **HTTP/2** |
| IDL & Serialisierung | **Protocol Buffers** (plattformunabhängig) |
| Kommunikation | **bidirektional, Vollduplex**; asynchrones **Streaming** |
| Effizienz | Header-Komprimierung, effiziente Serialisierung |
| Sprachen | viele |

*Demo (`hello.proto`):*

```proto
syntax = "proto3";
service Greeter { rpc SayHello (HelloRequest) returns (HelloReply) {} }
message HelloRequest { string name = 1; }
message HelloReply   { string message = 1; }
```

Stub-Generierung (`protoc`), dann **Server** (`Greeter`-Klasse, `grpc.server(ThreadPoolExecutor)`, `add_insecure_port("[::]:50051")`) und **Client** (`insecure_channel` → `GreeterStub` → `stub.SayHello(...)`). Praxis in [9.4](#94-übung-4--grpc-python--c).

**Synchroner vs. asynchroner RPC:** Beim **synchronen** RPC wartet der Client auf das Ergebnis. Beim **asynchronen** RPC macht er weiter. Wie erhält er das Ergebnis?

- **Client pollt** den Server (wiederholtes, aktives Abfragen), oder
- **Server unterbricht** den Client (RPC von Server zu Client / Callback).

### 4.3 Nachrichtenorientierte Kommunikation `★★★`

**Motivation:** RPC & Co. verbergen die Kommunikation (Zugriffstransparenz), haben aber Nachteile: (meist) **synchron**, Client **blockiert**, die Empfängerseite muss **aktiv** sein.
**Alternative:** nachrichtenorientierte Kommunikation = **Offenlegung der Kommunikation**, **Verzicht auf Zugriffstransparenz**.

#### Transiente nachrichtenorientierte Kommunikation

Nachrichten werden nur gespeichert, **solange die Partner laufen** → Sender und Empfänger müssen **gleichzeitig** ausgeführt werden.

- **Berkeley Sockets:** standardisierte Schnittstelle zur **Transportschicht**.
- **Message Passing Interface (MPI):** Standard für **High Performance Computing**:
  - **Punkt-zu-Punkt:** `Send`, `Receive`
  - **Kollektiv:** `Broadcast`, `Reduce`, `Gather` …
  - **Einseitig:** `Put`, `Get`
  - *Demo:* π-Berechnung: jeder Rang summiert seinen Anteil, `comm.reduce(..., op=SUM, root=0)` sammelt das Ergebnis bei Rang 0.

#### Persistente nachrichtenorientierte Kommunikation: Nachrichtenwarteschlangen

- Nachrichten werden **so lange wie nötig** gespeichert → Sender und Empfänger müssen **nicht gleichzeitig** laufen.
- **Kernidee:** Nachrichten in **Warteschlangen** speichern und weiterleiten, auch wenn Sender oder Empfänger inaktiv sind → **zeitliche Entkopplung**.
- **Beispiele:** E-Mail, Apache Kafka, JMS, AMQP, RabbitMQ, ZeroMQ, **ROS**.

**Eigenschaften:**

| Aspekt | Inhalt |
|---|---|
| **Modell** | meist **eigene private Warteschlange** je Anwendung; Adressierung über **eindeutige Warteschlangennamen** |
| **Semantik** | **nur das Einfügen** in die Warteschlange wird garantiert; **Zeitpunkt oder Lesen** der Nachricht **nicht** |
| **Szenarien** | beide aktiv; nur Sender oder nur Empfänger aktiv; beide passiv (Nachrichten bleiben gespeichert) |

**Operationen:**

| Operation | Wirkung |
|---|---|
| **Put** | Nachricht **nicht-blockierend** einfügen |
| **Get** | **blockierend** Nachricht lesen |
| **Poll** | **nicht-blockierend** abfragen |
| **Notify** | **automatische Bearbeitung** durch registrierte Funktionen (Callback) |

**Architektur:** Anwendungen greifen **nur auf lokale Warteschlangen** zu. **Ausgangswarteschlange** nimmt zu versendende Nachrichten auf, **Zielwarteschlange** enthält empfangene. Die **Middleware** überträgt zwischen den Warteschlangen. **Warteschlangenmanager** interagieren direkt mit den Anwendungen, **Relays** sind Zwischenstationen für bessere Skalierung.

**Message Broker:** **spezialisierter Knoten**, der Nachrichten auf Anwendungsebene **zwischen Formaten übersetzt**. Hauptziel: **Integration** vielfältiger Anwendungen in ein verteiltes System; Konvertierung nötig, wenn sich Anwendungen nicht kennen.

**RPC vs. nachrichtenorientierte Kommunikation (Zusammenfassung):**

| | RPC | Nachrichtenwarteschlangen (MOM) |
|---|---|---|
| Transparenz | Zugriffstransparenz | Kommunikation **sichtbar** |
| Synchronisation | meist **synchron** (Client blockiert) | **asynchron** |
| Kopplung | **eng** (beide gleichzeitig aktiv) | **lose / zeitlich entkoppelt** |
| Speicherung | transient | **persistent** |

### 4.4 Datenströme `★★`

**Motivation:** Bisher: unabhängige Informationseinheiten, die **zeitunabhängig** korrekt sind. **Neu:** **zeitkritische** Kommunikation: Die Einhaltung genauer Zeitintervalle ist entscheidend.

*Beispiel Audio:* 16 Bit-Samples, 44 100 Hz, Stereo → 44 100 · 16 Bit · 2 = 1 411 200 Bit/s = **176,4 KB/s**. Wiedergabe braucht korrekte Reihenfolge und exakte Dauer (1/44 100 s pro Sample).

**Arten:**

| Art | Merkmal | Beispiele |
|---|---|---|
| **Diskret** | Übertragungszeitpunkt irrelevant für die Interpretation | UNIX-Pipes, TCP/IP-Verbindungen |
| **Kontinuierlich** | **zeitgenaue** Übertragung nötig | Audio, Video |
| **Komplex** | mehrere **zeitlich synchronisierte Unterströme** | Stereo-Audio, Audio+Video, Film mit Untertitel |

**Übertragungsmodi:** **asynchron** (keine zeitlichen Vorgaben, z. B. Dateiübertragung) · **synchron** (**maximale** End-to-End-Verzögerung garantiert) · **isochron** (**strikte** Einhaltung: minimale **und** maximale Verzögerung).

**Servicequalität (QoS):** IP ist nur **Best Effort**, Pakete können verworfen werden. Maßnahmen:

| Ebene | Maßnahmen |
|---|---|
| **Netzwerk** | Klassifizierung/Priorisierung (**DSCP**, Traffic Shaping, Network Slicing); **CDN** (Datenquelle näher zum Nutzer) |
| **Anwendung** | **Adaptive Bitrate Streaming (ABS)** (Qualität an Bandbreite anpassen); **Forward Error Correction (FEC)** (redundante Zusatzinfo); **Datenpufferung**; **verschachtelte Übertragung** |

- **Datenpufferung:** Pakete werden in einem Puffer gesammelt, bevor sie weitergegeben werden → **Laufzeitschwankungen (Jitter) werden ausgeglichen**; Preis: **Verzögerung am Anfang** des Stroms.
- **Verschachtelte Übertragung (Interleaving):** Übertragungsreihenfolge wird von der Abspielreihenfolge **entkoppelt** → bei Paketverlust entstehen **viele kleine statt einer großen Lücke** (zeitlich verteilt, leichter zu kaschieren); Preis: ebenfalls Anfangsverzögerung.

### 4.5 Multicasting `★★`

**Grundidee:** Kommunikation von **einem Sender an mehrere Empfänger**. Paarweise Kommunikation mit jedem Empfänger ist zu aufwändig.

| Ebene | Umsetzung |
|---|---|
| **Netzwerk** | Ethernet-/IP-Multicast in **LANs**; Multicast-Routing in Unternehmensnetzen; im Internet **nur eingeschränkt** (komplexe Verwaltung, fehlende ISP-Unterstützung) |
| **Anwendung** | **Peer-to-Peer / Overlay-Netzwerke** zum Aufbau von Kommunikationspfaden; **Publish/Subscribe** oder **Gossip-Protokolle** |

---

## 5. Synchronisation

*(Vorlesung 5 · Übung 5)*

**Motivation:** Verteilte Systeme ermöglichen Kooperation, und Kooperation braucht meist ein **abgestimmtes Vorgehen**. Beispiele: Einigung auf **Nachrichtenreihenfolgen** (→ relative zeitliche Synchronisation) und **zeitweise exklusiver Zugriff** auf verteilte Ressourcen (z. B. Drucker).

| Lösungsansatz | Einigung worauf? |
|---|---|
| **Uhrensynchronisation** | gemeinsame **reale** Zeit |
| **Logische Uhren** | **relativen** zeitlichen Ablauf |
| **Gegenseitiger Ausschluss** | **exklusiven** Zugriff |
| **Wahlalgorithmen** | einen **ausgewählten Prozess** (Koordinator) |

### 5.1 Uhrensynchronisation `★★★`

**Wozu synchronisierte Uhren?** Beispiele: **verteilter Dateizugriff** (verlässliche Zeitstempel, z. B. Änderungszeit bei inkrementeller Übersetzung), **Sicherheitsüberprüfungen** (zeitlich begrenzte Gültigkeit), **Finanzvermittlung/Börse** (zeitabhängige Kosten/Gewinne), **Sensornetze** (zeitabhängige Messwerte).

**Grundproblem:**

- *Zentralisiertes System:* eindeutige Uhrzeit per Systemaufruf. Wenn A vor B nach der Zeit fragt, gilt Zeit(A) ≤ Zeit(B).
- *Verteiltes System:* **jeder Teilnehmer hat seine eigene Uhrzeit** → **Einigung auf gemeinsame Uhrzeit** nötig.

**Physische Uhren in Computern:**

1. Chipsatz mit **Quarzoszillator** liefert den Basistakt (z. B. 100 MHz).
2. Die CPU nutzt ihn für einen programmierbaren **Hardware-Timer**.
3. Der Timer löst die Aktualisierung der **Systemzeit** im Betriebssystem aus.
4. Beim Booten wird die Systemzeit aus dem **batteriegestützten CMOS-RAM** gelesen.

**Zeitabweichungen:** Beim Einzelrechner unbedeutend (gleich für alle Prozesse). Im verteilten System hat **jedes System seine eigene Quarzuhr**, leichte Frequenzunterschiede führen zur **Zeitabweichung (Clock Skew)** → **inkonsistente Zeitstempel** für Dateien, Nachrichten, Prozesse.

**Globale Zeit: UTC (Universal Coordinated Time):**

- Sonnenzeit ist an die Umwelt angepasst, aber **nicht konstant** (Schwankungen der Erdrotation). Internationale **Atomzeit** ist stabil und genau.
- **UTC = präzise Atomzeit + Schaltsekunden** (Anpassung an die Sonnenzeit).
- **Verbreitung:** Stromnetze (50/60 Hz, bei Schaltsekunde kurz erhöht), Radiostationen (Kurzwelle), Satellitennavigation, **Zeitserver im Internet**.

#### NTP (Network Time Protocol) `★★★`

Synchronisiert viele Uhren (1) zu einer **Referenzzeit** (Atomuhr, UTC-Funkempfänger) oder (2) **untereinander**.

**Grundidee:** Client A kontaktiert Zeitserver B und ermittelt vier Zeiten:

```
 Client A                          Zeitserver B
    |                                   |
 T1 |---------- Anfrage --------------->| T2   (B empfängt)
    |                                   |
    |                                   |
 T4 |<--------- Antwort ----------------| T3   (B sendet)
    |
   T1 = A sendet (A-Uhr)     T2 = B empfängt (B-Uhr)
   T4 = A empfängt (A-Uhr)   T3 = B sendet   (B-Uhr)
```

**Formeln (auswendig!):**

$$t_{Delay} = \frac{(T_4 - T_1) - (T_3 - T_2)}{2} \qquad\qquad t_{Offset} = T_3 + t_{Delay} - T_4$$

Klartext (falls dein Viewer kein LaTeX darstellt):

```
tDelay  = ((T4 - T1) - (T3 - T2)) / 2     (einfache Laufzeit: Gesamtzeit minus Bearbeitungszeit beim Server, halbiert)
tOffset = T3 + tDelay - T4                (Serverzeit bei Ankunft beim Client minus Client-Zeit)
```

- Messung **wiederholen**; die Zeitdifferenz = tOffset **bei minimalem tDelay**.
- **tOffset < 0 ⇒ Uhr von A geht zu schnell. tOffset > 0 ⇒ Uhr von A geht zu langsam.**

**Rechenbeispiel (alle Werte in ms):** T1 = 0, T2 = 250, T3 = 260, T4 = 130.

```
tDelay  = ((130 - 0) - (260 - 250)) / 2 = (130 - 10) / 2 = 60 ms
tOffset = 260 + 60 - 130                = 190 ms   > 0  ->  Uhr von A geht 190 ms NACH (zu langsam)
```

**Ausgleich der Zeitdifferenz:**

- **Graduell**, die Uhr darf **nicht zurückgesetzt** werden (sonst „Zeitreisen“, z. B. Dateien mit Zeitstempel in der Zukunft, Make-Probleme).
- Uhr **zu schnell** → Systemzeit pro Timer-Tick **weniger** erhöhen (z. B. **9 ms statt 10 ms**). Uhr **zu langsam** → **mehr** erhöhen (z. B. **11 ms**).

**Hierarchie der Zeitserver (Strata):**

| Stratum | Bedeutung |
|---|---|
| **0** | präzise Referenzuhren (Atomuhren, GPS-Empfänger) |
| **1** | Server, **direkt** an Stratum-0-Uhren angeschlossen |
| **≥ 2** | Server, die ihre Zeit von einem **niedrigeren** Stratum beziehen |

→ **A übernimmt die Zeit von B nur, wenn B ein kleineres Stratum-Level hat.**

*Linux-Praxis:* `timedatectl timesync-status` zeigt den aktuellen NTP-Server; Python-Demo mit `ntplib` (siehe [9.5](#95-vorlesungsdemos-unter-linux)).

### 5.2 Logische Uhren `★★`

**Motivation:** Einigung auf eine einheitliche **reale** Zeit ist aufwändig. Meist genügt eine einheitliche **zeitliche Abfolge**.

**Happens-before-Relation a → b:**

1. a und b im **selben Prozess**, a geschieht vor b ⇒ a → b.
2. a = **Senden** einer Nachricht, b = **Empfangen** derselben ⇒ a → b.
3. **Transitiv:** a → b und b → c ⇒ a → c.
4. Ereignisse x, y, die (direkt oder indirekt) **keine Nachrichten austauschen**, sind **nebenläufig** („gleichzeitig“): weder x → y noch y → x.

**Gesucht:** Zeiten C(x) für jedes Ereignis, sodass **a → b ⇒ C(a) < C(b)**. Zeiten dürfen nur **wachsen**.

**Lamport-Algorithmus (Middleware verwaltet lokale Zähler):**

| Ereignis | Aktion |
|---|---|
| **Senden** durch P<sub>i</sub> | 1. C<sub>i</sub> = C<sub>i</sub> + 1. 2. Zeitstempel t<sub>m</sub> der Nachricht = C<sub>i</sub> |
| **Empfangen** durch P<sub>j</sub> | 1. C<sub>j</sub> = **max**{C<sub>j</sub>, t<sub>m</sub>}. 2. C<sub>j</sub> = C<sub>j</sub> + 1. 3. Nachricht an die Anwendung ausliefern |

Zusatz für **eindeutige** Zeitstempel: **Prozessnummer i als Nachkommastelle** (Zeitstempel 2.1 = Zählerstand 2 von Prozess 1). (Üblicherweise wird zusätzlich vor jedem lokalen Ereignis hochgezählt; die Folie nennt Senden/Empfangen.)

**Rechenbeispiel (alle Zähler starten bei 0):**

```
P1: sendet m1  -> C1 = 1, ts = 1  ----------------+
P2:                                               v  empfängt m1: C2 = max(0,1)+1 = 2
P2: sendet m2  -> C2 = 3, ts = 3  ----------------+
P3:                                               v  empfängt m2: C3 = max(0,3)+1 = 4
P3: sendet m3  -> C3 = 5, ts = 5  -> P1 empfängt: C1 = max(1,5)+1 = 6
```

**Wozu die Korrektur (`max`)?** Angenommen P2 steht schon bei C2 = 2 und empfängt eine Nachricht mit ts = 6. Ohne Korrektur wäre der Empfang „zeitlich vor“ dem Senden (2 < 6), das verletzt a → b ⇒ C(a) < C(b). Mit Korrektur: C2 = max(2, 6) + 1 = **7 > 6**. ✔

> **Achtung:** Aus C(a) < C(b) folgt **nicht** a → b (Lamport-Uhren erkennen Nebenläufigkeit nicht). Nur die Umkehrung gilt.

#### Vollständig geordneter Multicast mit Lamport-Uhren

**Beispiel Bank mit replizierten Servern:** Einzahlung von 100 € an Standort A und Zinsberechnung an Standort B. **Unterschiedliche Reihenfolge ⇒ unterschiedliche Kontostände.** → **Einheitliche Reihenfolge** auf allen Kopien nötig (welche, ist egal).

**Verfahren (rein verteilt, kein zentraler Prozess):**

1. Jede Multicast-Nachricht bekommt einen **Lamport-Zeitstempel**.
2. Empfänger sortieren Nachrichten **nach Zeitstempel** in ihre **lokale Warteschlange** ein.
3. Der Empfänger **bestätigt** (ACK) die Nachricht per **Multicast an alle**.
4. Die Nachricht am **Kopf** der Warteschlange wird an die Anwendung ausgeliefert, wenn sie von **allen** Prozessen bestätigt wurde.

**Eigenschaft:** Alle Prozesse haben **immer identische Warteschlangen** → Auslieferung überall in **derselben Reihenfolge**. **Voraussetzung:** Nachrichten **desselben Senders** kommen **geordnet** an.

**Die drei Beispielsituationen (n = 3, P1–P3):**

| Situation | Ablauf |
|---|---|
| **Ein Multicast** | P1 sendet bei T1 = 2 die Nachricht mit Zeitstempel **2.1**. P2, P3 reihen 2.1 ein und senden ACKs an alle. Sobald ein Prozess alle ACKs für 2.1 hat, wird 2.1 verarbeitet. |
| **Zwei Multicasts, unterschiedliche Zeit** | P1: **2.1** (T1 = 2), P2: **1.2** (T2 = 1). Die Sortierung stellt sicher, dass **1.2 überall am Kopf** steht → 1.2 wird zuerst verarbeitet, danach 2.1. |
| **Zwei Multicasts, gleiche Zeit** | P1: **2.1**, P2: **2.2** (beide T = 2). Die **Prozessnummer als Nachkommastelle entscheidet**: 2.1 vor 2.2, überall. |

### 5.3 Gegenseitiger Ausschluss `★★`

**Problem:** Mehrere Prozesse greifen gleichzeitig auf gemeinsame Ressourcen zu → Inkonsistenzen/Fehler. **Ziel:** Zu jedem Zeitpunkt **höchstens ein Prozess** in der Ressource.

| Verfahrensfamilie | Idee | Vor-/Nachteile |
|---|---|---|
| **Token-basiert** | Ein **Token** kreist; nur der **Besitzer** darf die Ressource nutzen | + geringe Gefahr von Deadlock und Verhungern (Starvation); − **Tokenverlust** erfordert komplexe Wiederherstellung |
| **Erlaubnis-basiert** | Vor dem Zugriff **Zustimmung** anderer Prozesse einholen | viele Protokolle möglich |

#### Die vier Algorithmen

**(1) Zentralisierter Algorithmus**

- Ein Prozess wird **Koordinator**. Zugriffsanfragen gehen an ihn.
- Er erlaubt den Zugriff nur, wenn die Ressource **frei** ist, sonst kommt die Anfrage in eine **Warteschlange** und wird später genehmigt.
- Nach der Nutzung: **Freigabenachricht** an den Koordinator.
- **Nachrichten pro Zugriff:** Anfrage + Genehmigung + Freigabe = **3**.
- + einfach, **fair**, kein Deadlock/Verhungern. − Koordinator = **Single Point of Failure** und evtl. **Bottleneck**; − Client kann **„Zugriff verweigert“ nicht von „Koordinator ausgefallen“ unterscheiden**.

**(2) Dezentraler Algorithmus**

- **n Koordinatoren**; Zugriff nur mit **Mehrheitsvotum m > n/2**.
- Koordinatoren melden **klar, wenn der Zugriff verweigert** wird → neuer Versuch nach **zufälliger Zeit**.
- Koordinatoren können **abstürzen und resetten** → Risiko **falscher Freigaben**.
- Folienbeispiel: T = 3 h, Nutzung ∆t = 10 s, Reset-Wahrscheinlichkeit während einer Nutzung p = ∆t/T (≈ 10 s / 10 800 s ≈ **0,09 %**; die Folie nennt „0,92 %“, siehe [Kap. 11](#11-korrekturen-und-unstimmigkeiten-im-material)). Bei n = 32 und m = ¾·n ist die Wahrscheinlichkeit einer **Regelverletzung < 10<sup>−40</sup>**.
- − Bei **hoher Konkurrenz** sinkt die Auslastung stark; − effiziente Lösungen komplexer als zentrale.

**(3) Verteilter Algorithmus**

- Zugriffsanfrage mit **Prozessnummer + logischem Zeitstempel** an **alle** Prozesse.
- Reaktion des Empfängers je nach Zustand:
  - **I.** nicht aktueller Nutzer und nicht interessiert → sendet **OK**
  - **II.** **aktueller Nutzer** → **keine Antwort**, Anfrage in die Warteschlange
  - **III.** **will selbst nutzen** → eigener Zeitstempel **niedriger** ⇒ wie II, sonst **OK**
- Vor der Nutzung wird auf **OK von allen** gewartet. Nach der Nutzung: **OK an alle in der Warteschlange** (und leeren).
- **Nachrichten pro Zugriff:** (n−1) Anfragen + (n−1) OKs = **2(n−1)**.
- − hoher Nachrichtenaufwand, **n Points of Failure**, Ausfallerkennung schwierig. **Fazit:** eher theoretische/akademische Lösung.

**(4) Token-Ring-Algorithmus**

- Prozesse in einem **logischen Ring** (Reihenfolge egal). Ein **Token** zirkuliert; der Besitzer darf die Ressource nutzen.
- Nutzung beendet **oder** kein Bedarf → Token **weitergeben**.
- + **Fairness** (Rundlauf sichert die Reihenfolge). − **Token-Verlust** schwer erkennbar, komplexe Wiederherstellung. Bestätigungsnachrichten erkennen Prozessausfälle → Ring anpassen.

| | Zentral | Dezentral | Verteilt | Token-Ring |
|---|---|---|---|---|
| Koordination | 1 Koordinator | n Koordinatoren, Mehrheit | alle Prozesse | Token |
| Hauptproblem | Single Point of Failure | Resets, Auslastung bei Konkurrenz | n Points of Failure, viele Nachrichten | Tokenverlust |
| Fairness | ✔ | zufällige Wiederholung | ✔ (Zeitstempel) | ✔ |

### 5.4 Wahlalgorithmen `★★`

**Motivation:** Viele verteilte Algorithmen brauchen einen **Koordinator**. Jeder Prozess hat eine **eindeutige ID** (z. B. Netzwerkadresse). **Ziel:** Prozess mit der **höchsten Nummer** wird Koordinator. **Problem:** Der Status (aktiv/nicht aktiv) aller Prozesse ist **nicht global bekannt**. Wahlalgorithmen stellen sicher, dass **am Ende alle denselben Koordinator kennen**.

#### Bully-Algorithmus

- **Start:** Ein Prozess bemerkt den **Ausfall des Koordinators**.
- Prozess P sendet **ELECTION** an **alle Prozesse mit höherer ID**.
  - **Keine Antwort** ⇒ P wird neuer Koordinator.
  - **Antwort** eines höheren Prozesses ⇒ dieser **übernimmt die Wahl**.
- Wer ELECTION von einer **niedrigeren** ID bekommt, antwortet **OK** und startet **selbst eine Wahl** (falls noch nicht geschehen).
- Ende: Der Prozess mit der **höchsten ID** wird Koordinator und sendet **COORDINATOR** an alle.
- Kommt ein ausgefallener Prozess zurück, startet er **eine neue Wahl**. Der Höchste „**schlägt sich durch**“ (Bully = Rüpel).

*Beispiel:* Prozesse 1–6, Koordinator **6 fällt aus**, P3 bemerkt es.

```
P3 --ELECTION--> P4, P5, P6          P4, P5 antworten OK (6 antwortet nicht)
P4 --ELECTION--> P5, P6              P5 antwortet OK
P5 --ELECTION--> P6                  keine Antwort  ->  P5 wird Koordinator
P5 --COORDINATOR--> alle
```

#### Ring-Algorithmus

- Prozesse in einem **logischen Ring**, jeder kennt seinen **Nachfolger**.
- Ein Prozess startet die Wahl: **ELECTION mit eigener ID** an den Nachfolger. Jeder Empfänger **hängt seine ID an** und reicht weiter.
- Enthält die Nachricht die **eigene ID**, ist der Ring durchlaufen → Koordinator = **höchste ID** der Liste; Versand von **COORDINATOR** um den Ring.
- + einfach. − **langsame Ausbreitung** des Ergebnisses. **Ausgefallene Nachbarn** werden **übersprungen**.

*Beispiel:* Ring 3 → 5 → 1 → 4 → (zurück zu 3). P3 startet:

```
[3] -> P5: [3,5] -> P1: [3,5,1] -> P4: [3,5,1,4] -> P3 (sieht eigene ID)
Koordinator = max = 5;  COORDINATOR(5) läuft einmal um den Ring
```

#### Wahlen in kabellosen (Ad-hoc-)Umgebungen

- Klassische Algorithmen setzen **stabile Netze und zuverlässige Übertragung** voraus, unrealistisch für **mobile Ad-hoc-Netze**. **Ziel:** den **„besten“** Koordinator wählen (nicht nur den mit der höchsten ID).
- **Ablauf (baumartig):**
  1. Ausgangsknoten sendet **ELECTION** an seine Nachbarn.
  2. Beim **ersten** Empfang: Absender als **Elternknoten** merken, ELECTION an eigene Nachbarn weiterleiten, **Ressourceninfos** sammeln (Kapazität, **Batteriestand**), auf Antworten **aller** Nachbarn warten, den **besten Knoten** bestimmen und an den Elternknoten melden.
  3. **Weitere** ELECTION-Nachrichten werden **sofort** beantwortet.
- Die Ressourceninformationen laufen schrittweise zum Ausgangsknoten zurück → am Ende wird der **leistungsfähigste Knoten** Koordinator.

---

## 6. Konsistenz und Replikation

*(Vorlesung 6 · Übung 5)*

**Motivation:** Daten werden **repliziert**, um **Zuverlässigkeit** und **Leistungsfähigkeit** zu erhöhen. Wird **eine** Kopie aktualisiert, müssen **alle anderen** nachziehen.
**Konsistenz** = alle Kopien haben nach jeder Operation den **gleichen Zustand**.

**Herausforderungen:** Erstellung, Nutzung, Verwaltung replizierter Daten · gemeinsames Verständnis von Konsistenz → **Konsistenzmodelle** · Sicherstellung von Konsistenz → **Konsistenzprotokolle**.

### 6.1 Replikation

#### Einsatzgründe `★★★`

| Grund | Details |
|---|---|
| **Erhöhung der Zuverlässigkeit** | Bei **Ausfall einer Kopie** auf eine andere **umschalten**. **Schutz vor Datenkorruption** durch Mehrfachkopien und **Mehrheitsprinzip**. |
| **Leistungssteigerung** | **Bessere Skalierbarkeit** durch Lastverteilung auf mehrere Server. **Kürzere Zugriffszeiten** durch Kopien in **Nutzernähe**. |

**Der Preis: Konflikt zwischen Konsistenz und Performance.** Replikation verursacht **Inkonsistenz**, wenn Kopien nicht aktualisiert sind. *Beispiel:* **Browser-Cache** verbessert Zugriffszeiten, kann aber **veraltet** sein. → Abwägung **Aktualität ↔ Performance**.

> **Prüfungsantwort „Einsatzgründe für Replikation“:** (1) Zuverlässigkeit/Verfügbarkeit (Umschalten bei Ausfall, Mehrheitsentscheid gegen korrupte Kopien), (2) Leistung (Lastverteilung, kürzere Zugriffszeiten durch Nähe). Nachteil: Konsistenzaufwand.

#### Replikation als Skalierungstechnik `★★`

- **Caching:** Daten nahe an den Prozessen → kürzere Zugriffszeiten. Aber: häufige Aktualisierungen erzeugen **mehr Netzwerkverkehr**, und viele Updates sind **unnütz**, wenn #Zugriffe ≪ #Aktualisierungen.
- **Strikte Konsistenz** erfordert **atomare Aktualisierung aller Kopien** → aufwändiger globaler Abgleich, hohe Kommunikationskosten, bei vielen geografisch verteilten Replikaten kaum umsetzbar.
- **Lösung:** **Konsistenzanforderungen lockern**, je nach Zugriffs- und Aktualisierungsverhalten der Anwendung.

#### Management von Replikaten `★★`

**Platzierung von Replikatservern:** Auswahl von **K Standorten aus N** Nutzerstandorten, **Latenz und Netzwerklast minimieren**. Komplexes Optimierungsproblem → **Heuristiken**, Vorgehen: Regionen/Cluster von Nutzern identifizieren.

**Drei Arten von Replikaten:**

| Art | Beschreibung | Beispiel |
|---|---|---|
| **Permanent** | **statische** Replikate, meist wenige Server an festen Standorten | Web-Cluster, geografisch verteilte **Mirrors** |
| **Server-initiiert** | **dynamisch** vom Dateninhaber erzeugte Kopien zur Leistungssteigerung | temporäre Serverkopien nahe aktiver Nutzergruppen |
| **Client-initiiert** | **lokale, temporäre Speicher (Caches)**, ohne direkte Konsistenzgarantien des Datenspeichers | Browser-Cache |

**Verteilung von Inhalten (drei Fragen):**

| Frage | Optionen |
|---|---|
| **Was** wird verteilt? | 1. **Aktualisierungsnachricht/Invalidierung** (wenig Bandbreite) · 2. **aktualisierte Daten** (sinnvoll bei **vielen Leseoperationen**) · 3. **Aktualisierungsoperation** (wenig Bandbreite, aber **Rechenleistung** bei den Replikaten) |
| **Wer** löst aus? | **Push/serverbasiert:** Server sendet automatisch; geeignet für **hohe Konsistenzanforderungen und viele Lesezugriffe**; mehr Verwaltungsaufwand beim Server. **Pull/clientbasiert:** Client fragt aktiv; effizient bei **niedrigem Lese-zu-Schreib-Verhältnis**; **längere Antwortzeiten** bei Aktualisierung. |
| **Wie** wird verteilt? | **Unicast:** einzelne Nachrichten, gut für einzelne Anfragen, ineffizient bei vielen Empfängern. **Multicast:** eine Nachricht an eine Gruppe, effizient bei vielen Replikaten, besonders in **lokalen Netzen**. |

### 6.2 Konsistenzmodelle `★★`

**Konsistenzmodelle** = Regeln, die beschreiben, **wie und wann Daten für verschiedene Prozesse sichtbar sein müssen**. Grundannahme: Eine **Leseoperation liefert den Wert der letzten Schreiboperation**. Modelle **schränken ein, welche Werte gelesen werden dürfen**:

- **Starke Einschränkungen** → einfache Nutzung, aber **hoher Aufwand**
- **Wenige Einschränkungen** → schwierige Nutzung, aber **gute Performance**
- **Strikte Konsistenz:** **atomare Ausführung aller Operationen in global einheitlicher Reihenfolge** (aufwändig, z. B. durch Sperren).

#### Datenzentrierte Konsistenzmodelle (globale Reihenfolge)

| Modell | Inhalt | Beispiel |
|---|---|---|
| **Kontinuierliche Konsistenz** | Inkonsistenz wird in **drei Dimensionen** toleriert: **numerische Werte** (max. Abweichung), **Aktualität** (max. Alter), **Reihenfolge** (max. Abweichung zwischen Updates) | Börsenkurs darf max. 1 % abweichen · Wetterdaten max. 2 min alt |
| **Sequentielle Konsistenz** | **Alle Prozesse sehen dieselbe Reihenfolge** aller Operationen; die Reihenfolge je Prozess entspricht seiner **Programmreihenfolge** | P1: W(x)a, P2: W(x)b. Alle lesen erst b, dann a ✔. P3 liest b,a aber P4 liest a,b ✘ |
| **Kausale Konsistenz** | Abschwächung der sequentiellen K.: nur **kausal abhängige** Schreiboperationen müssen **überall in gleicher Reihenfolge** gesehen werden. **Unabhängige** Schreiboperationen dürfen in **unterschiedlicher** Reihenfolge erscheinen | P1 schreibt a; P2 liest a, schreibt b ⇒ b hängt von a ab ⇒ alle sehen a vor b |

#### Client-zentrierte Konsistenzmodelle (Sicht eines einzelnen Prozesses)

- Datenzentrierte Modelle regeln **globale Reihenfolgen**: aufwändig, nur nötig bei **vielen gleichzeitigen Aktualisierungen**.
- **Client-zentrierte** Modelle regeln die Zugriffe des **lokalen Prozesses**, **keine Zusicherung für gleichzeitige Zugriffe anderer**. Geeignet, wenn es **kaum gleichzeitige Aktualisierungen** gibt.

| Modell | Garantie | Beispiel |
|---|---|---|
| **Letztendliche Konsistenz** (Eventual) | Jede Kopie wird **irgendwann** aktualisiert | DNS, Web-Caches |
| **Monotones Lesen** | Wiederholtes Lesen liefert **gleiche oder aktuellere** Werte, nie ältere | E-Mail-Postfach zeigt nicht plötzlich wieder alte Zustände |
| **Monotones Schreiben** | Aktualisierungen werden auf **allen** Kopien **in gleicher Reihenfolge** ausgeführt | Software-Bibliothek: Update 2 setzt Update 1 voraus |
| **Read Your Writes** (Lese dein Geschriebenes) | Nach einem Schreibvorgang sieht der Schreiber **seine eigene** Änderung | Passwort geändert, sofort wirksam |
| **Writes Follow Reads** (Geschriebenes folgt Gelesenem) | Ein Schreibvorgang wirkt auf einen **mindestens so aktuellen** Stand wie den zuvor **gelesenen** | Forum: Antwort erscheint nach dem gelesenen Beitrag |

---

## 7. Fehlertoleranz

*(Vorlesung 6 · Übung 5)*

**Verteilte Systeme müssen trotz teilweiser Ausfälle weiterfunktionieren und sich erholen.**

- *Einzelsysteme:* Ausfälle betreffen oft das **gesamte** System.
- *Verteilte Systeme:* nur **bestimmte Komponenten** fallen aus, der Rest bleibt funktionsfähig.
- **Ziele des Systemdesigns:** **automatische Erholung** von Teilfehlern · **akzeptable Leistung** während der Reparatur · **Betrieb trotz bestehender Fehler** fortsetzen.

### 7.1 Konzepte und Modelle `★★★`

#### Eigenschaften verlässlicher Systeme (Dependability)

| Eigenschaft | Bedeutung |
|---|---|
| **Verfügbarkeit** (Availability) | System ist **jederzeit einsatzbereit** |
| **Zuverlässigkeit** (Reliability) | System läuft **über längere Zeit ohne Ausfall** |
| **Sicherheit** (Safety) | Fehler verursachen **keine katastrophalen Folgen** |
| **Wartbarkeit** (Maintainability) | Fehler lassen sich **leicht erkennen und beheben** |

> **Abgrenzung (Klassiker):** *Verfügbarkeit* = Anteil der Zeit, in dem es läuft (kurze Ausfälle okay). *Zuverlässigkeit* = **kontinuierlich** ohne Ausfall. Ein System, das jede Stunde 1 ms ausfällt, ist hoch verfügbar, aber unzuverlässig.

#### Fehlerbegriffe `★★★`

| Deutsch (Folie) | Englisch | Bedeutung |
|---|---|---|
| **Fehlursache** | *Fault* | **Grund** für den Fehler, z. B. **defekte Hardware** |
| **Fehler** | *Error* | **Zustand**, der zu einem Systemausfall führen kann |
| **Ausfall** | *Failure* | **Zugesicherte Dienste** können **nicht mehr** bereitgestellt werden |

*Kette:* Fehlursache → Fehler → Ausfall. Beispiel: defekter Speicherchip (Fehlursache) → falscher Wert im Speicher (Fehler) → Server liefert falsche Antworten (Ausfall).

**Arten von Fehlern:**

| Art | Merkmal |
|---|---|
| **Vorübergehend** (transient) | tritt **einmal** auf und **verschwindet** |
| **Intermittierend** | **kommt und geht unregelmäßig** |
| **Dauerhaft** (permanent) | besteht **bis zur Reparatur/zum Austausch** |

#### Ausfallmodelle `★★★`

Fehlverhalten deutet auf Probleme bei **Servern, Kommunikationskanälen oder deren Abhängigkeiten**. Einzelfehler können zu umfassenden Ausfällen führen → **Klassifikationsschemata** bewerten die Schwere:

| Fehlertyp | Beschreibung |
|---|---|
| **Absturzfehler** (Crash) | Server **stoppt**, arbeitet aber **bis zum Stillstand korrekt** |
| **Auslassungsfehler** (Omission) | Server **reagiert nicht** auf Anfragen |
| ↳ Empfangsauslassung | Server **empfängt** Nachrichten nicht |
| ↳ Sendeauslassung | Server **sendet** keine Nachrichten |
| **Zeitfehler** (Timing) | Antwort **außerhalb des vorgegebenen Zeitintervalls** |
| **Antwortfehler** (Response) | Antwort ist **falsch** |
| ↳ Wertfehler | **Wert** der Antwort ist falsch |
| ↳ Zustandsübergangsfehler | Server **weicht vom korrekten Kontrollfluss** ab |
| **Willkürlicher (Byzantinischer) Fehler** | Server erzeugt **beliebige Antworten zu beliebigen Zeiten** |

> Die Schwere steigt grob von **Absturz** (am harmlosesten) bis **willkürlich** (am schlimmsten, u. a. weil man ihn nicht einmal erkennen kann).

#### Verschleierung von Ausfällen durch Redundanz `★★★`

Fehlertolerante Systeme **verbergen Fehler vor anderen Prozessen**. Ansatz: **Redundanz**, in drei Arten:

| Art | Idee | Beispiel |
|---|---|---|
| **Informationsredundanz** | **zusätzliche Bits** in Daten, um beschädigte Informationen wiederherzustellen | **Hamming-Code** korrigiert Übertragungsfehler |
| **Zeitliche Redundanz** | Aktionen/Operationen werden **bei Bedarf wiederholt** | Transaktion wird bei Fehler **erneut ausgeführt**; Nachricht nach Timeout erneut senden |
| **Physische Redundanz** | **zusätzliche Hardware oder Prozesse** überbrücken den Ausfall einzelner Komponenten | **Prozessreplikation**, mehrere Instanzen parallel |

> **Merkhilfe:** *Information* = extra **Bits**, *Zeit* = extra **Versuche**, *Physik* = extra **Geräte/Prozesse**.

### 7.2 Resiliente Prozesse `★★`

**Prozessgruppen:** Mehrere **identische Prozesse** erhalten **alle Nachrichten**; fällt einer aus, übernimmt ein anderer.

| Gruppentyp | Aufbau |
|---|---|
| **Hierarchisch** | **ein Koordinator** + mehrere **Backup-Prozesse** |
| **Flach** | **gleichrangige** Prozesse mit **repliziertem Schreiben** |

**Fehlertoleranz-Grad:**

- Gruppe von **k + 1** Prozessen kann **k Prozessausfälle** (z. B. Abstürze) verbergen: mindestens einer überlebt.
- Gruppe von **2k + 1** Prozessen kann **k fehlerhafte** Prozesse verbergen: bei bis zu k falschen Antworten bilden die k+1 korrekten die **Mehrheit** (Mehrheitsentscheid).

**Fehlererkennung:** Welche Gruppenmitglieder funktionieren noch? Ansätze: **aktives „Anpingen“** oder **passives Beobachten** eingehender Nachrichten. Schwierigkeit: unzuverlässige Netze, und man kann **Prozessausfall nicht von Kanalausfall unterscheiden**.

### 7.3 Zuverlässige Kommunikation `★★`

Kanalfehler: **Absturz, Verlust, Verzögerung, willkürliche Fehler**. Zuverlässige Kommunikation behandelt vor allem **Absturz und Verlust**.

**Client-Server:** Punkt-zu-Punkt nutzt zuverlässige Transportprotokolle (z. B. **TCP**). Bei **RPC** gibt es fünf Fehlerklassen:

| # | Fehler | Behandlung |
|---|---|---|
| 1 | **Client kann Server nicht finden** | **Fehler rückmelden** (Exception) |
| 2 | **Anfrage geht verloren** | **erneut senden nach Timeout** |
| 3 | **Server stürzt nach empfangener Anfrage ab** | **komplex**, **Ausführung unklar** (wurde sie ausgeführt?) |
| 4 | **Antwort geht verloren** | **wiederholte Ausführung**, wenn möglich (nur bei **idempotenten** Operationen unproblematisch) |
| 5 | **Client stürzt nach gesendeter Anfrage ab** | **komplex**: Anfrage **„verwaist“** (Orphan) |

**Gruppenkommunikation (Multicast):** Nachricht an eine Gruppe muss **alle** erreichen. Herausforderungen: **Nachrichtenreihenfolgen**, **Dynamik der Gruppen** (Abstürze), **Effizienz und Skalierbarkeit**.

### 7.4 Wiederherstellung `★★`

**Ziel:** Nach einem Ausfall einen **korrekten Systemzustand** wiederherstellen.

| Ansatz | Bedeutung |
|---|---|
| **Rückwärtserholung** (Backward Recovery) | **Rückkehr zu einem früheren, korrekten Zustand** |
| **Vorwärtserholung** (Forward Recovery) | **Überführung in einen neuen, korrekten Zustand** |
| **Checkpointing** | **regelmäßiges Speichern** des Systemzustands |
| **Message Logging** | **Aufzeichnen** gesendeter/empfangener Nachrichten |

- **Kombination** Checkpointing + Message Logging = **effizientere Wiederherstellung mit weniger Checkpoints** (ab dem letzten Checkpoint werden die geloggten Nachrichten erneut abgespielt).
- Beides erfordert **stabile Datenspeicherung**.
- Rückwärtserholung lässt sich **anwendungsunabhängig in Middleware** realisieren. Aber: Wiederherstellung eines früheren Zustands ist **aufwändig**, und **manche Zustände lassen sich nicht zurücksetzen** (z. B. bereits ausgezahltes Geld, versendete E-Mail).

---

## 8. Fragenkatalog

Der Katalog ist nach den Übungen aufgebaut:

| Teil | Inhalt | Bezug |
|---|---|---|
| **A** | Probeklausur mit Musterlösung | **Übung 5, Aufgabe 1** (a–d) |
| **B** | Fragen zu **allen klausurrelevanten Themen** | **Übung 5, Aufgabe 2** (a–g) + restlicher Vorlesungsstoff |
| **C** | Verständnisfragen zu den **Programmieraufgaben** | Übungen 1–4 |
| **D** | **Rechen- und Skizzenaufgaben** mit Lösungen | NTP, Lamport, Bully, Ring, … |
| **E** | **Wahr/Falsch-Schnelltest** | alle Themen |

> Antworten stehen jeweils im Zitatblock direkt unter der Frage. `★★★` markiert Fragen zu ausdrücklich klausurrelevanten Themen.

---

### Teil A: Probeklausur (Übung 5, Aufgabe 1)

**A.a) Nennen Sie zwei Architekturstile für verteilte Systeme und erklären Sie kurz deren Eigenschaften.** `★★★`

> **Schichtenarchitektur:** Komponenten sind in Schichten organisiert; eine Komponente in Schicht L<sub>i</sub> darf nur Komponenten der Schicht L<sub>i−1</sub> aufrufen. Der Kontrollfluss geht von Schicht zu Schicht, **Anfragen nach unten, Antworten nach oben**. Sehr verbreitet bei Netzwerken (OSI) und in Anwendungen (Nutzerschnittstelle / Verarbeitung / Datenhaltung).
> **Ereignisbasierte Architektur:** Komponenten kommunizieren durch **Ereignisse** (ggf. mit Daten) über **Publish/Subscribe**. Komponenten veröffentlichen und abonnieren Ereignisse, die Middleware ordnet sie zu und gibt sie weiter. Hauptvorteil: **lockere Kopplung** (Sender und Empfänger kennen sich nicht).
> *(Weitere Stile: objektbasiert = Komponenten sind Objekte, verbunden durch verteilte Prozeduraufrufe, passt zum Client-Server-Modell; datenzentriert = Kommunikation über gemeinsamen Datenspeicher.)*

**A.b) Welches Rollenmodell liegt vielen verteilten Systemen zugrunde? Nennen und erklären Sie es kurz.** `★★★`

> Das **Client-Server-Modell**. Die Prozesse werden in zwei Gruppen geteilt: **Server** bieten Dienste an (z. B. Dateisystem, Datenbank), **Clients** fordern Dienste per **Anfrage** an und **warten auf die Antwort** (Anfrage-Antwort-Verhalten). Es beherrscht die Komplexität verteilter Systeme. Rollen können sich überlagern: Ein Server kann für andere Dienste selbst Client sein.

**A.c) Was ist mit vertikaler und horizontaler Verteilung gemeint? Erklären Sie kurz und nennen Sie jeweils ein Beispiel.** `★★★`

> **Vertikale Verteilung:** Die **logischen Komponenten/Schichten** einer Anwendung werden auf **verschiedene Computer** verteilt (z. B. Drei-Schichten-Architektur). Vorteil: Spezialisierung der Rechner. *Beispiel:* Browser (Nutzerschnittstelle), Anwendungsserver (Verarbeitung), Datenbankserver (Datenhaltung).
> **Horizontale Verteilung:** **Clients bzw. Server selbst** werden in **logisch äquivalente Teile** aufgespalten, jeder Teil bearbeitet einen **eigenen Datenausschnitt** → **Lastverteilung**. Führt zu **dezentralisierten** Architekturen. *Beispiel:* **Peer-to-Peer-Netz** (z. B. verteilte Hashtabelle) oder ein Web-Cluster mit mehreren gleichartigen Servern.

**A.d) Was ist eine Middleware und wozu gibt es sie?** `★★★`

> Eine **Schicht zwischen Anwendung und verteilter Plattform** (Betriebssystem/Netzwerk). Ziel: **Verteilungstransparenz**: Daten, Verarbeitung und Kontrolle werden **vor der Anwendung verborgen**, Heterogenität (Hardware, Betriebssysteme, Datenformate) wird überbrückt, und allgemeine Dienste (Kommunikation, Authentifizierung, Transaktionen, Namensdienste) werden bereitgestellt. Das **vereinfacht die Anwendungsentwicklung**. *Beispiele:* CORBA (objektbasiert), ROS (eventbasiert), gRPC, Kafka. *Nachteil:* Einschränkungen und fehlende Flexibilität des gewählten Stils.

---

### Teil B: Fragen nach klausurrelevanten Themen (Übung 5, Aufgabe 2)

#### B1. Einführung (Begriffsdefinitionen, Ziele, Eigenschaften) `★★★`

**E1. Was ist ein verteiltes System?**

> Eine Ansammlung **unabhängiger Computer**, die für den Nutzer wie ein **einziges zusammenhängendes System** erscheint.

**E2. Nennen Sie wichtige Eigenschaften verteilter Systeme.**

> (1) Unterschiede zwischen den Computern, ihre Kommunikation und die interne Organisation sind **verborgen**. (2) **Einheitliche Nutzung** unabhängig von Ort und Zeit. (3) Gute **Erweiterbarkeit/Skalierbarkeit**. (4) **Kontinuierliche Verfügbarkeit** trotz Störungen, Erweiterungen oder Reparaturen.

**E3. Nennen Sie die vier Ziele verteilter Systeme.**

> **Verfügbarmachung von Ressourcen**, **Verteilungstransparenz**, **Offenheit**, **Skalierbarkeit**.

**E4. Welche Arten von Transparenz gibt es? Erklären Sie je eine kurz.**

> **Zugriff** (einheitlicher Zugriff unabhängig von der Repräsentation), **Verortung** (Ort irrelevant, logische Namen), **Ortsveränderung** (Verschieben bleibt unbemerkt), **Replikation** (Kopien wie Original nutzbar), **Nebenläufigkeit** (gleichzeitige Nutzer stören sich nicht), **Störung** (Ausfälle/Wiederherstellung bleiben verborgen).

**E5. Was bedeutet „transparent“ im Zusammenhang mit verteilten Systemen?**

> Zwei mögliche Lesarten: (1) *vorhanden, aber vom Nutzer nicht wahrgenommen*, (2) *durchsichtig, sodass das Verhalten nachvollziehbar ist*. Bei verteilten Systemen ist **(1)** gemeint: Die Verteilung soll **unsichtbar** sein.

**E6. Was ist Offenheit, und welche Ziele hat sie?**

> Dienste werden über **standardisierte Schnittstellen** (IDL) mit **Syntax** (Funktionsnamen, Parameter, Rückgabewerte) und **Semantik** (Bedeutung) beschrieben, vollständig und neutral. Ziele: **Interoperabilität, Portabilität, Erweiterbarkeit, Flexibilität**. *Beispiele für Beschreibungen:* WSDL (XML, SOAP) und OpenAPI (JSON/YAML, REST).

**E7. In welchen drei Dimensionen kann ein System skalieren? Nennen Sie je ein Problem.**

> **Größe** (Nutzer/Ressourcen): zentrale Dienste/Daten/Algorithmen werden zum **Flaschenhals**. **Geografie** (Entfernung): **Latenz** im WAN, synchrone Kommunikation blockiert, Kommunikation unzuverlässiger. **Verwaltung** (Domänen): Konflikte bei Ressourcennutzung, Verwaltung und **Sicherheit**.

**E8. Mit welchen Techniken lässt sich Skalierbarkeit verbessern? Wie unterscheiden sich Replikation und Caching?**

> **Latenzen verstecken** (asynchrone Kommunikation, Verarbeitung beim Client), **Aufteilung** (z. B. DNS), **Replikation**, **Caching**. Replikation: Entscheidung beim **Ressourcenbesitzer**, **im Voraus geplant**. Caching: Entscheidung beim **Client**, **auf Abruf**. Beides erzeugt **Konsistenzprobleme**.

**E9. Nennen Sie fünf der „8 Fehlannahmen“ über verteilte Systeme.**

> Das Netzwerk ist zuverlässig · sicher · homogen · die Topologie ändert sich nicht · Latenz ist 0 · Bandbreite ist unendlich · Transportkosten sind 0 · es gibt nur einen Administrator.

**E10. Was unterscheidet Cluster- von Grid-Computing?**

> **Cluster:** Standard-PCs + Hochgeschwindigkeitsnetz, **homogen**. **Grid:** Rechner mehrerer **Verwaltungsdomänen** zu **virtuellen Organisationen**, **heterogen**.

**E11. Wofür steht ACID? Was ist eine verteilte Transaktion?**

> **A**tomar, **C**onsistent, **I**soliert, **D**auerhaft. Eine Haupttransaktion wird in mehrere parallele **Subtransaktionen** zerlegt. Änderungen werden erst beim **Commit der Haupttransaktion** dauerhaft, bei **Abbruch** werden **alle** Subtransaktionen zurückgenommen (Alles-oder-Nichts).

**E12. Warum wird bei allgegenwärtigen verteilten Systemen (Ubiquitous Computing) auf Verteilungstransparenz verzichtet?**

> Instabilität ist der **Normalfall** (mobile, batteriebetriebene, drahtlose Knoten, Verbindungen kommen und gehen). Verteilung von Daten, Prozessen und Kontrolle muss daher **explizit behandelt** werden. Beispiel: Sensornetz mit stark beschränkten Ressourcen.

---

#### B2. Architekturen (Architekturstile, Schichtenarchitektur) `★★★`

**A1. Was unterscheidet Software- und Systemarchitektur?**

> **Softwarearchitektur (logisch):** aus welchen Komponenten besteht das System, wo wird welche Funktionalität verortet (Prinzipien: SOLID, KISS, DRY, YAGNI). **Systemarchitektur (physisch):** wie werden die Komponenten auf reale Rechner verteilt (zentralisiert, dezentralisiert, hybrid).

**A2. Nennen Sie die vier Architekturstile und je eine Eigenschaft.**

> **Schichten** (nur Aufruf der Schicht darunter) · **objektbasiert** (Komponenten = Objekte, verteilter Prozeduraufruf, Client-Server) · **ereignisbasiert** (Publish/Subscribe, lockere Kopplung) · **datenzentriert** (gemeinsamer Datenspeicher; als Shared Data Space zusätzlich zeitlich entkoppelt).

**A3. Beschreiben Sie die Schichtenarchitektur für interaktive Anwendungen.**

> **Drei Schichten:** (1) **Nutzerschnittstelle** (Ein-/Ausgabe, meist Client, ggf. lokale Verarbeitung), (2) **Verarbeitung** (Kernfunktionalität, meist Server und Client zugleich), (3) **Datenhaltung** (Datenbank/Dateisystem, persistente Daten, meist Server). *Beispiel Suchmaschine:* Eingabemaske → Anfrageverarbeitung/Ranking → Index.

**A4. Wie lassen sich die drei Schichten auf Client und Server verteilen (Thin/Fat Client)?**

> Je mehr Schichten der Client übernimmt, desto „dicker“: nur Teile der UI (a) → komplettes Frontend ohne Verarbeitung (b) → plus Eingabeprüfung (c) → komplette Anwendung mit direktem DB-Zugriff (d) → plus lokale Datenhaltung (e). **Thin Client:** wenig Aufwand beim Client, zentrale Verwaltung. **Fat Client:** weniger Serverlast und Latenz, aber mehr Pflege auf dem Client.

**A5. Unterscheiden Sie verbindungslose und verbindungsorientierte Client-Server-Kommunikation.**

> **Verbindungslos:** für zuverlässige Netze (LAN), geringer Overhead, aber Zusatzaufwand bei Verlust/Beschädigung. **Verbindungsorientiert:** für unsichere Netze (WAN), z. B. **TCP**; Overhead durch Verbindungsaufbau, dafür Mehrfachnutzung der Verbindung und Kompression.

**A6. Was sind strukturierte und unstrukturierte P2P-Netze? Was ist eine DHT?**

> **Strukturiert:** Overlay deterministisch aufgebaut (Routing-Tabellen), häufigstes Verfahren **verteilte Hashtabelle**: Daten und Knoten erhalten **Schlüssel (z. B. 160 Bit)**, eine Anfrage wird zum **zuständigen Knoten geroutet**. **Unstrukturiert:** Overlay **zufällig**, jeder Knoten hat eine **Nachbarschaftsliste**, Suche per **Flooding**; Herausforderungen: isolierte Gruppen, Lastungleichgewicht.

**A7. Was sind Superpeers und welches Problem entsteht dabei?**

> Spezialknoten, die **Indizes speichern** oder als **Broker** wirken, um die Skalierbarkeit unstrukturierter P2P-Netze zu verbessern (**Aufgabe der Symmetrie**). Neues Problem: **Wer darf Superpeer sein?** → **Leader-Election-Problem**.

**A8. Was ist ein Edge-Server-System?**

> Hybride Architektur: Server am **Rand von (Sub-)Netzwerken**, Clients verbinden sich mit dem Edge-Server ihres Netzes (Beispiel: ISP).

**A9. Wie lässt sich das Verhalten einer Middleware anpassen?**

> **Statisch** über **Daten** (Parameter, Spezifikationen), **dynamisch** über **Code** (**Interceptoren**, Callbacks). Techniken für adaptive Software: Separation of Concerns, **Computational Reflection**, komponentenbasierte Architektur mit **Late Binding**.

**A10. Was ist das Feedback Control Model (Regelkreis) im Selbstmanagement?**

> Das System **misst** seinen Zustand, **vergleicht** ihn mit dem Sollzustand und **passt** Ausführungsverhalten/-verteilung automatisch **an**.

---

#### B3. Prozesse (Threads, Server und Zustände) `★★★`

**P1. Unterscheiden Sie Prozess und Thread.**

> **Prozess:** vollständiger Zustand (CPU-Kontext, Speicher, Ressourcen), **isoliert**, Kommunikation per **IPC**, grob → hoher Overhead. **Thread:** **nur CPU-Kontext**, mehrere Threads in einem Prozess, Kommunikation über **gemeinsamen Speicher** (→ **Synchronisation** nötig), fein → hohe Performance.

**P2. Welche Vorteile haben Threads in nicht-verteilten Systemen?**

> Überbrückung **blockierender Operationen** (GUI vs. Verarbeitung), **Nutzung mehrerer Kerne**, Aufteilung großer Anwendungen ohne IPC-Overhead, **Strukturierung** unabhängiger Aufgaben.

**P3. Wie werden Threads in verteilten Systemen eingesetzt?** `★★★`

> **Clients:** lange Nachrichtenlaufzeiten (100 ms bis Sekunden) **verbergen**: Kommunikation starten und weiterarbeiten, z. B. **Browser** lädt Bilder parallel über **separate Verbindungen**; Nutzer kann interagieren; Last verteilt sich auf replizierte Server. **Server (Hauptanwendung):** **mehrere Anfragen gleichzeitig**, einfacherer Server-Code, bessere Performance.

**P4. Vergleichen Sie einen single- und einen multi-threaded Dateiserver.**

> **Single-threaded:** Hauptschleife arbeitet sequentiell, lange Wartezeiten, **CPU idle** bei Plattenzugriffen. **Multi-threaded:** **Dispatcher** nimmt Anfragen an und verteilt sie auf **Worker-Threads**; parallele Bearbeitung, **CPU bleibt ausgelastet**, während andere Threads auf die Platte warten.

**P5. Welche drei Arten der Virtualisierung gibt es?**

> **Process Virtual Machine** (Laufzeitsystem mit abstrahierten Instruktionen, z. B. JRE/Interpretation oder Emulation), **Virtual Machine Monitor** (komplette Hardware-Abschirmung, mehrere Betriebssysteme, z. B. KVM, Hyper-V, vSphere), **Containerization** (isolierte Umgebung auf dem vorhandenen OS, geringer Overhead, z. B. Docker, Kubernetes).

**P6. Welche vier Schnittstellen hat ein Computersystem?**

> **APIs** (Anwendung ↔ Bibliothek), **Systemaufrufe** (Bibliothek ↔ OS), **privilegierte Instruktionen** (OS ↔ Hardware), **allgemeine Instruktionen** (Anwendung ↔ Hardware). Virtualisierung = Nachahmen einer solchen Schnittstelle.

**P7. Unterscheiden Sie iterative und nebenläufige Server.** `★★★`

> **Iterativ:** der Server bearbeitet jede Anfrage **selbst**, nacheinander. **Nebenläufig:** Anfragen werden an **separate Threads/Prozesse** übergeben, der Server wartet sofort auf neue Anfragen. Varianten: **Multithreaded Server** und **Fork-Server** (UNIX/Linux, `fork`).

**P8. Woher kennt ein Client Adresse und Kontaktpunkt eines Servers?**

> **Adresse:** fest (z. B. Nameserver 8.8.8.8) oder dynamisch über **DNS**. **Kontaktpunkt (Port):** **statisch** (HTTP 80, HTTPS 443, SSH 22, DNS UDP 53; schnell, aber begrenzt) oder **dynamisch** über **Endpoint-Daemon** (Verzeichnis mit festem Port) oder **Superserver** (z. B. `inetd`, startet Server erst bei Anfrage, ressourceneffizient).

**P9. Was ist der Unterschied zwischen zustandslosen und zustandsbehafteten Servern? Nennen Sie je ein Beispiel.** `★★★`

> **Zustandslos:** speichert **nichts** über Clients, Zustandsverlust stört nicht, einfach und robust; Beispiel **Webserver**. **Zustandsbehaftet:** speichert **persistent** Informationen über Clients (explizit zu löschen), **schneller**, aber nach Absturz muss der Zustand **wiederhergestellt** werden; Beispiel **Dateiserver**, der weiß, welcher Client welche Datei liest/schreibt.

**P10. Was ist „Soft State“?**

> Sonderfall zustandsloser Server: Zustandsinformation wird nur **zeitlich begrenzt** gehalten und verfällt danach von selbst.

**P11. Was ist ein dreistufiger Server-Cluster? Wie wahrscheinlich ist es, dass bei 1000 Servern kein Server ausfällt, wenn jeder mit p = 0,1 % ausfällt?**

> Stufe 1: **Switch** (Routing der Anfragen), Stufe 2: **Anwendungs-/Rechenserver**, Stufe 3: **Daten-/Dateiserver bzw. Datenbanken**. P(kein Ausfall) = (1 − p)<sup>N</sup> = 0,999<sup>1000</sup> ≈ **36,8 %**.

**P12. Was ist Code-Migration? Nennen Sie Gründe und Modelle.**

> Verschieben von Programmen, ggf. **während der Ausführung**. Gründe: **Leistung**, **weniger Kommunikation** (Code zu den Daten), **Flexibilität** (Code bei Bedarf laden). Modelle: **schwache Mobilität** (nur Code + Initialdaten), **starke Mobilität** (zusätzlich Ausführungssegment: Instruktionszeiger, Stack), **sender-** vs. **empfängerinitiiert**. Problem: **Sicherheit**, Heterogenität (Lösung: VM wie JVM).

---

#### B4. Kommunikation (Arten von Kommunikation, RPC) `★★★`

**K1. Was ist ein Protokoll?**

> Eine **standardisierte Menge von Regeln**, die festlegt, wie Daten zwischen Rechnern/Prozessen **ausgetauscht, formatiert und verarbeitet** werden. Verbindungsorientiert (vorher Verbindung aufbauen) oder verbindungslos.

**K2. Nennen Sie die Schichten des ISO/OSI-Modells mit ihren Aufgaben.**

> **1** Bitübertragung (Bits) · **2** Sicherung (Frames, Prüfsummen) · **3** Vermittlung (Routing, IP) · **4** Transport (Reihenfolge, Vollständigkeit; TCP/UDP) · **5** Sitzung · **6** Darstellung (Bedeutung der Bits, Datenformate) · **7** Anwendung (HTTP, FTP). Middleware liegt (hauptsächlich) in der Anwendungsschicht.

**K3. Welche Arten von Kommunikation unterscheidet man? Nennen Sie jeweils die Gegensätze.** `★★★`

> **Persistent** (System speichert so lange wie nötig, Sender darf enden) vs. **transient** (nur solange Sender und Empfänger laufen). **Asynchron** (Sender fährt fort) vs. **synchron** (Sender blockiert). **Diskret** (jede Nachricht ist vollständig) vs. **Streaming** (kontinuierlich, mehrere Nachrichten gehören zusammen). *Beispiele:* E-Mail = persistent + asynchron; klassischer RPC = transient + synchron; Videostream = Streaming.

**K4. Erklären Sie die Grundidee des Remote Procedure Call.** `★★★`

> Ein Prozess auf Maschine A **ruft eine Prozedur auf Maschine B auf**, als wäre sie lokal (**Zugriffstransparenz**). A wird angehalten, Parameter gehen zum Server, das Ergebnis zurück. Möglich durch **Client-Stub** (Platzhalter mit gleicher Schnittstelle, verpackt Parameter, sendet) und **Server-Stub** (entpackt, ruft Original auf, sendet Ergebnis).

**K5. Beschreiben Sie den Ablauf eines RPC in Schritten.** `★★★`

> 1 Client ruft Client-Stub · 2 Stub baut Nachricht (Marshaling), ruft OS · 3 Client-OS sendet an Server-OS · 4 Server-OS übergibt an Server-Stub · 5 Server-Stub entpackt, ruft Server-Prozedur · 6 Server arbeitet, Ergebnis an Stub · 7 Stub packt Ergebnis in Nachricht, ruft OS · 8 Server-OS sendet an Client-OS · 9 Client-OS übergibt an Client-Stub · 10 Stub entpackt, gibt Ergebnis an Client.

**K6. Was ist Parameter-Marshaling, und welches Problem entsteht bei Wertparametern?** `★★★`

> Marshaling = **Verpacken der Parameter (plus Prozedurname) in eine Nachricht**; das Format legt das RPC-Protokoll fest. Problem: **Heterogenität**: unterschiedliche Datentypen/Bitgrößen, **Endianness** (Little/Big Endian), Zeichensätze (ASCII/UTF), Programmumgebungen (Python-Client, C-Server). Lösung: **plattformunabhängige Formate/Serialisierung**.

**K7. Warum sind Referenzparameter (Pointer) beim RPC ein Problem, und wie löst man es?**

> Pointer gelten nur im **Adressraum ihres Prozesses**. Lösungen: Pointer **verbieten**, **referenzierte Werte übertragen** (einfach für Skalare, Arrays, Strukturen; nicht für verkettete Listen), Parameter als **Input/Output** markieren.

**K8. Welche Informationen braucht man, um RPC-Stubs automatisch zu generieren?**

> (1) **RPC-Protokoll** (Nachrichtenformat, Darstellung einfacher Typen, Netzwerkkommunikation), (2) **Schnittstellendefinition in einer IDL** (Prozedurnamen, Parameter, Ergebnisse, Datentypen).

**K9. Nennen Sie Eigenschaften von gRPC.**

> Open Source (Google), **HTTP/2**, **Protocol Buffers** als plattformunabhängige IDL und effiziente Serialisierung, **bidirektionale Vollduplex-Kommunikation**, **asynchrones Streaming**, Header-Komprimierung, viele Programmiersprachen.

**K10. Unterscheiden Sie synchronen und asynchronen RPC. Wie erhält der Client beim asynchronen RPC das Ergebnis?**

> **Synchron:** Client blockiert bis zur Antwort. **Asynchron:** Client arbeitet weiter. Ergebnis per **Polling** (Client fragt wiederholt) oder per **Unterbrechung durch den Server** (RPC/Callback vom Server zum Client).

**K11. Welche Nachteile des RPC motivieren nachrichtenorientierte Kommunikation?**

> RPC ist meist **synchron** (Client **blockiert**) und verlangt, dass die **Empfängerseite aktiv** ist. Nachrichtenorientierte Kommunikation legt die Kommunikation offen (**keine Zugriffstransparenz**), ermöglicht dafür **Asynchronität** und **zeitliche Entkopplung**.

**K12. Unterscheiden Sie transiente und persistente nachrichtenorientierte Kommunikation mit Beispielen.**

> **Transient:** Nachrichten nur gespeichert, solange beide Partner laufen; **Berkeley Sockets** (Schnittstelle zur Transportschicht), **MPI** (HPC: Send/Receive, Broadcast/Reduce/Gather, Put/Get). **Persistent:** **Nachrichtenwarteschlangen** (E-Mail, Kafka, RabbitMQ, ROS), Sender/Empfänger müssen nicht gleichzeitig laufen.

**K13. Welche Operationen bieten Nachrichtenwarteschlangen, und was wird garantiert?**

> **Put** (nicht-blockierend einfügen), **Get** (blockierend lesen), **Poll** (nicht-blockierend abfragen), **Notify** (Callback-Funktion registrieren). Garantiert wird **nur das Einfügen** in die Warteschlange, **nicht**, wann oder ob die Nachricht gelesen wird.

**K14. Was ist ein Message Broker?**

> Spezialisierter Knoten, der Nachrichten **auf Anwendungsebene zwischen verschiedenen Formaten übersetzt**, um vielfältige Anwendungen zu **integrieren**, die sich nicht kennen.

**K15. Was sind Datenströme? Welche Arten und Übertragungsmodi gibt es?**

> Folgen von Daten. **Diskret** (Zeitpunkt irrelevant: Pipes, TCP), **kontinuierlich** (zeitgenau nötig: Audio/Video), **komplex** (mehrere synchronisierte Unterströme). Modi: **asynchron** (keine Vorgaben), **synchron** (maximale End-to-End-Verzögerung), **isochron** (minimale *und* maximale Verzögerung).

**K16. Wie lässt sich bei IP-Best-Effort-Netzen die Qualität von Datenströmen verbessern?**

> **Netzwerkebene:** Priorisierung (DSCP, Traffic Shaping, Network Slicing), CDN. **Anwendungsebene:** **Adaptive Bitrate Streaming**, **FEC**, **Pufferung** (Laufzeitschwankungen ausgleichen, Anfangsverzögerung), **verschachtelte Übertragung** (Paketverluste zeitlich verteilen).

**K17. Wie wird Multicasting umgesetzt?**

> **Netzwerkebene:** Ethernet-/IP-Multicast im LAN, im Internet nur eingeschränkt. **Anwendungsebene:** **Overlay/P2P**, **Publish/Subscribe**, **Gossip-Protokolle**.

---

#### B5. Synchronisation (Uhrensynchronisation, NTP) `★★★`

**S1. Wozu braucht man synchronisierte Uhren in verteilten Systemen?**

> Zuverlässige **Zeitstempel** (Dateiänderungen, inkrementelle Übersetzung), **zeitlich begrenzte Sicherheitsüberprüfungen**, **Finanz-/Börsenanwendungen**, **Sensornetze** (zeitabhängige Messwerte).

**S2. Was ist Clock Skew und warum entsteht er?**

> Jeder Rechner hat **eigene Quarzuhr**; **leichte Frequenzunterschiede** führen zu **Zeitabweichungen** und damit zu inkonsistenten Zeitstempeln.

**S3. Was ist UTC?**

> **Universal Coordinated Time** = präzise **Atomzeit + Schaltsekunden** (Angleichung an die Sonnenzeit/Erdrotation). Verbreitung über Stromnetze, Kurzwellenradio, Satelliten, Zeitserver.

**S4. Erklären Sie das Verfahren von NTP einschließlich der Formeln.** `★★★`

> Client A fragt Zeitserver B und ermittelt **T1** (A sendet), **T2** (B empfängt), **T3** (B sendet), **T4** (A empfängt).
> **tDelay = ((T4 − T1) − (T3 − T2)) / 2**, **tOffset = T3 + tDelay − T4**. Messung wiederholen, tOffset beim **minimalen tDelay** verwenden. **tOffset < 0:** Uhr von A zu **schnell**; **tOffset > 0:** zu **langsam**.

**S5. Wie wird die Zeitdifferenz ausgeglichen, und warum darf man die Uhr nicht einfach zurücksetzen?**

> **Graduell:** zu schnelle Uhr → Systemzeit pro Tick **weniger** erhöhen (z. B. 9 statt 10 ms), zu langsame → **mehr** (11 ms). Ein Zurücksetzen würde die Zeit **rückwärts laufen** lassen, Zeitstempel/Ordnungen würden inkonsistent.

**S6. Erklären Sie die Stratum-Hierarchie bei NTP.** `★★★`

> **Stratum 0:** Referenzuhren (Atomuhr, GPS). **Stratum 1:** direkt daran angeschlossene Server. **Stratum ≥ 2:** beziehen Zeit von niedrigerem Stratum. A übernimmt Zeit von B nur, wenn B ein **kleineres Stratum** hat.

**S7. Was besagt die Happens-before-Relation, und wie funktionieren Lamport-Uhren?** `★★`

> a → b gilt, wenn a vor b im **selben Prozess** liegt oder a das **Senden** und b das **Empfangen** derselben Nachricht ist; außerdem **transitiv**. Ohne Nachrichtenpfad: **nebenläufig**. Lamport: Senden: C = C + 1, Zeitstempel = C. Empfangen: C = max(C, ts) + 1. Garantiert **a → b ⇒ C(a) < C(b)**.

**S8. Wie funktioniert vollständig geordneter Multicast, und wozu dient er?** `★★`

> Jede Nachricht erhält einen **Lamport-Zeitstempel**, wird **nach Zeitstempel in die lokale Warteschlange** einsortiert und per **ACK-Multicast** bestätigt. Ausgeliefert wird die Nachricht am **Kopf**, sobald **alle** bestätigt haben → überall **gleiche Reihenfolge** (z. B. replizierte Bankkonten: Einzahlung und Zinsberechnung).

**S9. Vergleichen Sie die Algorithmen für gegenseitigen Ausschluss.** `★★`

> **Zentral:** 1 Koordinator, 3 Nachrichten, einfach/fair, aber **Single Point of Failure**. **Dezentral:** n Koordinatoren, **Mehrheit m > n/2**, Wiederholung nach Zufallszeit, Probleme bei Resets/hoher Konkurrenz. **Verteilt:** Anfrage an alle, OK von allen nötig, **2(n−1)** Nachrichten, n Ausfallpunkte. **Token-Ring:** Token kreist, fair, **Tokenverlust** schwer erkennbar.

**S10. Beschreiben Sie Bully- und Ring-Wahlalgorithmus.** `★★`

> **Bully:** ELECTION an alle **höheren** IDs; bekommt P keine Antwort, wird er Koordinator, sonst übernimmt der Antwortende; am Ende sendet der **höchste** COORDINATOR an alle. **Ring:** ELECTION mit eigener ID wandert den Ring entlang, jeder **hängt seine ID an**; kehrt die Nachricht zum Starter zurück, wird die **höchste ID** Koordinator und per COORDINATOR bekannt gemacht.

---

#### B6. Replikation (Einsatzgründe) `★★★`

**R1. Nennen Sie die Einsatzgründe für Replikation.** `★★★`

> **Zuverlässigkeit:** Umschalten bei Ausfall einer Kopie; **Schutz vor Datenkorruption** durch Mehrfachkopien und **Mehrheitsprinzip**. **Leistung:** **bessere Skalierbarkeit** (Lastverteilung), **kürzere Zugriffszeiten** (Kopien in Nutzernähe).

**R2. Welchen Zielkonflikt bringt Replikation mit sich?** `★★★`

> **Konsistenz vs. Performance:** Sind Kopien nicht aktuell, entsteht **Inkonsistenz** (z. B. veralteter Browser-Cache). Strikte Konsistenz erfordert **atomare Aktualisierung aller Kopien** (teuer). Lösung: **Konsistenzanforderungen lockern** je nach Anwendung.

**R3. Welche drei Arten von Replikaten gibt es?**

> **Permanent** (statisch, feste Standorte, Mirrors), **server-initiiert** (dynamisch durch den Dateninhaber, nahe aktiver Nutzer), **client-initiiert** (lokale Caches ohne Konsistenzgarantien).

**R4. Welche Entscheidungen fallen bei der Verteilung von Aktualisierungen an?**

> **Was:** Invalidierung / neue Daten / Operation. **Wer:** **Push** (Server, bei vielen Lesezugriffen und hohen Konsistenzanforderungen) oder **Pull** (Client, bei niedrigem Lese-Schreib-Verhältnis). **Wie:** **Unicast** oder **Multicast**.

**R5. Erklären Sie sequentielle und kausale Konsistenz.** `★★`

> **Sequentiell:** alle Prozesse sehen **dieselbe Reihenfolge** aller Operationen, jeweils konsistent mit der Programmreihenfolge. **Kausal:** nur **kausal abhängige** Schreibvorgänge müssen überall gleich geordnet erscheinen, unabhängige dürfen unterschiedlich geordnet sein.

**R6. Nennen und erklären Sie client-zentrierte Konsistenzmodelle.** `★★`

> **Letztendlich** (irgendwann überall aktuell), **monotones Lesen** (nie ältere Werte als zuvor gelesen), **monotones Schreiben** (Updates in gleicher Reihenfolge), **Read Your Writes** (eigene Schreibvorgänge sichtbar), **Writes Follow Reads** (Schreiben baut auf zuvor Gelesenem auf). Geeignet bei **wenigen gleichzeitigen Updates**.

---

#### B7. Fehlertoleranz (Begriffsdefinitionen, Redundanz) `★★★`

**F1. Welche Eigenschaften zeichnen verlässliche Systeme aus?** `★★★`

> **Verfügbarkeit** (jederzeit einsatzbereit), **Zuverlässigkeit** (läuft lange ohne Ausfall), **Sicherheit/Safety** (Fehler ohne katastrophale Folgen), **Wartbarkeit** (Fehler leicht erkennen/beheben).

**F2. Unterscheiden Sie Fehlursache, Fehler und Ausfall.** `★★★`

> **Fehlursache (Fault):** Grund, z. B. defekte Hardware. **Fehler (Error):** Zustand, der zu einem Ausfall führen kann. **Ausfall (Failure):** zugesicherte Dienste können nicht mehr erbracht werden. Kette: Fehlursache → Fehler → Ausfall.

**F3. Welche Arten von Fehlern gibt es?** `★★★`

> **Vorübergehend** (einmal, verschwindet), **intermittierend** (kommt und geht unregelmäßig), **dauerhaft** (bis Reparatur/Austausch).

**F4. Nennen Sie Ausfallmodelle (Fehlertypen) für Server.** `★★★`

> **Absturz** (stoppt, bis dahin korrekt), **Auslassung** (reagiert nicht; Empfangs-/Sendeauslassung), **Zeitfehler** (Antwort außerhalb des Zeitintervalls), **Antwortfehler** (Wert- oder Zustandsübergangsfehler), **willkürlich/byzantinisch** (beliebige Antworten zu beliebigen Zeiten).

**F5. Wie verbirgt man Ausfälle durch Redundanz? Nennen Sie die drei Arten mit Beispiel.** `★★★`

> **Informationsredundanz:** zusätzliche Bits (z. B. **Hamming-Code**). **Zeitliche Redundanz:** Aktionen **wiederholen** (z. B. Transaktion erneut ausführen). **Physische Redundanz:** zusätzliche **Hardware/Prozesse** (z. B. **Prozessreplikation**).

**F6. Wie viele Prozesse braucht eine Gruppe, um k Ausfälle bzw. k fehlerhafte Prozesse zu verbergen?** `★★`

> **k + 1** Prozesse verbergen **k Ausfälle** (einer bleibt übrig). **2k + 1** Prozesse verbergen **k fehlerhafte** Prozesse (die k+1 korrekten bilden die Mehrheit).

**F7. Welche Fehlerklassen gibt es beim RPC und wie behandelt man sie?** `★★`

> (1) Server nicht gefunden → **Fehler melden**; (2) Anfrage verloren → **Timeout und erneut senden**; (3) Server stürzt nach Empfang ab → **komplex, Ausführung unklar**; (4) Antwort verloren → **erneute Ausführung, wenn möglich** (idempotent); (5) Client stürzt nach Anfrage ab → **komplex, verwaiste Anfrage**.

**F8. Was sind Rückwärts- und Vorwärtserholung, Checkpointing, Message Logging?** `★★`

> **Rückwärts:** Rückkehr zu einem **früheren korrekten** Zustand. **Vorwärts:** Überführung in einen **neuen korrekten** Zustand. **Checkpointing:** regelmäßiges Zustandsspeichern. **Message Logging:** Nachrichten aufzeichnen. Kombination = weniger Checkpoints nötig.

**F9. Warum ist Fehlertoleranz in verteilten Systemen anders als in Einzelsystemen?**

> In Einzelsystemen betrifft ein Ausfall meist **alles**. In verteilten Systemen gibt es **Teilausfälle**: nur einzelne Komponenten fallen aus, der Rest läuft weiter. Ziel: **automatische Erholung**, **akzeptable Leistung während der Reparatur** und Weiterbetrieb trotz Fehlern.

---

### Teil C: Verständnisfragen zu den Programmieraufgaben (Übungen 1–4)

Die Übungen 1–4 sind Programmieraufgaben. Die Klausur fragt eher das **Konzept dahinter** ab. Diese Fragen prüfen, ob du erklären kannst, *was* du da gebaut hast und *warum* es funktioniert.

#### C1. Übung 1: OpenAPI-Taschenrechner (Einführung, Offenheit, Schichten)

**C1.1 Was beschreibt eine OpenAPI-Spezifikation (`calculator.yaml`), und welche Elemente enthält sie?**

> Die **Schnittstelle** eines REST-Dienstes (IDL für Web-APIs): `openapi` (Version), `info` (Titel/Version), `servers` (URL), `paths` (Endpunkte wie `/add`) mit HTTP-Methode, **`parameters`** (Name, Ort `query`, Typ, Pflicht), **`responses`** (Statuscodes, Inhaltstyp, Schema) und **`operationId`**. Sie legt die **Syntax** fest, die Semantik steht in den Beschreibungstexten.

**C1.2 Wozu dient die `operationId`, und wie hängt die YAML-Datei mit dem Python-Code zusammen?**

> Die `operationId` (Form `modulname.funktionsname`) **bindet einen Endpunkt an eine Python-Funktion**. Das Framework (connexion) nimmt die Anfrage entgegen, **validiert Parameter gegen die Spezifikation** und ruft die Funktion auf. Das ist analog zum **Server-Stub** beim RPC: Spezifikation → generierter/gebundener Aufrufcode.

**C1.3 Wie lässt sich der Taschenrechner in die Drei-Schichten-Architektur einordnen?**

> **Nutzerschnittstelle** = Client-Anwendung (Eingabe/Ausgabe, Aufgabe c), **Verarbeitung** = Server mit `add` usw., **Datenhaltung** = Cache/Datenbank (Aufgabe d). Verteilung auf mehrere Rechner = **vertikale Verteilung**.

**C1.4 Welche Rolle hat die Client-Anwendung aus Aufgabe c) im Sinne von RPC/Transparenz?**

> Ein HTTP-Aufruf (`GET /add?a=2&b=3`) verhält sich wie ein **entfernter Prozeduraufruf** auf `add(2, 3)`. Der Client **kennt nur die Schnittstelle** (Offenheit), nicht die Implementierung. Das HTTP-Protokoll ersetzt das proprietäre RPC-Protokoll, JSON ersetzt das Marshaling-Format.

**C1.5 Variante A: Caching von Client-Anfragen und Ergebnissen. Welche Skalierungstechnik ist das, wo liegt der Cache, und gibt es ein Konsistenzproblem?**

> **Caching** = client-initiierte Kopie (spart Latenz und Serverlast, „Latenzen verstecken“). Der Cache liegt **beim Client** (oder davor), Schlüssel = (Operation, a, b). Ein **Konsistenzproblem entfällt hier**, weil Rechenoperationen **deterministisch** sind: dieselbe Eingabe liefert immer dasselbe Ergebnis, ein Cache-Eintrag wird nie veraltet. Bei veränderlichen Daten (Wechselkurs) wäre Invalidierung nötig.

**C1.6 Variante B: Speicherung von Server-Ergebnissen in einer Datenbank. Was bringt das, und macht es den Server zustandsbehaftet?**

> Bringt **Persistenz** (Verlauf, Auswertung, Wiederverwendung von Ergebnissen) und realisiert die **Datenhaltungsschicht**. Der Server bleibt **zustandslos bezüglich der Clients**, solange er keine Informationen *über einzelne Clients* für die Beantwortung zukünftiger Anfragen braucht. Die Datenbank hält gemeinsamen Datenbestand, keinen Sitzungszustand.

**C1.7 Warum sollte der Dienst Fehlerfälle (z. B. Division durch 0) in der Spezifikation beschreiben?**

> Weil **Syntax und Semantik inklusive Fehlern** zur Schnittstelle gehören (Offenheit): Clients müssen wissen, mit welchem **Statuscode** (z. B. 400) und welchem Format Fehler gemeldet werden. Ohne das ist die Schnittstelle unvollständig.

---

#### C2. Übung 2: ROS 2 Publisher/Subscriber (Architekturen, Middleware, Kommunikation)

**C2.1 Erklären Sie die Begriffe Node, Topic, Publisher, Subscriber, Message und `spin`.**

> **Node:** Prozess/Komponente im ROS-System. **Topic:** benannter Kanal (`chatter`, `/temperature`). **Publisher:** veröffentlicht Nachrichten auf einem Topic. **Subscriber:** abonniert ein Topic, bekommt pro Nachricht einen **Callback**. **Message:** typisierte Datenstruktur (z. B. `std_msgs/String`, `geometry_msgs/Point`), definiert in einer **IDL** (`.msg`). **`spin`:** Ereignisschleife, die auf Nachrichten/Timer wartet und Callbacks aufruft.

**C2.2 Welchem Architekturstil und welcher Kommunikationsart entspricht das ROS-Beispiel?**

> **Ereignisbasierter Stil** (Publish/Subscribe), **lockere Kopplung**: Publisher und Subscriber kennen **nur das Topic**, nicht einander. **Nachrichtenorientiert**, **asynchron**, 1-zu-n (Multicast-artig). ROS wird in der Vorlesung zu den Nachrichtenwarteschlangensystemen gezählt. Ob Nachrichten **persistent** gehalten werden, hängt von der QoS-Einstellung ab (Standard: nicht für später startende Subscriber).

**C2.3 Was bedeutet die `10` in `create_publisher(String, "chatter", 10)`?**

> **Warteschlangenlänge (QoS-History-Tiefe)**: bis zu 10 Nachrichten werden zwischengepuffert. Ist ein Empfänger langsamer, werden **ältere Nachrichten verworfen**.

**C2.4 Was passiert, wenn der Subscriber später als der Publisher startet bzw. gar nicht läuft?**

> Der Publisher läuft **unabhängig** weiter (zeitliche Entkopplung auf Sender-Seite, kein Blockieren). Mit Standard-QoS gehen **vor dem Start gesendete Nachrichten verloren**; der Subscriber sieht nur Nachrichten ab seiner Anmeldung. Gegensatz zu RPC, wo der Server aktiv sein müsste.

**C2.5 Ihr Aggregator abonniert drei Topics. Welche Eigenschaften hat dieser Knoten (Zustand, Rolle, Schwächen)?**

> Er ist **zustandsbehaftet** (hält die zuletzt bekannten Werte), ist **Subscriber für drei Topics** (Zusammenführung), und als **zentraler Knoten** ein **Single Point of Failure** und möglicher **Flaschenhals**. Das entspricht einer **zentralisierten** Sicht. Gegenmittel: mehrere Aggregatoren (Replikation) oder Peer-Auswertung.

**C2.6 Warum ist der „Snapshot“ der letzten Werte nicht automatisch konsistent?**

> Die Sensoren senden **zu unterschiedlichen Zeitpunkten und Raten**. Der Snapshot mischt Werte aus **verschiedenen Momenten**. Für eine echte zeitliche Zuordnung braucht man **Zeitstempel** und **synchronisierte Uhren** (→ NTP) bzw. logische Ordnung (→ Lamport).

**C2.7 Welche Rolle spielt der Timer im Producer, und welchem Konzept der Vorlesung entspricht der Callback beim Subscriber?**

> Der Timer löst periodisch (1 Hz) die Veröffentlichung aus. Der Callback beim Subscriber entspricht dem **Notify-Mechanismus** von Nachrichtenwarteschlangen (**automatische Bearbeitung durch registrierte Funktionen**), im Gegensatz zu **Get** (blockierend) oder **Poll**.

**C2.8 Wie sieht Verteilungstransparenz in ROS aus?**

> Verortungstransparenz: Topic-Namen statt Rechneradressen. Der Publisher weiß nicht, **wo** oder **wie viele** Subscriber existieren. Die Middleware (bei ROS 2 DDS-basiert) übernimmt Entdeckung, Serialisierung und Zustellung.

---

#### C3. Übung 3: Threads in Python (Prozesse, Skalierung)

**C3.1 Warum nutzt man Threads statt Prozessen, und was ist der Preis?**

> Threads haben **geringen Overhead** (nur CPU-Kontext) und **teilen den Speicher** (einfache Kommunikation). Preis: **Synchronisation** nötig (Race Conditions), keine Isolation: ein Fehler kann den ganzen Prozess treffen.

**C3.2 Was ist der Idealfall, wenn jeder Thread die gleiche Arbeit macht, und wie lässt sich „Effizienzsteigerung“ messen?**

> Jeder Thread führt dieselbe Operation aus. **Perfekte Parallelität** ⇒ die **Gesamtlaufzeit bleibt konstant**, wenn die Threadzahl wächst (jeder Thread läuft auf eigenem Kern/eigener Wartezeit). Wächst die Laufzeit ≈ proportional zur Threadzahl (n · t<sub>1</sub>), gibt es **keinen Parallelitätsgewinn**. Effizienz bis zu der Threadzahl, ab der die Laufzeit zu steigen beginnt.

**C3.3 Was erwarten Sie für die CPU-intensive Operation und warum?**

> In **CPython** erlaubt die **Global Interpreter Lock (GIL)**, dass nur **ein Thread gleichzeitig Python-Bytecode** ausführt. Reine Rechenschleifen laufen daher **nicht parallel**: die Laufzeit wächst ≈ linear mit der Threadanzahl, selbst bei vielen Kernen. (Echte Parallelität: `multiprocessing`, C-Erweiterungen, Free-Threaded-Python-Builds.)

**C3.4 Was erwarten Sie für die I/O-intensive Operation (hashlib über große Datei)?**

> Typischerweise **gewisser Gewinn**: Dateilesen gibt die GIL frei, und `hashlib` gibt sie bei großen Datenblöcken ebenfalls frei. Der Gewinn endet bei der **Kernanzahl** bzw. der **Speicher-/Plattenbandbreite**. *Messen:* Der **Page-Cache** verfälscht Ergebnisse (zweiter Lauf liest aus RAM), siehe [9.3](#93-übung-3--threads-messen).

**C3.5 Was erwarten Sie für die netzwerkintensive Operation (HTTP-Requests) und warum?**

> **Starker Gewinn**, weil **Latenz dominiert**: Threads **überlagern Wartezeiten** (blockierende Systemaufrufe geben die GIL frei). Das entspricht „**Latenzen verstecken**“ und dem Browser-Beispiel. Grenzen: **Bandbreite**, Serverlast, Rate-Limits, Overhead.

**C3.6 Warum fordert die Aufgabe, dass die Laufzeit eines Threads einige Sekunden beträgt?**

> Damit **Thread-Erzeugung und -Start (Overhead)** gegenüber der eigentlichen Arbeit **vernachlässigbar** sind und Messschwankungen klein bleiben.

---

#### C4. Übung 4: gRPC mit Python und C++ (Kommunikation, RPC)

**C4.1 Was passiert beim Aufruf von `protoc`/`grpc_tools.protoc`, und welche Dateien entstehen?**

> Der Compiler erzeugt aus der **IDL** (`.proto`) die **Stubs**. In Python: `hello_pb2.py` (**Nachrichtenklassen**, Serialisierung/Marshaling) und `hello_pb2_grpc.py` (**Client-Stub** `GreeterStub`, **Server-Basisklasse** `GreeterServicer`, `add_GreeterServicer_to_server`). In C++: `.pb.h/.pb.cc` und `.grpc.pb.h/.grpc.pb.cc`. → Praxis der **automatischen Stub-Generierung**.

**C4.2 Ordnen Sie die Bestandteile des Beispiels den RPC-Begriffen zu.**

> `GreeterStub` = **Client-Stub**; `Greeter(GreeterServicer)` bzw. `add_..._to_server` = **Server-Stub + Server-Implementierung**; `hello.proto` = **IDL**; `HelloRequest`/`HelloReply` = **Parameter/Ergebnis (Marshaling)**; `insecure_channel` = **Verbindung** (HTTP/2); `stub.SayHello(...)` = **synchroner** (blockierender) Aufruf.

**C4.3 Wozu dienen die Feldnummern (`= 1`, `= 2`) in einer `.proto`-Datei?**

> Sie identifizieren die Felder im **binären Wire-Format** (statt Feldnamen). Sie dürfen daher **nicht geändert** werden, wenn Sender und Empfänger unterschiedliche Versionen nutzen → **Abwärtskompatibilität/Erweiterbarkeit** (Offenheit).

**C4.4 Wie bilden Sie in Protobuf ab: Integer/Float/Bool, Listen, Enum, Klasse, Liste von Klassen?**

> `int32`/`float`/`bool`; **`repeated`** für Listen; **`enum`** (erster Wert muss `0` sein); **`message`** für Klassen-Datenstrukturen (Verschachtelung durch Verwendung als Feldtyp); `repeated Robot robots = 1;` für Listen von Klassen. Beispiel: [9.4](#94-übung-4--grpc-python--c).

**C4.5 Warum können Python-Client und C++-Server zusammenarbeiten (Interoperabilität)?**

> Weil beide nur die **gemeinsame, plattformunabhängige IDL** und das **Protobuf-Wire-Format über HTTP/2** brauchen. Endianness, Datentypgrößen und Sprachunterschiede (**Heterogenität**) löst das **Marshaling** der Stubs. Das ist genau das Hauptproblem bei Wertparametern aus der Vorlesung.

**C4.6 Wie werden Pointer/Referenzen in gRPC behandelt?**

> Es gibt **keine Referenzen über Prozessgrenzen**: Nachrichten werden **per Wert** serialisiert, verschachtelte Messages werden komplett mitkopiert. Das ist die Strategie „**referenzierte Werte explizit übertragen**“ aus der Vorlesung (verkettete Listen müssten als `repeated` abgeflacht werden).

**C4.7 Wozu `ThreadPoolExecutor(max_workers=10)` im Server?**

> Der Server ist **nebenläufig (multithreaded)**: bis zu 10 Anfragen gleichzeitig in **Worker-Threads**. Entspricht dem **Dispatcher/Worker**-Modell.

**C4.8 Was bedeutet `insecure`, und welche Fehlannahme steckt dahinter?**

> Die Verbindung ist **unverschlüsselt/unauthentifiziert** (kein TLS). Für lokale Tests ok, produktiv verletzt es die Annahme „**das Netzwerk ist sicher**“ (Fehlannahme Nr. 2).

**C4.9 Was passiert, wenn der Server nicht läuft? Welcher RPC-Fehlerklasse entspricht das?**

> Der Client bekommt einen Fehler (Python: `grpc.RpcError` mit `StatusCode.UNAVAILABLE`; C++: `status.error_code()`, im Beispiel „RPC failed“). Entspricht **Fehlerklasse 1: Client kann Server nicht finden**, die Behandlung ist **Fehler rückmelden**.

---

### Teil D: Rechen- und Skizzenaufgaben

**D1. NTP.** `★★★` Ein Client misst (alle Zeiten in ms): T1 = 1000, T2 = 1090, T3 = 1095, T4 = 1105. Berechnen Sie tDelay und tOffset. Geht die Client-Uhr zu schnell oder zu langsam?

> tDelay = ((1105 − 1000) − (1095 − 1090)) / 2 = (105 − 5) / 2 = **50 ms**.
> tOffset = 1095 + 50 − 1105 = **+40 ms** > 0 → Uhr des Clients geht **40 ms nach (zu langsam)**. Anpassung: Systemzeit pro Tick etwas **größer** erhöhen (z. B. 11 statt 10 ms).

**D2. NTP (negativer Offset).** `★★★` T1 = 0, T2 = 30, T3 = 35, T4 = 105 (ms).

> tDelay = ((105 − 0) − (35 − 30)) / 2 = **50 ms**. tOffset = 35 + 50 − 105 = **−20 ms** < 0 → Client-Uhr geht **20 ms vor (zu schnell)**. Anpassung: Tick **kleiner** (z. B. 9 ms).

**D3. Lamport-Uhren.** `★★` Drei Prozesse mit **unsynchronisierten** Startwerten C1 = 4, C2 = 0, C3 = 9. Ablauf: (1) P1 sendet m1 an P2. (2) P2 empfängt m1. (3) P2 sendet m2 an P3. (4) P3 empfängt m2. (5) P3 sendet m3 an P1. (6) P1 empfängt m3. Geben Sie alle Zählerstände an und sagen Sie, bei welchen Empfangsereignissen die Korrektur (`max`) wirkt.

> (1) C1 = 5, ts(m1) = 5. (2) C2 = max(0, 5) + 1 = **6** (Korrektur wirkt: 5 > 0). (3) C2 = 7, ts(m2) = 7. (4) C3 = max(9, 7) + 1 = **10** (keine Korrektur nötig: 9 > 7). (5) C3 = 11, ts(m3) = 11. (6) C1 = max(5, 11) + 1 = **12** (Korrektur wirkt).
> Endstände: C1 = 12, C2 = 7, C3 = 11.

**D4. Vollständig geordneter Multicast.** `★★` P1 sendet bei T1 = 3, P2 bei T2 = 3 und P3 bei T3 = 2 je einen Multicast. In welcher Reihenfolge werden die Nachrichten überall ausgeliefert?

> Zeitstempel (Zähler.Prozessnummer): P1 → **3.1**, P2 → **3.2**, P3 → **2.3**. Sortierung: **2.3, 3.1, 3.2**. Jede Nachricht wird ausgeliefert, sobald sie am Kopf der Warteschlange steht und von allen bestätigt wurde.

**D5. Bully-Algorithmus.** `★★` Prozesse 1–7, Koordinator **7** und Prozess **5** sind ausgefallen. P2 bemerkt den Ausfall von 7. Wer wird Koordinator? Skizzieren Sie den Ablauf.

> P2 sendet ELECTION an 3, 4, 5, 6, 7. **3, 4, 6** antworten OK (5, 7 nicht). Diese starten eigene Wahlen: P3 → 4, 5, 6, 7 (4, 6 antworten), P4 → 5, 6, 7 (6 antwortet), P6 → 7 (**keine Antwort**). **P6 wird Koordinator** (höchste aktive ID) und sendet **COORDINATOR** an alle.

**D6. Ring-Algorithmus.** `★★` Ring (Nachfolgerreihenfolge): 1 → 5 → 3 → 2 → 6 → 4 → (zurück zu 1). **P3** ist ausgefallen. P1 startet die Wahl. Welche Liste trägt die Nachricht, wer wird Koordinator?

> Die Nachricht startet mit [1] → P5: [1,5] → (P3 wird **übersprungen**) → P2: [1,5,2] → P6: [1,5,2,6] → P4: [1,5,2,6,4] → P1 erkennt die eigene ID. Koordinator = **6**. COORDINATOR(6) läuft einmal um den Ring.

**D7. Server-Cluster.** `★★★` Jeder Server fällt unabhängig mit p = 0,1 % aus. Wie hoch ist die Wahrscheinlichkeit, dass **kein** Server ausgefallen ist, bei N = 100, 1000 und 5000?

> (1 − p)<sup>N</sup>: N = 100 → 0,999<sup>100</sup> ≈ **90,5 %**; N = 1000 → ≈ **36,8 %**; N = 5000 → ≈ **0,7 %**. Je größer der Cluster, desto normaler sind Teilausfälle → **automatisches Management/Self-Healing** nötig.

**D8. Datenstrom.** `★★` Berechnen Sie die Datenrate eines Audiostroms mit 44,1 kHz, 16 Bit, Stereo, sowie die Datenmenge für 1 Minute. Wie hoch wäre sie bei 48 kHz, 24 Bit, 6 Kanälen?

> 44 100 · 16 Bit · 2 = 1 411 200 Bit/s = **176,4 KB/s**. 1 min = 60 · 176 400 B ≈ **10,6 MB**.
> 48 000 · 24 · 6 = 6 912 000 Bit/s = **864 KB/s**.

**D9. Prozessgruppen.** `★★` Wie viele Prozesse braucht eine Gruppe, wenn sie (a) 2 Prozessausfälle (Abstürze), (b) 2 fehlerhafte (willkürlich antwortende) Prozesse verbergen soll?

> (a) k + 1 = **3**. (b) 2k + 1 = **5** (3 korrekte stimmen die 2 fehlerhaften per Mehrheit nieder).

**D10. Dezentraler gegenseitiger Ausschluss.** `★★` n = 5 Koordinatoren. Wie viele Zustimmungen braucht ein Prozess mindestens? Warum genügt nicht m = 2?

> m > n/2 = 2,5 → mindestens **m = 3**. Mit m = 2 könnten zwei Prozesse **gleichzeitig** je 2 Zustimmungen erhalten (2 + 2 ≤ 5), die Mehrheit garantiert, dass sich zwei Mengen **überlappen** und nur einer gewinnt.

**D11. Dezentraler Algorithmus: Reset-Wahrscheinlichkeit.** `★★` T = 3 h, ∆t = 10 s. Wie groß ist p = ∆t/T?

> p = 10 s / 10 800 s ≈ 9,3 · 10<sup>−4</sup> ≈ **0,093 %** (auf der Folie steht „0,92 %“, das ist ein Faktor-10-Fehler, siehe [Kap. 11](#11-korrekturen-und-unstimmigkeiten-im-material)). Die Schlussfolgerung (Regelverletzung extrem unwahrscheinlich) bleibt gleich.

**D12. Konsistenz.** `★★` Gegeben: P1: W(x)a, P2: W(x)b (unabhängig). P3 liest erst b, dann a. P4 liest erst a, dann b. Ist das sequentiell konsistent? Kausal konsistent?

> **Nicht sequentiell konsistent:** P3 und P4 sehen die Schreibvorgänge in **unterschiedlicher Reihenfolge**, es gibt keine einheitliche globale Reihenfolge. **Kausal konsistent: ja**, da W(x)a und W(x)b **nicht kausal abhängig** (P2 hat a nicht gelesen) und damit in beliebiger Reihenfolge sichtbar sein dürfen.

---

### Teil E: Wahr/Falsch-Schnelltest

| # | Aussage | W/F | Begründung |
|---|---|---|---|
| 1 | Ein verteiltes System erscheint dem Nutzer als mehrere unabhängige Systeme. | **F** | Es erscheint als **ein** zusammenhängendes System. |
| 2 | Caching wird vom Ressourcenbesitzer geplant, Replikation vom Client. | **F** | Umgekehrt: **Replikation** = Besitzer/geplant, **Caching** = Client/auf Abruf. |
| 3 | „Latenz ist 0“ ist eine der 8 Fehlannahmen. | **W** | |
| 4 | In einer Schichtenarchitektur darf Schicht L<sub>i</sub> beliebige andere Schichten aufrufen. | **F** | Nur L<sub>i−1</sub>. |
| 5 | Horizontale Verteilung bedeutet Aufteilung in logische Schichten auf verschiedene Rechner. | **F** | Das ist **vertikal**. Horizontal = gleichartige Teile (z. B. P2P). |
| 6 | Threads teilen sich den Speicher, daher ist Synchronisation nötig. | **W** | |
| 7 | Ein Webserver ist typischerweise zustandsbehaftet. | **F** | Er ist **zustandslos** (vergisst den Client). |
| 8 | Beim RPC verpackt der Client-Stub die Parameter („Marshaling“). | **W** | |
| 9 | Pointer können beim RPC problemlos als Zahlenwert übergeben werden. | **F** | Gelten nur im Adressraum des Prozesses. |
| 10 | Bei persistenter Kommunikation müssen Sender und Empfänger gleichzeitig laufen. | **F** | Das gilt für **transiente**. |
| 11 | Bei NTP bedeutet tOffset < 0, dass die Client-Uhr zu schnell geht. | **W** | |
| 12 | Eine NTP-Uhr wird bei Abweichung sofort auf die neue Zeit gesetzt. | **F** | **Graduelle** Anpassung, nie zurücksetzen. |
| 13 | Lamport-Uhren garantieren: C(a) < C(b) ⇒ a → b. | **F** | Nur a → b ⇒ C(a) < C(b). |
| 14 | Beim zentralisierten Algorithmus ist der Koordinator ein Single Point of Failure. | **W** | |
| 15 | Der Bully-Algorithmus wählt den Prozess mit der niedrigsten ID. | **F** | **Höchste** ID. |
| 16 | Replikation erhöht Zuverlässigkeit und Leistung, kann aber Inkonsistenz verursachen. | **W** | |
| 17 | Monotones Lesen garantiert, dass nie ein älterer Wert als zuvor gelesen wird. | **W** | |
| 18 | Eine Fehlursache ist der Zustand, der zu einem Ausfall führen kann. | **F** | Das ist der **Fehler**; Fehlursache = Grund (z. B. defekte Hardware). |
| 19 | Ein Hamming-Code ist ein Beispiel für zeitliche Redundanz. | **F** | **Informationsredundanz**. |
| 20 | Eine Gruppe von 2k+1 Prozessen kann k fehlerhafte Prozesse verbergen. | **W** | Mehrheitsentscheid. |

---

## 9. Linux-Praxisteil

Die Übungsblätter haben je eine Windows- und eine Ubuntu-24.04-Anleitung. Dieses Kapitel fasst **alles für Linux** zusammen, korrigiert Stolpersteine und ergänzt Befehle zum Testen.

> **Was wurde getestet?** Die Python-Teile der Übungen 1, 3 und 4 (OpenAPI/connexion, Thread-Messung inkl. lokalem Testserver, gRPC-Proto mit allen Datentypen) habe ich in einer Linux-Umgebung ausgeführt. **ROS 2 (Übung 2) konnte ich hier nicht installieren**, die dortigen Befehle folgen deinem Übungsblatt und der Standard-`ros2`-CLI.

### 9.0 Grundausstattung

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip build-essential curl netcat-openbsd
```

- Das Übungsblatt zielt auf **Ubuntu 24.04 (Noble)**. Auf anderen Distributionen (Arch, Fedora, …) sind die **ROS-2-Binärpakete** das Problem. Dann am einfachsten einen **Ubuntu-24.04-Container** (Docker/Podman/Distrobox) verwenden. Alles andere (Python, gRPC, Threads) läuft überall.
- **Virtuelle Umgebung immer so:**

```bash
python3 -m venv .venv          # einmalig im Projektordner
source .venv/bin/activate      # bei jedem neuen Terminal ('source' nicht vergessen!)
deactivate                     # verlassen
```

> Unter Ubuntu 24.04 verweigert `pip install` außerhalb einer venv die Installation (`error: externally-managed-environment`). Das ist **gewollt** (PEP 668), die venv ist die Lösung. Die Windows-Teile der Blätter (pixi, `cmd`, `.bat`) entfallen komplett.

---

### 9.1 Übung 1 – OpenAPI-Taschenrechner

**a) Ausführen und testen**

```bash
mkdir -p ~/vs/uebung1 && cd ~/vs/uebung1
python3 -m venv .venv && source .venv/bin/activate
pip install "connexion[flask,swagger-ui,uvicorn]" requests
```

`calculator.yaml`:

```yaml
openapi: 3.0.1
info:
  title: Calculator API
  description: API für einen Taschenrechner
  version: 1.0.0
servers:
  - url: http://localhost:8000/
paths:
  /add:
    get:
      summary: Addiert zwei Zahlen
      operationId: app_calculator.add          # <Modulname>.<Funktion>
      parameters:
        - {in: query, name: a, schema: {type: integer}, required: true, description: Erste Zahl}
        - {in: query, name: b, schema: {type: integer}, required: true, description: Zweite Zahl}
      responses:
        '200':
          description: Ergebnis der Addition
          content:
            application/json:
              schema:
                type: object
                properties:
                  result: {type: integer}
```

`app_calculator.py`:

```python
import connexion

app = connexion.App(__name__, specification_dir=".")
app.add_api("calculator.yaml")

def add(a: int, b: int) -> dict:
    return {"result": a + b}

if __name__ == "__main__":
    app.app.debug = True
    app.run(host="localhost", port=8000)
```

```bash
python3 app_calculator.py                      # Terminal 1: Server starten

curl "http://localhost:8000/add?a=2&b=3"       # Terminal 2: Test -> {"result": 5}
curl -s "http://localhost:8000/add?a=2&b=x"    # falsche Eingabe -> 400 (Validierung gegen die Spezifikation)
xdg-open http://localhost:8000/ui/             # Swagger-UI im Browser (interaktives Testen)
```

**Stolpersteine:**

- Getestet mit **connexion 3.x**. Dort braucht man die Extras `flask`, `swagger-ui` und `uvicorn` (sonst `ImportError`). Bei älteren 2.x-Versionen genügt `connexion[swagger-ui]`.
- Die Vorlesungsfolie nennt `operationId: app-calculator.add` (Datei mit Bindestrich). Besser **Unterstriche** verwenden (`app_calculator.py`), das ist ein gültiger Python-Modulname.
- Port belegt? `ss -tlnp | grep 8000` zeigt, wer ihn nutzt.

**b) Erweitern:** pro Operation einen weiteren Eintrag unter `paths` (`/sub`, `/mul`, `/div`, …) mit eigener `operationId` und die zugehörige Funktion in Python. Fehlerfall (Division durch 0) als **`400`-Response** in der YAML beschreiben.

**c) Minimaler Client:**

```python
import requests

a = int(input("a: "))
b = int(input("b: "))
r = requests.get("http://localhost:8000/add", params={"a": a, "b": b}, timeout=5)
r.raise_for_status()
print("Ergebnis:", r.json()["result"])
```

**d) Zusatzschicht:** Cache mit `functools.lru_cache` oder einem `dict` (Variante A), Datenbank mit dem eingebauten **`sqlite3`**-Modul (Variante B). Konzeptfragen dazu: [C1.5/C1.6](#c1-übung-1-openapi-taschenrechner-einführung-offenheit-schichten).

---

### 9.2 Übung 2 – ROS 2 Publish/Subscribe

**Installation (Ubuntu 24.04, ROS 2 Kilted Kaiju)**, wie auf dem Blatt, plus fehlendes `apt update`:

```bash
cd /tmp
wget https://github.com/ros-infrastructure/ros-apt-source/releases/download/1.1.0/ros2-apt-source_1.1.0.noble_all.deb
sudo dpkg -i ros2-apt-source_1.1.0.noble_all.deb
sudo apt update                                          # fehlt auf dem Blatt, wird nach dem Hinzufügen der Paketquelle gebraucht
sudo apt install ros-kilted-ros-base ros-kilted-demo-nodes-py
```

Für Aufgabe 2c (`rqt_plot`/`rqt_gui`) zusätzlich (**ros-base enthält keine GUI-Werkzeuge**):

```bash
sudo apt install ros-kilted-rqt ros-kilted-rqt-plot     # alternativ: ros-kilted-desktop (groß)
apt search rqt-plot                                      # falls ein Paketname abweicht
```

**Umgebung einrichten (in *jedem* neuen Terminal!):**

```bash
source /opt/ros/kilted/setup.bash        # zsh: setup.zsh
ros2                                     # Hilfe -> Installation ok
```

Optional dauerhaft: `echo 'source /opt/ros/kilted/setup.bash' >> ~/.bashrc`.

**Demo testen (zwei Terminals, jeweils sourcen):**

```bash
ros2 run demo_nodes_py talker            # Terminal 1: Publisher
ros2 run demo_nodes_py listener          # Terminal 2: Subscriber
```

**Eigene Knoten (`producer.py`, `consumer.py`):**

```bash
source /opt/ros/kilted/setup.bash
python3 producer.py                      # Terminal 1
python3 consumer.py                      # Terminal 2
```

> **Wichtig:**
> - `python3` statt `python` aufrufen. Das Skript `producer.py` hat den Shebang `#!/usr/bin/env python`, und ein Programm namens `python` gibt es unter Ubuntu 24.04 standardmäßig nicht. Entweder `python3 producer.py` nutzen oder den Shebang auf `python3` ändern (dann `chmod +x producer.py && ./producer.py`).
> - Die ROS-Python-Pakete (`rclpy`) liegen im **System-Python**. Die ROS-Knoten also **nicht** in der gRPC-venv ausführen (`ModuleNotFoundError: No module named 'rclpy'`). Wer eine venv will: `python3 -m venv --system-site-packages .venv`.
> - `with rclpy.init():` (Context-Manager) ist in Kilted möglich. Bei älteren Distributionen (Humble/Jazzy) klassisch `rclpy.init()` … `rclpy.shutdown()` verwenden.
> - Beim Kopieren aus dem PDF auf die **Einrückung** achten (Python reagiert auf jedes Leerzeichen).

**Nützliche `ros2`-Kommandos (zum Verstehen und Debuggen):**

```bash
ros2 node list                           # laufende Knoten
ros2 topic list                          # vorhandene Topics (/chatter, /temperature, ...)
ros2 topic info /chatter                 # Nachrichtentyp, Anzahl Publisher/Subscriber
ros2 topic echo /chatter                 # Nachrichten live mitlesen
ros2 topic hz /chatter                   # Veröffentlichungsrate (hier ~1 Hz)
ros2 interface show std_msgs/msg/String          # Nachrichtendefinition (die IDL!)
ros2 interface show geometry_msgs/msg/Point
rqt_graph                                # Graph: Knoten <-> Topics
```

**Hinweise zu Aufgabe 2:**

- Nachrichtentypen: `std_msgs.msg.Float32` (Temperatur), `std_msgs.msg.String` (Status), `geometry_msgs.msg.Point` (Position: Felder `x`, `y`, `z`).
- Der Aggregator braucht **drei** `create_subscription(...)` mit je eigenem Callback, der den **letzten Wert in einem Attribut** speichert. Ausgabe periodisch per Timer oder bei jedem Callback.
- **Warnungen (2c):** Der ROS-Logger färbt im Terminal automatisch, `self.get_logger().warn("…")` erscheint gelb, `.error("…")` rot. Alternativ ANSI-Codes: `print("\033[91mWARNUNG\033[0m")` (unter Linux nativ).
- **rqt_plot:** `rqt_plot /temperature/data /position/x /position/y` (Plot-Pfade = `Topic/Feld`). Der String-Status lässt sich nicht plotten.
- **Mehrere Rechner/Netzwerk:** Knoten im selben Netz finden sich automatisch. Um Störungen durch andere (z. B. im Hochschulnetz) zu vermeiden: `export ROS_DOMAIN_ID=42` (gleicher Wert in allen Terminals). Nur lokal: `export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` (ältere Distributionen: `ROS_LOCALHOST_ONLY=1`).
- Mehrere Knoten bequem starten: mehrere Terminals oder `tmux`.

---

### 9.3 Übung 3 – Threads messen

**Vorbereitung:**

```bash
nproc                                              # Anzahl der CPU-Kerne (wichtig für die Auswertung!)
lscpu | grep -E "Model name|^CPU\(s\)|Thread|Core"
python3 -m venv .venv && source .venv/bin/activate
pip install requests matplotlib
```

**Messgerüst:**

```python
import threading, time

def run_threads(work, n):
    """Startet n Threads, die jeweils work() ausführen, und liefert die Gesamtlaufzeit in s."""
    threads = [threading.Thread(target=work) for _ in range(n)]
    t0 = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    return time.perf_counter() - t0
```

Für jede der drei Operationstypen `run_threads(work, n)` mit n = 1, 2, 4, 8, 16, … aufrufen, mehrfach wiederholen (z. B. Median bilden) und mit `matplotlib` plotten (`plt.savefig("laufzeiten.png")`; ohne Display vorher `matplotlib.use("Agg")`).

**CPU-intensiv:** Rechenschleife (z. B. Potenzieren in `while`) mit fester Iterationszahl, die bei **einem** Thread einige Sekunden dauert.
**I/O-intensiv:** große Testdatei erzeugen und blockweise hashen:

```bash
head -c 512M /dev/urandom > big.bin       # oder: dd if=/dev/urandom of=big.bin bs=1M count=512 status=progress
time sha256sum big.bin                     # Referenzzeit (ein Prozess)
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches   # Page-Cache leeren, damit wirklich von Platte gelesen wird
```

> Nach dem ersten Lauf liegt die Datei im **Page-Cache** (RAM). Spätere Läufe messen dann kaum noch Plattenzugriffe. Für saubere Messungen vor jedem Lauf den Cache leeren oder die Wirkung bewusst diskutieren.

**Netzwerk-intensiv: nicht auf fremde Server schießen!** Besser einen **lokalen Testserver mit künstlicher Latenz** (getestet):

```python
# slow_server.py : python3 slow_server.py
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(0.2)                      # künstliche Latenz: 200 ms
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):            # Konsole nicht fluten
        pass

ThreadingHTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
```

Der Client-Thread führt dann z. B. 10 × `requests.get("http://127.0.0.1:8080/")` mit einer `requests.Session()` aus.

**Beobachten:**

```bash
htop                          # F2/Spalten: CPU je Kern. Bei reinem Python-CPU-Test siehst du ~1 Kern ausgelastet (GIL)
taskset -c 0 python3 test.py  # Programm auf einen Kern festnageln (Vergleichsmessung)
```

**Erwartung (und gemessene Beispielwerte aus meinem Test):**

| Operation | Erwartung | Begründung |
|---|---|---|
| **CPU (reines Python)** | Laufzeit wächst ≈ **linear** mit der Threadanzahl, **kein** Gewinn | **GIL**: nur ein Thread führt Bytecode aus |
| **I/O / hashlib** | Gewinn **bis ca. Kernanzahl**, danach Plateau/Anstieg | GIL wird beim Lesen/Hashen großer Blöcke freigegeben (typisch, selbst messen); Platten-/RAM-Bandbreite begrenzt |
| **Netzwerk** | Laufzeit bleibt ≈ **konstant**, bis Bandbreite/Server limitiert | Threads **überlagern Wartezeiten** („Latenzen verstecken“) |

*Meine Messung (lokaler Testserver, 200 ms Latenz, 10 Requests/Thread):* 1, 2, 4, 8 und 16 Threads brauchten jeweils **≈ 2,0 s** (also 16-fache Gesamtarbeit in gleicher Zeit). *Reines CPU-Python* auf einer Umgebung mit 1 Kern: Laufzeit ∝ Threadanzahl (0,12 s → 0,25 s → 0,47 s für 1/2/4 Threads).

> Dein Ergebnis hängt von **Kernanzahl, Python-Version (GIL-Build vs. optionaler Free-Threaded-Build), Festplatte und Netzwerk** ab. Bei der Auswertung also immer `nproc` und Python-Version angeben.

---

### 9.4 Übung 4 – gRPC (Python + C++)

#### Python (Aufgabe 1 und 2)

```bash
mkdir -p ~/vs/uebung4 && cd ~/vs/uebung4
python3 -m venv .venv
source .venv/bin/activate                  # Blatt-Fehler: dort fehlt 'source'!
pip install grpcio-tools                   # bringt grpcio + protobuf mit

# hello.proto, server.py, client.py wie auf dem Blatt anlegen, dann Stubs erzeugen:
chmod +x gen.sh && ./gen.sh                # gen.sh = das 'Kommando'-Skript des Blatts
# oder direkt:
rm -rf generated && mkdir generated
python3 -m grpc_tools.protoc -I. --python_out=generated --grpc_python_out=generated hello.proto

python3 server.py                          # Terminal 1
python3 client.py                          # Terminal 2 -> "Greeter client received: Hello, Google!"
ss -tlnp | grep 50051                      # prüfen, ob der Server lauscht
```

**Aufgabe 2: Datentypen in Protobuf** (ausprobiert und kompiliert, z. B. als `robot.proto`):

```proto
syntax = "proto3";

service Demo {
  rpc Send (Inventory) returns (Ack) {}
}

enum Status {                        // c) Aufzählungstyp
  STATUS_UNKNOWN = 0;                // proto3: erster Wert muss 0 sein
  STATUS_IDLE    = 1;
  STATUS_MOVING  = 2;
}

message Point {                      // d) "Klassen"-Datenstruktur
  float x = 1;
  float y = 2;
}

message Robot {
  int32  id      = 1;                // a) Integer
  float  battery = 2;                //    Float
  bool   active  = 3;                //    Bool
  Status status  = 4;                // c) Enum
  Point  position = 5;               // d) verschachtelte Message
  repeated float temperatures = 6;   // b) Liste von Basisdatentypen
}

message Inventory {
  repeated Robot robots = 1;         // e) Liste von Klassen mit Basis- und Enum-Feldern
}

message Ack { bool ok = 1; }
```

Nutzung in Python (getestet):

```python
import sys; sys.path.append("generated")
import robot_pb2 as pb

inv = pb.Inventory(robots=[
    pb.Robot(id=1, battery=0.5, active=True, status=pb.STATUS_MOVING,
             position=pb.Point(x=1.2, y=-0.8), temperatures=[20.5, 21.0])
])
data = inv.SerializeToString()            # Marshaling -> Bytes (hier nur 35 Byte)
print(pb.Inventory.FromString(data).robots[0].status)   # Unmarshaling
```

#### C++ (Aufgabe 3)

```bash
sudo apt install protobuf-compiler protobuf-compiler-grpc libgrpc++-dev build-essential pkg-config

rm -rf generated_cpp && mkdir generated_cpp
protoc -I. --grpc_out=generated_cpp --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` hello.proto
protoc -I. --cpp_out=generated_cpp hello.proto

c++ -Igenerated_cpp -o server server.cpp generated_cpp/hello.grpc.pb.cc generated_cpp/hello.pb.cc \
    -lgrpc++ -lprotobuf -lgpr -labsl_synchronization -lpthread -ldl -lz
c++ -Igenerated_cpp -o client client.cpp generated_cpp/hello.grpc.pb.cc generated_cpp/hello.pb.cc \
    -lgrpc++ -lprotobuf -lgpr -labsl_synchronization -lpthread -ldl -lz
```

- **Aufpassen:** Der Hinweis auf dem Blatt („gRPC für Python installieren“) meint hier die **C++-Pakete** oben.
- Gibt es Linker-/Standardfehler, helfen `-std=c++17` und/oder `$(pkg-config --cflags --libs grpc++ protobuf)` statt der manuellen `-l…`-Liste (falls die `.pc`-Dateien installiert sind).
- Die C++-API für die Typen aus Aufgabe 2 (generierter Code, Setter/Adder):

```cpp
Inventory inv;
Robot* r = inv.add_robots();            // repeated Message -> add_...()
r->set_id(1);                           // int32
r->set_battery(0.5f);                   // float
r->set_active(true);                    // bool
r->set_status(STATUS_MOVING);           // enum
r->mutable_position()->set_x(1.2f);     // verschachtelte Message -> mutable_...()
r->add_temperatures(20.5f);             // repeated float -> add_...()
```

**Interoperabilität (c):** Zuerst `python3 server.py`, dann `./client` (C++), danach umgekehrt (`./server`, `python3 client.py`). Beide benutzen **dieselbe `.proto`-Datei** und Port 50051. Nur ein Server gleichzeitig (sonst *Address already in use*).

---

### 9.5 Vorlesungsdemos unter Linux

**Sockets (Iterativer/nebenläufiger Server, Vorlesung 3):**

```bash
python3 iterative.py                 # Terminal 1  (Port 12345)
nc 127.0.0.1 12345                   # Terminal 2: Text tippen -> Server gibt "Empfangen: ..." aus
nc 127.0.0.1 12345                   # Terminal 3: beim iterativen Server hängt dieser Client, bis Client 2 beendet ist
```

Dasselbe mit `concurrent_threads.py` und `concurrent_fork.py`: **beide Clients werden gleichzeitig bedient.** Zum Beobachten:

```bash
ss -tnp | grep 12345                 # Verbindungen
ps --forest -o pid,ppid,cmd          # beim Fork-Server: Kindprozesse unter dem Server
pstree -p                            # alternative Prozessbaum-Ansicht
```

> `os.fork()` gibt es nur auf **Unix/Linux** (nicht unter Windows), das ist auch der Grund, warum die Fork-Demo hier „einfach“ läuft. Startet man den Server nach Abbruch sofort neu, kann `Address already in use` kommen (TIME_WAIT). Abhilfe: kurz warten oder vor `bind` setzen: `server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)` (`from socket import SOL_SOCKET, SO_REUSEADDR`).

**MPI (Vorlesung 4):**

```bash
sudo apt install openmpi-bin libopenmpi-dev
pip install mpi4py                   # in einer venv, braucht mpicc (libopenmpi-dev)
mpiexec -n 4 python3 hello.py        # 4 Prozesse -> "Hallo von Prozess i von 4"
mpiexec -n 4 python3 pi.py           # π-Berechnung mit reduce
mpiexec --oversubscribe -n 8 python3 pi.py   # mehr Prozesse als Kerne
```

**NTP (Vorlesung 5):**

```bash
timedatectl timesync-status          # NTP-Server, Offset, Delay (systemd-timesyncd)
timedatectl status                   # "System clock synchronized: yes/no"
chronyc tracking                     # falls chrony statt timesyncd läuft (chronyc sources: Server und Stratum)
pip install ntplib && python3 ntp.py # Demo aus der Vorlesung
```

**gRPC-Demo (Vorlesung 4)** = Übung 4. **ROS-Demo (Vorlesung 2)** ist ROS 1, nimm stattdessen die ROS-2-Version aus Übung 2.

---

### 9.6 Typische Fehlermeldungen (Linux)

| Meldung | Ursache und Lösung |
|---|---|
| `error: externally-managed-environment` | `pip` außerhalb einer venv → `python3 -m venv .venv && source .venv/bin/activate` |
| `bash: .venv/bin/activate: Permission denied` | `source` vergessen (Blattfehler) → `source .venv/bin/activate` |
| `python: command not found` / `bad interpreter` | Nur `python3` vorhanden → `python3 …` oder Shebang ändern |
| `ros2: command not found` | `source /opt/ros/kilted/setup.bash` vergessen (in **jedem** Terminal) |
| `ModuleNotFoundError: No module named 'rclpy'` | ROS nicht gesourced oder Skript in einer venv ohne `--system-site-packages` gestartet |
| `E: Unable to locate package ros-kilted-…` | `sudo apt update` nach `dpkg -i ros2-apt-source…` fehlt, oder falsche Ubuntu-Version |
| `ModuleNotFoundError: No module named 'hello_pb2'` | Stubs nicht erzeugt bzw. `sys.path.append("generated")` fehlt/falscher Ordner |
| `StatusCode.UNAVAILABLE` (gRPC) | Server läuft nicht / falscher Port (Fehlerklasse „Server nicht gefunden“) |
| `OSError: [Errno 98] Address already in use` | Port noch belegt → `ss -tlnp \| grep <port>`, Prozess beenden, `SO_REUSEADDR` |
| rqt öffnet sich nicht (über SSH) | Kein Display → lokal ausführen oder `ssh -X` |
| `./producer.py: Permission denied` | `chmod +x producer.py` |
| ROS-Knoten sehen sich nicht | verschiedene `ROS_DOMAIN_ID`, Firewall/Netzwerk-Multicast, nicht gesourct |

---

## 10. Spickzettel

### 10.1 Formeln und Zahlen

| Thema | Formel / Wert |
|---|---|
| NTP Laufzeit | **tDelay = ((T4 − T1) − (T3 − T2)) / 2** |
| NTP Abweichung | **tOffset = T3 + tDelay − T4**; < 0 ⇒ Uhr **zu schnell**, > 0 ⇒ **zu langsam** |
| Lamport Senden | **C = C + 1**, Zeitstempel = C |
| Lamport Empfangen | **C = max(C, ts) + 1** |
| Eindeutige Zeitstempel | Zähler **.** Prozessnummer (z. B. 2.1) |
| Cluster ohne Ausfall | **(1 − p)<sup>N</sup>** (p = 0,1 %, N = 1000 ⇒ ≈ 36,8 %) |
| Mehrheit (dezentral) | **m > n/2** |
| Nachrichten Zentral / Verteilt | **3** / **2(n−1)** pro Zugriff |
| Prozessgruppe, Abstürze | **k + 1** Prozesse für **k** Ausfälle |
| Prozessgruppe, falsche Antworten | **2k + 1** Prozesse für **k** fehlerhafte |
| Audio 44,1 kHz / 16 Bit / Stereo | **176,4 KB/s** |
| Ports | HTTP 80 · HTTPS 443 · SSH 22 · DNS UDP 53 |

### 10.2 Aufzählungen zum Auswendiglernen

| Thema | Liste |
|---|---|
| **4 Ziele** | Ressourcen · Transparenz · Offenheit · Skalierbarkeit |
| **6 Transparenzen** | Zugriff · Verortung · Ortsveränderung · Replikation · Nebenläufigkeit · Störung |
| **4 Ziele der Offenheit** | Interoperabilität · Portabilität · Erweiterbarkeit · Flexibilität |
| **3 Skalierungsdimensionen** | Größe · Geografie · Verwaltung |
| **4 Skalierungstechniken** | Latenz verstecken · Aufteilen · Replizieren · Cachen |
| **4 Architekturstile** | Schichten · objektbasiert · ereignisbasiert · datenzentriert |
| **3 Schichten (interaktiv)** | Nutzerschnittstelle · Verarbeitung · Datenhaltung |
| **3 Systemarchitekturen** | zentralisiert · dezentralisiert · hybrid |
| **3 Virtualisierungsarten** | Process VM · VMM · Container |
| **4 Schnittstellen** | API · Systemaufruf · privilegierte Instruktion · allgemeine Instruktion |
| **3 Kommunikationsachsen** | persistent/transient · asynchron/synchron · diskret/Streaming |
| **4 Warteschlangen-Operationen** | Put · Get · Poll · Notify |
| **3 Strom-Modi** | asynchron · synchron · isochron |
| **4 Synchronisationsaufgaben** | reale Zeit · logische Zeit · gegenseitiger Ausschluss · Wahl |
| **4 Mutex-Algorithmen** | zentral · dezentral · verteilt · Token-Ring |
| **3 Replikatarten** | permanent · server-initiiert · client-initiiert |
| **3 Datenzentrierte Modelle** | kontinuierlich · sequentiell · kausal (+ strikt) |
| **5 Client-zentrierte Modelle** | eventual · monotones Lesen · monotones Schreiben · Read Your Writes · Writes Follow Reads |
| **4 Dependability** | Verfügbarkeit · Zuverlässigkeit · Sicherheit · Wartbarkeit |
| **3 Fehlerarten** | vorübergehend · intermittierend · dauerhaft |
| **3 Redundanzarten** | Information · Zeit · Physik |
| **2 Erholungsarten** | rückwärts · vorwärts (+ Checkpointing, Message Logging) |
| **ACID** | Atomar · Consistent · Isoliert · Dauerhaft |

### 10.3 Gegenüberstellungen

| Gegensatz | Links | Rechts |
|---|---|---|
| Prozess ↔ Thread | schwer, isoliert, IPC | leicht, gemeinsamer Speicher, Synchronisation |
| Replikation ↔ Caching | Besitzer, geplant | Client, auf Abruf |
| Vertikal ↔ Horizontal | Schichten auf verschiedene Rechner | gleichartige Teile nebeneinander |
| Zustandslos ↔ Zustandsbehaftet | einfach, robust (Webserver) | schnell, Wiederherstellung nötig (Dateiserver) |
| Iterativ ↔ Nebenläufig | Server arbeitet selbst nacheinander | Thread/Prozess pro Anfrage |
| Transient ↔ Persistent | beide müssen laufen | Zwischenspeicherung, zeitlich entkoppelt |
| RPC ↔ Nachrichten (MOM) | transparent, synchron, eng gekoppelt | sichtbar, asynchron, lose gekoppelt |
| Statisch ↔ Dynamisch (Kontaktpunkt) | schnell, begrenzt | flexibel, indirekt (Daemon/Superserver) |
| Schwache ↔ Starke Mobilität | nur Code | Code + Ausführungszustand |
| Push ↔ Pull | Server sendet (viele Lesezugriffe) | Client fragt (wenige Lesezugriffe) |
| Sequentiell ↔ Kausal | alle sehen **eine** Reihenfolge | nur **abhängige** Writes geordnet |
| Rückwärts ↔ Vorwärts | zurück zu altem Zustand | in neuen korrekten Zustand |
| Strukturiertes ↔ Unstrukturiertes P2P | deterministisch, DHT, Routing | zufällig, Nachbarlisten, Flooding |
| Cluster ↔ Grid | homogen, eine Domäne | heterogen, mehrere Domänen |
| Bully ↔ Ring | ELECTION an höhere IDs | ID-Liste wandert um den Ring |
| Verfügbarkeit ↔ Zuverlässigkeit | Anteil der Zeit „up“ | **kontinuierlich** ohne Ausfall |

### 10.4 Mini-Glossar Deutsch ↔ Englisch

| Deutsch | Englisch |
|---|---|
| Fehlursache / Fehler / Ausfall | fault / error / failure |
| Verfügbarkeit / Zuverlässigkeit | availability / reliability |
| Absturz-, Auslassungs-, Zeit-, Antwort-Fehler | crash, omission, timing, response failure |
| Willkürlicher Fehler | arbitrary / Byzantine failure |
| Gegenseitiger Ausschluss | mutual exclusion |
| Wahlalgorithmus / Koordinator | election algorithm / coordinator |
| Uhrenabweichung | clock skew |
| Schaltsekunde | leap second |
| Warteschlange / Nachrichtenvermittler | queue / message broker |
| Verteilte Hashtabelle | distributed hash table (DHT) |
| Zustandslos / zustandsbehaftet | stateless / stateful |
| Letztendliche Konsistenz | eventual consistency |
| Rückwärts-/Vorwärtserholung | backward / forward recovery |
| Datenpufferung / Verschachtelung | buffering / interleaving |
| Schnittstellenbeschreibungssprache | interface definition language (IDL) |
| Platzhalter-Prozedur | stub |
| Parameter verpacken | (parameter) marshaling |

---

## 11. Korrekturen und Unstimmigkeiten im Material

Beim Durcharbeiten sind mir diese Punkte aufgefallen. Die Lösungen im Lernzettel berücksichtigen sie bereits.

| # | Wo | Problem | Richtig / Empfehlung |
|---|---|---|---|
| 1 | **Vorlesung 5**, Folie „Dezentraler Algorithmus“ (26/37) | p = ∆t/T mit ∆t = 10 s, T = 3 h wird mit **≈ 0,92 %** angegeben | 10 s / 10 800 s ≈ **0,093 %** (≈ 9,3 · 10<sup>−4</sup>). Die Folgerung („sehr unwahrscheinlich“) bleibt gleich. |
| 2 | **Übung 4**, Installation Python unter Ubuntu, Schritt 3 | `.venv/bin/activate` (so würde ein Befehl „Permission denied“ liefern) | **`source .venv/bin/activate`** |
| 3 | **Übung 2**, Installation ROS 2 unter Ubuntu | Nach `sudo dpkg -i ros2-apt-source…deb` fehlt ein `sudo apt update` vor dem `apt install` | `sudo apt update` ergänzen |
| 4 | **Übung 2**, `ros-base` | enthält **keine** GUI-Werkzeuge, aber Aufgabe 2c verlangt `rqt_plot`/`rqt_gui` | zusätzlich `ros-kilted-rqt ros-kilted-rqt-plot` (oder `ros-kilted-desktop`) |
| 5 | **Übung 2**, `producer.py` | Shebang `#!/usr/bin/env python`, unter Ubuntu 24.04 gibt es standardmäßig nur `python3` (`consumer.py` nutzt bereits `python3`) | `python3 producer.py` oder Shebang anpassen |
| 6 | **Übung 2**, Codeblock `producer.py` | Im PDF ist `_callback` gegenüber `__init__` um ein Leerzeichen anders eingerückt, das führt beim Kopieren zu `IndentationError` | Einrückung prüfen/angleichen (ggf. nur Darstellungsproblem) |
| 7 | **Vorlesung 2** (ROS-Demo) vs. **Übung 2** | Folie: **ROS 1** (`rospy`, `roscore`), Übung: **ROS 2** (`rclpy`, Context-Manager `rclpy.init()`) | Konzept (Publish/Subscribe, Topics) identisch, Syntax unterschiedlich |
| 8 | **Vorlesung 2**, Folienüberschrift „Fine Clients vs. Fat Clients“ | Vermutlich Tippfehler | gemeint: **Thin** Clients vs. Fat Clients |
| 9 | **Übung 4**, Aufgabe 3 | Hinweis „gRPC für **Python** installieren“ steht bei der **C++**-Aufgabe | Für C++ gelten die Installationsschritte „gRPC für C++ unter Ubuntu“ |
| 10 | **Vorlesung 1**, Beispiel `operationId: app-calculator.add` | Bindestrich im Modulnamen ist unüblich | Unterstrich: `app_calculator.add` / Datei `app_calculator.py` (getestet) |
| 11 | **Windows-Teile** der Übungen 2 und 4 | pixi, `cmd`, `.bat`, `.venv\Scripts\activate.bat` | unter Linux **nicht relevant** |

---

*Viel Erfolg bei der Klausur!*
