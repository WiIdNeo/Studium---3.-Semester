# Betriebssysteme – Kapitel 1: Einführung
## Zusammenfassung (Vorlesung + Übungsaufgaben)

---

# Teil 1: Inhaltliches Wissen aus der Vorlesung

## 1. Betriebssysteme als Begriff

### 1.1 Aufbau von Rechensystemen (Schichtenmodell)

Ein Rechensystem lässt sich (nach Tanenbaum) grob in vier Ebenen gliedern, von unten nach oben:

1. **Hardware** – die physikalischen Geräte; führt letztlich die Software aus.
2. **Mikroprogrammierung / Maschinensprache** – hardwarenächste Steuerung/Befehlssatz der CPU.
3. **Betriebssystem im engeren Sinne (Kern, Kernel)** – dient der Verwaltung und dem Betrieb des Rechners selbst.
4. **Systemsoftware** – z. B. (einfacher) Kommandointerpreter, Compiler, Text-Editor.
5. **Anwendungssoftware** – z. B. Office-Software, Buchungssysteme, Spiele; löst Probleme der (End-)Nutzer.

Wichtige Unterscheidung dabei ist der **Ausführungsmodus**:

- **Benutzermodus (user mode):** Anwendungssoftware läuft hier mit eingeschränktem Zugang (z. B. auf Speicher und Hardware kann nicht frei zugegriffen werden).
- **Kernmodus (kernel mode):** Das Betriebssystem läuft hier privilegiert mit vollständigem Zugang zur gesamten Hardware und zu allen Maschinenbefehlen.

Diese strikte Trennung ist die Grundlage für Sicherheit und Stabilität: Anwendungen können weder versehentlich noch böswillig direkt auf Hardware oder fremde Speicherbereiche zugreifen, sondern müssen den kontrollierten Weg über das Betriebssystem gehen.

### 1.2 Definitionsansätze für ein Betriebssystem

Es gibt zwei komplementäre Sichtweisen, ein Betriebssystem zu definieren:

**Bottom-Up-Definition – Betriebssystem als erweiterte (virtuelle) Maschine**
- Das OS versteckt die reale, komplexe Hardware hinter einer vereinfachten, abstrakten Schicht.
- Umsetzung durch sogenannte Systembefehle bzw. **Systemaufrufe** (system calls).
- Die neue, vereinfachte Sicht auf die Hardware heißt **virtuelle Maschine**; oft liegen mehrere solcher virtuellen Maschinen gestapelt übereinander.
- Beispiel: Die Systemaufrufe `read()`/`write()` für den Dateizugriff verstecken die konkrete Ansteuerung einer SSD (Adressierung, Spannungspegel, Fehlerbehandlung etc.).

**Top-Down-Definition – Betriebssystem als Ressourcenverwalter**
- Das OS teilt beschränkte Ressourcen (z. B. Rechenzeit, Speicher) auf konkurrierende Aufgaben (Programme, Nutzer) auf.
- Das Zuteilungsverfahren heißt **Allokation** (Verb: *allozieren*, nicht *allokieren*).
- Zwei Dimensionen sind bei der Allokation zu berücksichtigen: **Zeit** und **Raum**.
- Beispiel: Wollen zwei Programme gleichzeitig Dateien speichern, legt das OS fest, *wann* (Zeit) und *wo* (Raum) auf der SSD geschrieben wird.

Beide Sichtweisen schließen sich nicht aus, sondern beschreiben zwei Aufgaben, die ein Betriebssystem gleichzeitig erfüllt: Abstraktion der Hardware und faire/effiziente Verteilung knapper Ressourcen.

### 1.3 Betriebsarten (Modi) von Betriebssystemen

| Betriebsart | Beschreibung |
|---|---|
| **Stapelbetrieb** (batch mode) | Aufträge/Jobs/Programme werden zu Paketen geschnürt und nacheinander (sequenziell) abgearbeitet. Keine direkte Interaktion während der Abarbeitung. |
| **Dialogbetrieb** (interactive mode) | Der Benutzer bekommt auf jede Aktion interaktiv eine direkte Reaktion angezeigt. |
| **Echtzeitbetrieb** (realtime mode) | Programme werden garantiert innerhalb einer vorgegebenen Zeit abgeschlossen (feste Zeitschranken). |
| **Mehrprogrammbetrieb** (multitasking mode) | Mehrere Programme laufen (quasi-)gleichzeitig auf einem Rechner. |
| **Mehrbenutzerbetrieb** (multiuser mode) | Mehrere Benutzer arbeiten gleichzeitig an einem Rechner. |

**Betriebsarten heutiger Betriebssysteme:** Moderne Betriebssysteme laufen üblicherweise **gleichzeitig** im Dialog-, Mehrprogramm- (pro Nutzer) und Mehrbenutzerbetrieb. Dafür müssen akzeptable Reaktionszeiten gewährleistet und begrenzte Ressourcen auf Nutzer und Programme verteilt werden. Dagegen können moderne Betriebssysteme in der Regel **keinen echten Echtzeitbetrieb** (feste Reaktionszeiten sind z. B. bei Updates oder voller Systemlast nicht garantiert) und **keinen Stapelbetrieb** direkt anbieten (diese Funktionalität ist nicht fest ins OS integriert, wird aber ggf. von System- oder Anwendungssoftware nachgebildet, z. B. Cron-Jobs, Batch-Skripte).

---

## 2. Historische Entwicklung der Betriebssysteme

| Generation | Zeitraum | Rechnertechnologie | Betriebssystem-Merkmale |
|---|---|---|---|
| **1.** | ca. 1945–1955 | Relais und Röhren | **Kein Betriebssystem!** Programmierung direkt über Steckbretter oder Maschinensprache (z. B. Z3, ENIAC). |
| **2.** | ca. 1955–1965 | Einzelne Transistoren in Großrechnern (mainframes) | **Stapelverarbeitung** (batch processing) von Aufträgen; Eingabe über Lochkarten, Ausgabe über Ausdrucke; später Zwischenspeicherung von Ein-/Ausgabe auf Magnetbändern (z. B. IBM 704). |
| **3.** | ca. 1965–1980 | Mehrere integrierte Bausteine (IC) in Minicomputern | **Mehrprogrammbetrieb**, **Spooling** (Simultaneous Peripheral Operation On Line), erste **Dialogsysteme** (z. B. DEC PDP-7). |
| **4.** | ca. 1980–heute | Vollständig integrierte Schaltkreise (VLSI) in Mikrocomputern | Betriebssystem auf Diskette (**DOS**, z. B. MS-DOS), **fensterbasierte Benutzerschnittstellen**, erste **verteilte Betriebssysteme** (z. B. IBM PC, Commodore 64). |
| **5.** | ca. 1995–heute | Portable, batteriebetriebene (Multicore-)Rechner (Laptops/Notebooks) | Fensterbasierte Oberflächen, zusätzlich **Energiemanagement**. |
| **6.** | ca. 2005–heute | Multicore-Rechner mit Touch-Screens (PDAs, Tablets, Smartphones) | Energiemanagement, **touchbasierte Benutzerschnittstelle**, **Cloud Computing**. |

Erkennbarer roter Faden: Mit wachsender Hardwareleistung wandelt sich das Betriebssystem von "gar nicht vorhanden" über reine Stapelverarbeitung hin zu interaktiven, grafischen, mobilen und vernetzten Systemen – die Anforderungen an Ressourcenverwaltung und Abstraktion wachsen stetig mit.

---

## 3. Systemaufrufe (System Calls)

### 3.1 Motivation

Ohne Betriebssystem müsste ein Programmierer z. B. zum Schreiben von Daten auf einen Datenträger selbst:
- hardwarenah (z. B. in Maschinencode) programmieren,
- herausfinden, welches Datenträgermodell verbaut ist,
- entscheiden, wo die Daten physisch abgelegt werden,
- den Datenträger individuell ansteuern (z. B. Spannungen auf Leiterbahnen),
- Konflikte und Fehler selbst erkennen (z. B. Datenträger voll).

Mit Betriebssystem genügt stattdessen z. B.:

```c
int fd = open("output.txt", O_RDWR); // Öffne Datei mit Dateihandle fd, ...
write(fd, "hallo welt", 10);         // ... schreibe 10 Zeichen hinein, ...
close(fd);                           // ... und gebe Datei wieder frei.
```

Das Betriebssystem exponiert also **Systemaufrufe** als klar definierte Programmierschnittstelle (API) und übernimmt dahinter die komplette Komplexität.

### 3.2 POSIX und Win32

- **POSIX-1003.1** ist eine IEEE-Standardisierung von ca. 100 Systemaufrufen, die von den meisten UNIX-Varianten (Linux, macOS, BSD, …) unterstützt wird.
- **Win32 API** ist die proprietäre Microsoft-Implementierung (ab Windows 95), die ähnliche, aber nicht identische Funktionalität bietet.

Beispiele wichtiger POSIX-Systemaufrufe:

**Prozessverwaltung**
| Aufruf | Beschreibung |
|---|---|
| `pid = fork()` | Erzeugen eines Kindprozesses, identisch zum Vaterprozess |
| `waitpid(pid, &statloc, options)` | Warten auf Terminierung des Kindes |
| `exit(status)` | Prozess beenden und Status zurückliefern |

**Dateiverwaltung**
| Aufruf | Beschreibung |
|---|---|
| `fd = open(file, how, ...)` | Datei zum Lesen und/oder Schreiben öffnen |
| `s = close(fd)` | Offene Datei schließen |
| `n = read(fd, buffer, nbytes)` | Daten aus Datei in Puffer lesen |
| `n = write(fd, buffer, nbytes)` | Daten vom Puffer in Datei schreiben |

**Verzeichnis-/Dateiverwaltung**
| Aufruf | Beschreibung |
|---|---|
| `s = mkdir(name, mode)` | Neues Verzeichnis erzeugen |
| `s = rmdir(name)` | Leeres Verzeichnis löschen |
| `s = link(name1, name2)` | Neuer Eintrag `name2` zeigt auf `name1` (harter Link) |
| `s = unlink(name)` | Verzeichniseintrag löschen |
| `s = mount(special, name, flag)` | Dateisystem einbinden |
| `s = unmount(special)` | Eingebundenes Dateisystem entfernen |
| `s = chdir(dirname)` | Wechsel des aktuellen Verzeichnisses |

**Verschiedenes**
| Aufruf | Beschreibung |
|---|---|
| `s = chmod(name, mode)` | Ändern der Dateirechte |
| `s = kill(pid, signal)` | Signal an einen Prozess schicken |
| `seconds = time(&seconds)` | Zeit seit dem 1. Januar 1970 (Unix-Epoche) erfragen |

**Gegenüberstellung UNIX ↔ Win32**

| UNIX | Win32 | Beschreibung |
|---|---|---|
| `fork()` | `CreateProcess()` | Neuen Prozess erzeugen |
| `waitpid()` | `WaitForSingleObject()` | Auf Ende eines Prozesses warten |
| `exit()` | `ExitProcess()` | Ausführung beenden |
| `open()` | `CreateFile()` | Datei erzeugen/öffnen |
| `close()` | `CloseHandle()` | Datei schließen |
| `read()` | `ReadFile()` | Daten aus Datei lesen |
| `write()` | `WriteFile()` | Daten in Datei schreiben |
| `mkdir()` | `CreateDirectory()` | Verzeichnis erzeugen |
| `rmdir()` | `RemoveDirectory()` | Leeres Verzeichnis löschen |
| `link()` | – | Win32 unterstützt keine harten POSIX-Links |
| `unlink()` | `DeleteFile()` | Datei löschen |
| `mount()` / `umount()` | – | Win32 unterstützt kein POSIX-Einbinden von Dateisystemen |
| `chdir()` | `SetCurrentDirectory()` | Arbeitsverzeichnis ändern |
| `chmod()` | – | keine POSIX-Rechte, stattdessen ACLs (Access Control Lists) |
| `kill()` | – | Win32 unterstützt keine POSIX-Signale |
| `time()` | `GetLocalTime()` | Aktuelle Zeit erfragen |

### 3.3 Ablauf eines Systemaufrufs

Der Ablauf eines Systemaufrufs (z. B. `read()`) läuft in vier Phasen ab:

1. **Aufruf durch Anwendung**
   1a. Die Anwendung legt Parameter (z. B. Dateihandle `fd`, Pufferadresse `&buffer`, Anzahl Bytes `nbytes`) auf den **Stapel** (Stack, ein Zwischenspeicher nach dem LIFO-Prinzip).
   1b. Die Anwendung ruft eine **Bibliotheksfunktion** (z. B. `read()`) für den Systemaufruf auf.
2. **Aufruf durch Bibliotheksfunktion**
   2a. Die Bibliotheksfunktion legt einen **Code** (Identifikationsnummer des Systemaufrufs) in ein **CPU-Register**.
   2b. Die Bibliotheksfunktion löst den Systemaufruf im OS-Kern aus (**kernel trap**) – hierbei wechselt die CPU vom Benutzer- in den Kernmodus.
3. **Abarbeitung im Betriebssystemkern**
   3a. Der **Dispatcher** (Verteiler) im OS-Kern schlägt anhand des Systemaufruf-Codes die zugehörige Kernelfunktion in einer Tabelle nach und ruft sie auf.
   3b. Die Kernelfunktion läuft durch und springt nach Abschluss zurück zur Bibliotheksfunktion (Wechsel zurück in den Benutzermodus).
4. **Rückkehr und Aufräumen**
   4a. Die Bibliotheksfunktion springt zur Anwendung zurück.
   4b. Die Anwendung bereinigt den Stapel (entfernt die zuvor abgelegten Parameter) und setzt die Ausführung fort.

Register und Stapel dienen hier als Transportmittel: Register für kurze, feste Werte (z. B. den Systemaufruf-Code), der Stapel für die eigentlichen Parameter und Rücksprungadressen. Der Adressraum eines Prozesses ist dabei klar in einen **Benutzeradressraum** und einen **Kernadressraum** getrennt – nur im Kernadressraum darf tatsächlich Hardware angesprochen werden.

---

## 4. Betriebssystemstrukturen

### 4.1 Monolithische Struktur
- **Grundform:** Betriebssystem und (teilweise) Anwendungen bilden ein einziges, unstrukturiertes Programm. Jede Funktion kann jede andere Funktion aufrufen, die gesamte Information ist überall sichtbar.
  → Problembehaftet bezüglich Sicherheit und Wartbarkeit.
- **Verbesserte Variante:** Dreischichtige Struktur zwischen Anwendung, Systemaufrufen und OS-Hilfsfunktionen. Pro Systemaufruf existiert eine Bibliotheksfunktion; interne OS-Hilfsfunktionen stehen Anwendungen nicht zur Verfügung.
  → Etwas sicherer und besser wartbar, aber weiterhin ein "großer Block".

### 4.2 Geschichtete Struktur
- Verallgemeinerter Ansatz: Das Betriebssystem besteht aus einer **Hierarchie von Schichten**, wobei jede Schicht nur auf tieferliegenden Schichten aufbaut.
- Beispiel: **THE-System** der TH Eindhoven (E. W. Dijkstra, 1968); ähnlich: Ring- bzw. Zwiebelschalen-Architekturen (z. B. MULTICS).

| Schicht | Funktionalität | Effekt |
|---|---|---|
| 6 | der Benutzer | – |
| 5 | Benutzerprogramme | Funktion des Programms |
| 4 | Ein-/Ausgabeschichten | abstrakte Geräte mit gepufferter E/A |
| 3 | Kommunikationsverwaltung | eine Bedienkonsole pro Prozess |
| 2 | Speicherverwaltung | ein Adressraum pro Prozess |
| 1 | Prozessverwaltung | Mehrprogrammbetrieb |

Dies verbessert Sicherheit und Wartbarkeit weiter, da eine Schicht nur wohldefinierte Schnittstellen der darunterliegenden Schicht nutzen darf.

### 4.3 Client/Server-Struktur (Mikrokern)
- Idee: Möglichst viele OS-Funktionen werden in höhere Schichten (eigene Prozesse) ausgelagert; übrig bleibt nur ein minimaler **Mikrokern** (micro kernel).
- Der Mikrokern übermittelt ausschließlich **Nachrichten** zwischen Client-Prozessen (z. B. Anwendungen) und Server-Prozessen (z. B. Datei-Server, Prozess-Verwalter, Terminal-Server, Speicher-Server des OS).
- Vorteile: kleinere, einfachere OS-Bestandteile (weniger Abhängigkeiten), robustere Bestandteile (abgestürzte Server-Prozesse lassen sich einzeln neu starten, ohne das ganze System zu gefährden).
- Ermöglicht u. a. den Einsatz in verteilten Betriebssystemen.

### 4.4 Verteilte Betriebssysteme
- Idee: Viele Rechner mit jeweils eigenem (Mikro-)Kernel werden über ein Netzwerk verbunden, sollen für den Nutzer aber wie **ein einziger Rechner mit einem einzigen Betriebssystem** erscheinen.
- Umsetzung über das Client/Server-Modell mit Nachrichtenaustausch über das Netzwerk: Ein Client schickt einen Auftrag an einen Server (z. B. Dateiserver, Prozessserver, Terminalserver), der eine Antwort zurückschickt.
- Beispiele: Großrechner/Number Cruncher, Rechensysteme der Firma Cray, das Betriebssystem **Amoeba** von Tanenbaum (bis 1998).

---

## 5. Zusammenfassung der Kernbegriffe (Kapitel 1)

- **Begrifflichkeiten:** Anwendungssoftware vs. Systemsoftware vs. Betriebssystem; Betriebssystem als virtuelle Maschine oder als Ressourcenverwalter; Stapel-, Dialog-, Echtzeit-, Mehrprogramm- und Mehrbenutzerbetrieb.
- **Systemaufrufe:** bieten die Programmierschnittstelle für Programme; standardisiert über POSIX bzw. proprietär über die Win32-API; erfordern einen Wechsel vom Benutzer- in den Kernelmodus.
- **Betriebssystemstrukturen:** monolithisch, geschichtet, Client/Server, verteilt; die Kapselung in kleine, unabhängige Einheiten ist grundsätzlich vorteilhaft (Sicherheit, Wartbarkeit, Robustheit).

---
---

# Teil 2: Lösungen der Übungsaufgaben

## Aufgabe 1: Grundkonzepte

### a) Welchen Nutzen hat ein Betriebssystem für den Endanwender eines Systems?

Für den Endanwender erfüllt das Betriebssystem im Wesentlichen zwei Funktionen:

- **Benutzeroberfläche:** Es stellt eine grafische oder textuelle Oberfläche (z. B. Desktop, Dateimanager, Kommandozeile) bereit, über die der Nutzer den Rechner überhaupt erst bedienen kann, ohne Maschinencode oder Hardwaredetails kennen zu müssen.
- **Ausführungsoberfläche für Programme:** Es stellt eine stabile Plattform bereit, auf der beliebige Anwendungsprogramme laufen können. Dabei übernimmt es im Hintergrund die Verwaltung der Ressourcen (Speicher, Rechenzeit, Ein-/Ausgabegeräte) und stellt sicher, dass mehrere Programme (und ggf. mehrere Nutzer) sich diese Ressourcen fair und ohne gegenseitige Störung teilen.

Kurz: Das Betriebssystem macht den Rechner für den Menschen benutzbar (Abstraktion der Hardware) und sorgt dafür, dass beliebige Software zuverlässig darauf ausgeführt werden kann (Ressourcenverwaltung) – der Endanwender muss sich um keines von beidem selbst kümmern.

### b) Weitere Beispiele für Abstraktion und Ressourcenverwaltung

Die Vorlesung nennt für **Abstraktion** das Beispiel `read()`/`write()` (verstecken die Ansteuerung einer SSD) und für **Ressourcenverwaltung** das gleichzeitige Speichern zweier Dateien (OS entscheidet Zeit und Ort). Andere, davon verschiedene Beispiele sind:

- **Abstraktion:** Die **virtuelle Speicherverwaltung**. Ein Programm "sieht" einen zusammenhängenden, eigenen Adressraum, obwohl der physische Arbeitsspeicher in Wirklichkeit fragmentiert, von anderen Prozessen mitbenutzt und teilweise sogar auf die Festplatte ausgelagert (Swapping) ist. Der Programmierer muss sich um diese Komplexität nicht kümmern.
- **Ressourcenverwaltung:** Die **CPU-Zeit-Zuteilung (Scheduling)**. Wollen mehrere Prozesse gleichzeitig rechnen, aber es steht nur eine begrenzte Anzahl an CPU-Kernen zur Verfügung, entscheidet der Scheduler des Betriebssystems, welcher Prozess wie lange und in welcher Reihenfolge Rechenzeit (Zeit-Dimension der Allokation) erhält.

### c) Smartphone im Stapelbetrieb: Navigation + Musik parallel

Im **Stapelbetrieb** werden Aufträge (Jobs) als Paket geschnürt und **strikt nacheinander** abgearbeitet – es gibt weder Interaktivität noch (in der Regel) echte Parallelität zwischen den Jobs.

Würde man versuchen, eine Navigationsapp zu starten und parallel Musik zu hören, würde das im reinen Stapelbetrieb **nicht funktionieren**: Der zweite "Auftrag" (Musik-Wiedergabe) könnte erst gestartet werden, nachdem der erste (Navigation) vollständig abgeschlossen ist – ein direktes Nebeneinanderlaufen beider Programme ist nicht vorgesehen. Zusätzlich gäbe es keine sofortige Rückmeldung (z. B. würde die Navigationsansprache nicht in Echtzeit erscheinen), da Stapelbetrieb keine interaktive, sofortige Reaktion auf Nutzereingaben liefert.

Die in den Notizen aufgeworfene Frage "Kann das Stapelsystem keine Parallelität?" lässt sich also bestätigen: Reiner Stapelbetrieb ist per Definition **nicht** mit Mehrprogrammbetrieb (paralleles Ausführen mehrerer Programme) gleichzusetzen; beides sind laut Vorlesung getrennte Betriebsarten.

### d) Arbeitet ein normaler Endanwender-PC in Echtzeitbetrieb?

**Nein.** Echtzeitbetrieb setzt voraus, dass Programme garantiert innerhalb einer fest vorgegebenen Zeit abgeschlossen werden (feste, zugesicherte Zeitschranken). Ein gewöhnlicher Endanwender-PC bietet diese Garantie nicht:

- Reaktionszeiten können z. B. durch Hintergrundprozesse, Systemupdates, hohe Systemlast oder das Scheduling anderer Prozesse schwanken.
- Es existiert kein Mechanismus, der eine feste obere Zeitschranke für die Fertigstellung einer Aufgabe garantiert – im schlimmsten Fall "hakt" oder verzögert sich etwas, ohne dass dies einen Fehler im eigentlichen Sinn darstellt.

Das deckt sich mit der Aussage aus der Vorlesung, dass moderne (Desktop-)Betriebssysteme üblicherweise **keinen echten Echtzeitbetrieb** leisten können.

### e) Was versteht man unter einem Kern (Kernel)?

Der **Kernel** ist das Betriebssystem im engeren Sinne – also abzüglich der mitgelieferten Zusatzsoftware (Systemsoftware wie Shell, Compiler, Texteditor etc.). Er übernimmt zwei zentrale Aufgaben:

- Er **abstrahiert die Hardware** (macht sie über Systemaufrufe nutzbar, ohne dass Anwendungen Hardwaredetails kennen müssen) und
- er **übernimmt die direkte Kommunikation mit der Hardware**, da nur der Kernel im privilegierten **Kernmodus** läuft und vollen Zugriff auf alle Hardwarekomponenten und Maschinenbefehle hat.

Alles, was oberhalb dieser Kernfunktionalität liegt (Kommandointerpreter, Compiler, grafische Oberfläche, Anwendungen), läuft dagegen im eingeschränkten **Benutzermodus** und muss für privilegierte Operationen den Umweg über Systemaufrufe an den Kernel gehen.

### f) Mehrbenutzer-, aber nicht Mehrprogramm-Betrieb – geht das?

**Ja, das ist grundsätzlich denkbar.** Mehrbenutzerbetrieb bedeutet lediglich, dass mehrere Benutzer gleichzeitig am selben System angemeldet sind bzw. arbeiten – es sagt zunächst nichts darüber aus, ob dabei mehrere *Programme* gleichzeitig laufen.

Ein Beispiel: Ein System könnte mehreren Nutzern erlauben, sich gleichzeitig einzuloggen (Mehrbenutzerbetrieb), dabei aber systemweit immer nur **ein einziges Programm zur selben Zeit** ausführen – etwa indem reihum jeweils nur der Auftrag eines Nutzers bearbeitet wird, bevor der nächste an der Reihe ist (ähnlich einem quasi-sequenziellen Stapelbetrieb, nur eben mit mehreren Nutzern als Auftraggebern). Es gäbe dann zwar mehrere Benutzer, aber zu keinem Zeitpunkt mehrere gleichzeitig laufende Programme.

In der Praxis ist eine solche Kombination unüblich, da Mehrbenutzersysteme aus Effizienz- und Komfortgründen fast immer auch Mehrprogrammbetrieb realisieren (jeder Nutzer bekommt "quasi-parallel" Rechenzeit zugeteilt); rein konzeptionell widersprechen sich die beiden Betriebsarten aber nicht.

---

## Aufgabe 2: Betriebssysteme als Programme

### a) Einordnung der Begriffe in die Ebenen des Rechensystem-Aufbaus

| Begriff | Ebene | Begründung |
|---|---|---|
| **Powershell** | Systemsoftware (Kommandointerpreter) | Powershell ist eine Shell, also ein (erweiterter) Kommandointerpreter, mit dem der Nutzer textuell Befehle an das Betriebssystem übergibt – analog zur Ebene "Kommandointerpreter" im Schichtenmodell. |
| **Ubuntu** | Betriebssystem / Systemsoftware-Ebene (Kernel + mitgelieferte Systemsoftware) | Ubuntu ist eine komplette Linux-Distribution, bestehend aus dem Linux-Kernel plus gebündelter Systemsoftware (Shell, Treiber, Basisdienste). Es bildet damit selbst die Betriebssystem-Ebene, auf der wiederum Anwendungssoftware läuft. |
| **Teams** | Anwendungssoftware | Microsoft Teams ist ein Kommunikations-/Kollaborationsprogramm für Endnutzer und löst ein konkretes Nutzerproblem (Videokonferenzen, Chat) – klassische Anwendungssoftware. |
| **Translation Lookaside Buffer (TLB)** | Hardware (bzw. Mikroprogrammierung) | Der TLB ist ein kleiner, sehr schneller Cache in der CPU/MMU (Memory Management Unit), der Übersetzungen von virtuellen in physische Speicheradressen zwischenspeichert. Er ist ein Hardwarebestandteil, der zwar vom Betriebssystem (Speicherverwaltung) genutzt wird, selbst aber physisch in der CPU realisiert ist. |
| **Windows Explorer** | Systemsoftware | Der Windows Explorer ist ein mit dem Betriebssystem ausgelieferter Dateimanager, vergleichbar mit einem Text-Editor auf der Systemsoftware-Ebene: Er ist kein vom Nutzer nachinstalliertes Anwendungsprogramm zur Problemlösung eines spezifischen Fachbereichs, sondern ein grundlegendes, systemnahes Werkzeug zur Bedienung des Rechners. |

### b) Nutzen des Systemaufrufs `open()` (Abstraktion & Ressourcenverwaltung)

- **Abstraktion:** `open()` erkennt automatisch relevante Eigenschaften der Datei (z. B. Dateityp, Größe, Speicherort auf dem physischen Datenträger) und liefert der Anwendung ein einfaches, einheitliches **Dateihandle** (`fd`) zurück. Die Anwendung muss weder wissen, auf welchem Dateisystem oder Datenträgertyp die Datei liegt, noch wie genau darauf zugegriffen wird – all das ist hinter dem Systemaufruf verborgen. Ohne diese Abstraktion müsste je nach Dateityp/Speicherort ein anderer, spezifischer Zugriffsbefehl verwendet werden.
- **Ressourcenverwaltung:** Beim Öffnen prüft und verwaltet das Betriebssystem den **Zugriff auf die gemeinsam genutzte Ressource "Datei"** – z. B. ob die Datei bereits von einem anderen Prozess exklusiv geöffnet ist, welche Zugriffsrechte gelten, und reserviert intern Verwaltungsstrukturen (z. B. einen Eintrag in der Dateideskriptor-Tabelle) für den Prozess. So wird sichergestellt, dass mehrere Prozesse nicht unkontrolliert gleichzeitig und widersprüchlich auf dieselbe Datei zugreifen.

### c) Fragen zum Schaubild auf Folie 27 (Ablauf eines Systemaufrufs)

**Was ist ein Register?**
Ein Register ist eine sehr kleine, aber extrem schnelle Speicherzelle direkt in der CPU. Register werden genutzt, um einzelne Werte (z. B. Zwischenergebnisse, Adressen oder – wie hier – den Identifikationscode eines Systemaufrufs) ohne Umweg über den (deutlich langsameren) Hauptspeicher unmittelbar verfügbar zu halten.

**Was ist der Stapel?**
Der Stapel (Stack) ist ein Speicherbereich, der nach dem LIFO-Prinzip (Last In, First Out) organisiert ist. Er dient hier dazu, die Parameter eines Funktions-/Systemaufrufs (z. B. `fd`, `&buffer`, `nbytes`) sowie Rücksprungadressen zwischenzuspeichern, damit sie nach dem Aufruf wieder korrekt "abgeräumt" bzw. verwendet werden können.

**Welche Aufgabe hat der Dispatcher?**
Der Dispatcher ist die Komponente im Kern, die anhand des übergebenen Systemaufruf-Codes in einer Tabelle nachschlägt, welche konkrete Kernelfunktion für diesen Aufruf zuständig ist, und diese Funktion dann aufruft. Er ist also der zentrale "Verteiler" zwischen der Nummer eines Systemaufrufs und seiner tatsächlichen Implementierung im Kern.

**Warum ist dieses umständlich anmutende Vorgehen sinnvoll? Warum liest die Bibliotheksfunktion nicht selbst von der Festplatte?**
Die Bibliotheksfunktion läuft im **Benutzermodus** und hat dort keinen direkten Zugriff auf Hardware wie die Festplatte – nur der Kernel im **Kernmodus** darf Hardware direkt ansprechen. Dieser Umweg über den Trap in den Kern ist notwendig, damit das Betriebssystem jeden Hardwarezugriff kontrollieren, prüfen (z. B. Berechtigungen) und zwischen konkurrierenden Prozessen fair vermitteln kann. Würde jede Anwendung direkt auf Hardware zugreifen dürfen, wären Systemstabilität und -sicherheit nicht mehr gewährleistet (z. B. könnten sich Prozesse gegenseitig Daten überschreiben oder Systemabstürze verursachen).

**Wann wird vom Benutzer- in den Kernmodus gewechselt und umgekehrt?**
- In den **Kernmodus** wird gewechselt, sobald die Bibliotheksfunktion den Systemaufruf mittels **Trap** auslöst (Schritt 2b).
- Zurück in den **Benutzermodus** wird gewechselt, sobald die Kernelfunktion ihre Arbeit abgeschlossen hat und die Kontrolle wieder an die Bibliotheksfunktion zurückgibt (Schritt 3b/4a).

**Wie kommt das Ergebnis von `read()` zurück zur Anwendung?**
Zum einen über den beim Aufruf übergebenen **Pufferzeiger** (`&buffer`): Die Kernelfunktion schreibt die gelesenen Daten direkt in den vom Aufrufer bereitgestellten Speicherbereich. Zum anderen liefert die Bibliotheksfunktion nach ihrer Rückkehr einen **Rückgabewert** (z. B. Anzahl tatsächlich gelesener Bytes bzw. einen Fehlercode) über ein Register bzw. den Stapel an die Anwendung zurück.

### d) Einsatz der Systemaufrufe `open()`, `fork()`, `mkdir()`, `mount()`, `time()` in einer Programmiersprache

Am Beispiel von **C** (sehr hardwarenah) und **C#/.NET** (höhere Sprache) lässt sich der Unterschied gut zeigen:

- In **C** (über `<unistd.h>`, `<sys/stat.h>`, `<sys/mount.h>`, `<time.h>` etc.) sind `open()`, `fork()`, `mkdir()`, `mount()` und `time()` **dünne Wrapper-Funktionen**, die den eigentlichen Systemaufruf nahezu unmittelbar auslösen – zwischen dem Funktionsaufruf im Quellcode und dem Trap in den Kern liegt kaum zusätzliche Logik.
- In **höheren Sprachen** wie C#, Java oder Python liegt zwischen dem Programm und dem eigentlichen Systemaufruf zusätzlich die **Sprach-Laufzeitumgebung/Standardbibliothek** (z. B. die .NET-Runtime bzw. die JVM). Ruft man z. B. in C# `Directory.CreateDirectory(...)` auf, übersetzt die .NET-Bibliothek diesen plattformunabhängigen Aufruf erst intern in den jeweiligen betriebssystemspezifischen Systemaufruf (`mkdir()` unter Linux/macOS bzw. `CreateDirectory()` unter Windows).
- `fork()` ist zudem ein gutes Beispiel für Plattformunterschiede: Es existiert nativ nur unter POSIX-Systemen; unter Windows gibt es kein direktes Äquivalent, dort wird stattdessen `CreateProcess()` verwendet (vgl. Win32-Tabelle oben).
- `mount()` ist sehr systemnah und in höheren, plattformunabhängigen Sprachen häufig gar nicht oder nur eingeschränkt über Bibliotheken zugänglich, da es stark betriebssystemspezifisch ist.

**Fazit:** Die Systemaufrufe werden in höheren Programmiersprachen in der Regel **nicht direkt**, sondern über eine oder mehrere Abstraktionsebenen (Standardbibliothek, Laufzeitumgebung) angesprochen, die den eigentlichen, plattformabhängigen Trap in den Kern übernehmen.

### e) Programm: Verzeichnis "mittagessen" mit Datei "ramen.txt" erzeugen (C#)

```csharp
using System;
using System.IO;

class Program {
    static void Main(string[] args) {
        Directory.CreateDirectory("./mittagessen");
        File.WriteAllText("./mittagessen/ramen.txt", "noodles meat shrooms");
    }
}
```

**Erklärung:**
- `Directory.CreateDirectory("./mittagessen")` entspricht letztlich dem Systemaufruf `mkdir()` – das Betriebssystem legt einen neuen Verzeichniseintrag an.
- `File.WriteAllText(...)` fasst mehrere Systemaufrufe zusammen: intern wird die Datei geöffnet bzw. neu angelegt (`open()`), der Text hineingeschrieben (`write()`) und die Datei anschließend wieder geschlossen (`close()`).
- (Kleine Korrektur gegenüber der ursprünglichen Notiz: Die Zeile mit `File.WriteAllText(...)` muss mit einem Semikolon `;` abgeschlossen werden, da C# dies syntaktisch zwingend verlangt.)

### f) Programm: Vorheriges Programm starten, warten, dann beenden (C#)

```csharp
using System;
using System.Diagnostics;
using System.Threading.Tasks;

class Program {
    static async Task Main(string[] args) {
        await StartScript();
        Environment.Exit(0);
    }

    public static async Task StartScript() {
        var startInfo = new ProcessStartInfo
        {
            FileName = "/bin/bash",
            Arguments = "-c \"/pfad/zur/ausfuehrbaren/Datei\"",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using var process = new Process { StartInfo = startInfo };
        process.Start();
        await process.WaitForExitAsync();
    }
}
```

**Erklärung:**
- `Process.Start()` entspricht (vereinfacht) einem `fork()` + `exec()`: Es wird ein neuer Prozess erzeugt, der ein anderes Programm (hier über die Bash gestartet) ausführt.
- `process.WaitForExitAsync()` entspricht dem Systemaufruf `waitpid()`: Der aufrufende Prozess wartet, bis der Kindprozess beendet ist.
- `Environment.Exit(0)` entspricht dem Systemaufruf `exit()`: Der eigene Prozess beendet sich mit einem Rückgabewert (hier `0` für "erfolgreich").
- Der in den ursprünglichen Notizen enthaltene Platzhalter `egZurAusführbarenDatei` wurde durch einen echten (Platzhalter-)Pfad ersetzt, da C# hier eine konkrete Zeichenkette erwartet.

**Hinweis aus der Aufgabenstellung:** Bei Python wäre das bloße Interpretieren von neuem Code **kein** Systemaufruf – der eigentliche Systemaufruf läge erst darin, `py.exe` (bzw. das entsprechende Unix-Äquivalent, z. B. `/usr/bin/python3`) als neuen Prozess zu starten. Das zeigt: Nicht jede "Ausführung von Code" ist automatisch ein Systemaufruf – entscheidend ist, ob tatsächlich ein neuer Prozess über das Betriebssystem erzeugt bzw. eine privilegierte Operation angestoßen wird.

### g) Warum hat die monolithische Struktur hohes Fehlerpotenzial?

In einer monolithischen Struktur laufen Betriebssystem und ggf. Teile der Anwendungslogik als **ein einziges großes Programm ohne klare Trennung**. Da an jeder Stelle des Codes auf alle verfügbaren Systemaufrufe und internen Funktionen zugegriffen werden kann und die gesamte Information (globale Variablen, interne Datenstrukturen) überall sichtbar ist, ergeben sich mehrere Probleme:

- **Fehlende Kapselung:** Ein Fehler (z. B. ein Speicherzugriffsfehler) in einer beliebigen Komponente kann unkontrolliert auf andere, eigentlich unabhängige Komponenten durchschlagen, da es keine geschützten Grenzen zwischen den Modulen gibt.
- **Schwierige Fehlersuche:** Da jede Funktion potenziell jede andere aufrufen und beeinflussen kann, ist es schwer nachzuvollziehen, welche Komponente für einen Fehler verantwortlich ist.
- **Sicherheitsrisiko:** Ein Fehler oder eine Schwachstelle in einem kleinen, eigentlich unwichtigen Teil (z. B. einem Gerätetreiber) kann das gesamte System kompromittieren, da dieser Teil im selben privilegierten Adressraum wie der Rest des Kernels läuft.
- **Stabilität:** Stürzt eine Komponente ab, reißt sie oft das gesamte System mit in den Absturz, da es keine Isolation (z. B. separate Prozesse mit eigenem Adressraum) gibt.

Genau diese Probleme motivieren die weiterentwickelten Strukturen (geschichtet, Client/Server, verteilt), die durch klar getrennte Schichten bzw. eigenständige, isolierte Prozesse Sicherheit und Wartbarkeit verbessern.

### h) Zusammenhang Client/Server-Architektur und verteilte Architektur

Die **Client/Server-Architektur** ist die konzeptionelle Grundlage der **verteilten Betriebssysteme**: Bei einer "klassischen" Client/Server-Struktur (z. B. mit Mikrokern) laufen Client-Prozesse (Anwendungen) und Server-Prozesse (z. B. Datei-Server, Prozessverwalter) zwar getrennt, aber typischerweise noch **auf demselben Rechner**, wobei ein einzelner Mikrokern die Nachrichten zwischen ihnen vermittelt.

Bei einem **verteilten Betriebssystem** wird dieses Prinzip über mehrere physisch getrennte Rechner hinweg ausgedehnt: Jeder Rechner hat seinen eigenen Kernel, aber Client und Server(e) befinden sich auf unterschiedlichen Maschinen und kommunizieren über ein **Netzwerk** statt (nur) über lokale Nachrichten im selben Rechner. Der Nutzer soll dabei trotzdem den Eindruck haben, mit einem einzigen, zusammenhängenden System zu arbeiten.

Kurz gesagt: In der **Client/Server-Architektur** gibt es (mindestens) einen Client und mehrere Server, die über Nachrichtenaustausch kommunizieren – meist auf einem Rechner. Beim **verteilten Betriebssystem** wird dasselbe Nachrichtenaustausch-Prinzip auf mehrere Rechner ausgeweitet, wobei jeder Teilnehmer je nach Situation sowohl Client als auch Server sein kann (z. B. ein Rechner, der selbst Aufträge verschickt, aber auch Dateiserver für andere ist).

### i) Stellungnahme zur Aussage des Kollegen

**Aussage:** "Bei der Client/Server-Architektur kann ja wieder jede Software-Komponente mit jeder anderen Komponente reden. Das widerspricht dem Gedanken der Schichtenarchitektur, durch Schichtung Sicherheit zu erzeugen, ist also eher ein Rückschritt."

**Der Kollege hat nicht recht – zumindest nicht in dieser pauschalen Form.** Zwar stimmt es oberflächlich, dass in der Client/Server-Struktur (im Gegensatz zur strikten Schichtenarchitektur mit "nur nach unten sichtbaren" Schichten) prinzipiell jede Komponente Nachrichten an jede andere Komponente schicken kann. Das ist aber nicht mit dem unkontrollierten, direkten Funktions- und Speicherzugriff der monolithischen Struktur vergleichbar:

- **Jede Komponente läuft in einem eigenen, isolierten Prozess** mit eigenem Adressraum. Eine Komponente kann nicht direkt auf den internen Speicher oder die Datenstrukturen einer anderen Komponente zugreifen, sondern nur über klar definierte **Nachrichten** kommunizieren.
- Diese Nachrichten laufen über den **Mikrokern**, der als kontrollierende Instanz fungiert und z. B. Zugriffsrechte prüfen bzw. Kommunikationswege einschränken kann.
- Stürzt eine Server-Komponente ab, betrifft dies (dank der Prozessisolation) im Idealfall nur diese Komponente und kann isoliert neu gestartet werden – ganz anders als im Monolithen, wo ein Fehler das gesamte System gefährdet.

Die Sicherheit entsteht bei Client/Server also **nicht** (wie bei der reinen Schichtenarchitektur) durch die Einschränkung "wer darf wen aufrufen", sondern durch **Prozessisolation und kontrollierte, mediierte Kommunikation**. In gewisser Weise wird sogar mehr Sicherheit erreicht als bei einer reinen Schichtenarchitektur, da selbst ein kompromittierter Server nicht direkt auf den Speicher anderer Komponenten zugreifen kann. Die Flexibilität, dass "jeder mit jedem reden kann", ist also kein Rückschritt, sondern lediglich eine andere, meist robustere Art, Sicherheit umzusetzen.
