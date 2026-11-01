# Betriebssysteme – Lernzusammenfassung zur Klausur

> Basis: Vorlesungen 1 (Einführung), 2 (Prozessverwaltung), 3 (Speicherverwaltung), 4 (Dateiverwaltung), 5 (Ein-/Ausgabe) und X (Angriffe auf die Seitentabelle) von Tobias Werner.
> Kapitel 6 (Systemsicherheit) wurde nicht hochgeladen und fehlt hier.
> Markierungen: ⭐ = sehr klausurtypisch, 🧮 = Rechen-/Anwendungsaufgabe, ➕ = Ergänzung von mir (steht nicht auf den Folien).

---

## 0. Klausurformat (Folie VL 1)

| Punkt | Info |
|---|---|
| Dauer / Umfang | 1 h schriftlich, ca. 25 Punkte, ca. 3 Aufgaben |
| Hilfsmittel | vermutlich keine (evtl. 1 handschriftlicher DIN-A4-Zettel, nach Abstimmung im Kurs, dann keine Auswendiglernfragen) |
| Stoff | gesamter Umfang, kein Lernen auf Lücke |
| Verteilung | ca. **25 % Wissen** (Definitionen), ca. **50 % Anwendung** (Algorithmen von Hand), ca. **25 % Theorie** (leichte Beweise) |

**Konsequenz:** Die Hälfte der Punkte gibt es für Handrechnen. Übe vor allem Seitenersetzung, Adressübersetzung, Scheduling, Deadlock-/Race-Analyse, FAT/I-Node-Rechnungen.

---

## 1. Einführung

### 1.1 Aufbau eines Rechensystems

| Schicht | Beschreibung | Modus |
|---|---|---|
| Anwendungssoftware | löst Probleme der Endnutzer (Office, Spiele, Compiler …) | **Benutzermodus** (user mode), eingeschränkter Zugriff |
| Systemsoftware | Verwaltung/Betrieb des Rechners selbst | |
| **Betriebssystem i. e. S. = Kern (Kernel)** | läuft im **Kernmodus** mit vollem Zugriff auf Hardware und alle Befehle | **Kernmodus** (kernel mode) |
| Hardware | Maschinensprache, Mikroprogrammierung, physikalische Geräte | |

### 1.2 Zwei Sichten auf ein OS ⭐

| | Bottom-Up | Top-Down |
|---|---|---|
| Sicht | **erweiterte Maschine / virtuelle Maschine** | **Ressourcenverwalter** |
| Idee | OS versteckt die reale Hardware hinter einer einfachen, abstrakten Schicht (Systemaufrufe) | OS teilt knappe Ressourcen (Rechenzeit, Speicher) konkurrierenden Aufgaben zu |
| Begriff | Systembefehle / Systemaufrufe | **Allokation** (Verb: *allozieren*), in zwei Dimensionen: **Zeit** und **Raum** |
| Beispiel | `read()`/`write()` verstecken die SSD-Ansteuerung | Zwei Programme schreiben gleichzeitig: OS legt fest *wann* (Zeit) und *wo* (Raum) geschrieben wird |

### 1.3 Betriebsarten ⭐

| Betriebsart | Bedeutung |
|---|---|
| Stapelbetrieb (batch) | Aufträge werden zu Paketen gebündelt und nacheinander abgearbeitet |
| Dialogbetrieb (interactive) | Benutzer bekommt auf jede Aktion direkte Reaktion |
| Echtzeitbetrieb (realtime) | Programme werden innerhalb einer vorgegebenen Zeit abgeschlossen |
| Mehrprogrammbetrieb (multitasking) | mehrere Programme gleichzeitig auf einem Rechner |
| Mehrbenutzerbetrieb (multiuser) | mehrere Benutzer gleichzeitig an einem Rechner |

**Moderne OS:** Dialog- + Mehrprogramm- + Mehrbenutzerbetrieb.
**Können i. d. R. nicht:** Echtzeit (feste Reaktionszeit nicht garantiert, z. B. bei Updates/Volllast) und Stapelbetrieb (nicht direkt im OS integriert, ggf. durch System-/Anwendungssoftware).

### 1.4 Historische Entwicklung (Generationen)

| Gen. | Zeit | Technologie | OS-Merkmale | Beispiele |
|---|---|---|---|---|
| 1 | ca. 1945–55 | Relais, Röhren | **kein OS**, Programmierung per Steckbrett/Maschinensprache | Z3 (1941), ENIAC (1946) |
| 2 | ca. 1955–65 | einzelne Transistoren, Großrechner (mainframes) | **Stapelverarbeitung** von Jobs, Lochkarten rein, Ausdrucke raus, später Magnetbänder | IBM 704 |
| 3 | ca. 1965–80 | integrierte Schaltkreise (IC), Minicomputer | **Mehrprogrammbetrieb, Spooling** (Simultaneous Peripheral Operation On Line), **Dialogsysteme** | DEC PDP-7 |
| 4 | ca. 1980–heute | VLSI auf einem Chip, Mikrocomputer | OS auf Diskette (DOS), **fensterbasierte GUI**, **verteilte OS** | IBM PC, C64 |
| 5 | ca. 1995–heute | portable, batteriebetriebene Multicore-Rechner (Laptops) | fensterbasierte GUI, **Energiemanagement** | Notebooks |
| 6 | ca. 2005–heute | Multicore nur per Touch (PDAs, Tablets, Smartphones) | Energiemanagement, **Touch-GUI**, **Cloud Computing** | Smartphone |

Merkhilfe: Röhre → Transistor/Batch → IC/Multiprogramming+Spooling → VLSI/GUI → mobil/Energie → Touch/Cloud.

### 1.5 Systemaufrufe ⭐

**Idee:** Das OS stellt Programmierern eine Schnittstelle bereit, statt dass sie die Hardware selbst ansteuern müssen.

```c
int fd = open("output.txt", O_RDWR);   // Datei öffnen, Handle fd
write(fd, "hallo welt", 10);           // 10 Zeichen schreiben
close(fd);                             // Datei freigeben
```

**POSIX (IEEE 1003.1):** Standard mit ca. 100 Systemaufrufen, von den meisten UNIX-Varianten unterstützt.
**Win32-API:** proprietär, ähnlich, aber nicht gleich.

| UNIX / POSIX | Win32 | Bedeutung |
|---|---|---|
| `fork()` | `CreateProcess()` | Prozess erzeugen |
| `waitpid()` | `WaitForSingleObject()` | auf Prozessende warten |
| `exit()` | `ExitProcess()` | Ausführung beenden |
| `open()` | `CreateFile()` | Datei erzeugen/öffnen |
| `close()` | `CloseHandle()` | Datei schließen |
| `read()` / `write()` | `ReadFile()` / `WriteFile()` | lesen / schreiben |
| `mkdir()` | `CreateDirectory()` | Verzeichnis anlegen |
| (`rmdir()`) | `RemoveDirectory()` | leeres Verzeichnis löschen |
| `unlink()` | `DeleteFile()` | Datei löschen |
| `chdir()` | `SetCurrentDirectory()` | Arbeitsverzeichnis ändern |
| `time()` | `GetLocalTime()` | Zeit erfragen |
| `link()`, `mount()`, `umount()`, `kill()` | **kein Pendant** | Win32 kennt keine harten POSIX-Links, kein POSIX-Mounten, keine POSIX-Signale |
| `chmod()` | – | keine POSIX-Rechte in Windows, stattdessen **ACLs** |

Weitere POSIX-Aufrufe: `fork()` (Kindprozess identisch zum Vater), `kill(pid, signal)`, `mount/unmount`, `link(name1, name2)` (neuer Eintrag zeigt auf Datei), `unlink`, `rmdir`, `chmod`.

### 1.6 Ablauf eines Systemaufrufs (am Beispiel `read(fd, &buffer, nbytes)`) ⭐

1. **Aufruf durch Anwendung**
   - 1a. Anwendung legt Parameter (`fd`, `&buffer`, `nbytes`) auf den **Stapel**
   - 1b. Anwendung ruft die **Bibliotheksfunktion** `read` auf
2. **Aufruf durch Bibliotheksfunktion**
   - 2a. legt den **Code (ID-Nummer)** des Systemaufrufs in ein **CPU-Register**
   - 2b. löst den Systemaufruf in den Kern aus (**Kernel Trap**) → Wechsel Benutzermodus → Kernmodus
3. **Abarbeitung im Kern**
   - 3a. **Dispatcher** schlägt die Kernelfunktion zum Systemaufruf-Code in einer **Tabelle** nach und ruft sie auf
   - 3b. Kernelfunktion läuft durch und springt zurück zur Bibliotheksfunktion
4. **Rückkehr und Aufräumen**
   - 4a. Bibliotheksfunktion springt zur Anwendung zurück
   - 4b. Anwendung bereinigt den Stapel (Stackpointer erhöhen) und macht weiter

### 1.7 Betriebssystemstrukturen ⭐

| Struktur | Idee | Vor-/Nachteile |
|---|---|---|
| **Monolithisch (Grundform)** | OS und Anwendung = ein Programm ohne Struktur, jede Funktion ruft jede | alles überall sichtbar → Probleme bei Sicherheit und Wartung |
| **Monolithisch (verbessert, 3 Schichten)** | Anwendung → Bibliotheksfunktionen (je Systemaufruf eine) → OS-Hilfsfunktionen (für Anwendungen nicht sichtbar) | etwas sicherer, besser wartbar |
| **Geschichtet** | Hierarchie von Schichten, jede baut nur auf tieferen auf (z. B. **THE-System**, Dijkstra, TH Eindhoven, 1968; ähnlich MULTICS-Ringe) | besser bzgl. Sicherheit und Wartbarkeit |
| **Client/Server (Mikrokern)** | möglichst viel in Server-Prozesse im Benutzermodus auslagern; Mikrokern übermittelt nur Nachrichten | kleiner, einfacher, **robuster** (abgestürzte Server neu starten), für verteilte OS geeignet |
| **Verteilt** | viele Rechner mit eigenem OS wirken wie ein Rechner mit einem OS; Client/Server mit Nachrichtenaustausch | z. B. Großrechner, Cray, Amoeba (Tanenbaum, bis 1998) |

**THE-System, Schichten (von unten):** 1 Prozessverwaltung (Mehrprogrammbetrieb) → 2 Speicherverwaltung (ein Adressraum pro Prozess) → 3 Kommunikationsverwaltung (Bedienkonsole pro Prozess) → 4 Ein-/Ausgabe (abstrakte Geräte mit gepufferter E/A) → 5 Benutzerprogramme → 6 Benutzer.

**Kernaussage:** Kapselung in kleine, unabhängige Einheiten ist vorteilhaft.

---

## 2. Prozessverwaltung

### 2.1 Prozess-Begriff ⭐

- **Prozess** = zeitlicher Fortschritt eines ablauffähigen Programms mit allen zugehörigen Ressourcen (Betriebsmittel, z. B. Variablen, offene Dateien).
- **Prozesskontext** = gesamte Information, die für den Ablauf des Programms im Prozess wichtig ist:

| Teil | Wo | Inhalt |
|---|---|---|
| **Benutzerkontext** | Hauptspeicher (user space) | Datenstrukturen, Programmcode, Aufrufstapel |
| **Hardwarekontext** | auf der CPU (nur für gerade aktive Prozesse) | Befehlszähler, Programmstatuswort, Registerinhalte, Stapelzeiger |
| **Systemkontext** | Hauptspeicher (kernel space) | Prozessnummer, Eltern-/Kindprozesse, Prioritäten, geöffnete Dateien |

- Jeder Programmstart erzeugt einen **neuen Prozess mit eigener ID und eigenem Kontext** (Programm zweimal starten → zwei unabhängige Prozesse).

**Prozesse entstehen durch:** Systemstart (init, Daemons), Systemaufruf (`fork()`, `CreateProcess()`), Benutzeranfrage (Terminal, Doppelklick), Stapelauftrag (cronjob).
**Prozesse enden durch:** normales Ende (`exit()`, Rückkehr aus `main`), einfacher Fehler (freiwillig, abgefangen), schwerwiegender Fehler (unfreiwillig, z. B. Division durch 0), anderen Prozess (`kill()`, `TerminateProcess()`).

### 2.2 Parallelität

- Ein Kern führt zu einer Zeit nur **einen** Maschinenbefehl aus.
- **Echte Parallelität:** n Prozesse auf n Kernen zeitgleich.
- **Quasi-Parallelität (scheinbarer Multiprogrammbetrieb):** mehr Prozesse (> 100) als Kerne (≤ 32); das OS wechselt pro Kern schnell (z. B. alle 16 ms) zwischen Prozessen.
- Zu einer Zeit max. 1 Prozess pro Kern und max. 1 Kern pro Prozess.
- **Kontextwechsel:** Umschalten eines Kerns auf einen anderen Prozess, der aktuelle Prozess wird **verdrängt**. Er wirkt zufällig → Quelle für Race Conditions.

### 2.3 Prozesszustände ⭐

| Zustand | Bedeutung | Warteschlange |
|---|---|---|
| **aktiv** | Instruktionen laufen gerade auf einem Kern | – |
| **bereit** | könnte rechnen, wartet auf Kern-Zuteilung (mehr Prozesse als Kerne) | **Bereit-Warteschlange** (ready queue) |
| **blockiert** | wartet auf externe Ressource außer CPU (Ereignis, Festplatte, Netzwerk, gesperrte Datei) | **Blockiert-Warteschlange** (blocked queue) |

**Übergänge (Zustandsdiagramm zeichnen können!):**

```
            Prozess bekommt Kern-Allokation
   ┌────────┐ ───────────────────────────────▶ ┌───────┐
   │ bereit │                                  │ aktiv │
   └────────┘ ◀─────────────────────────────── └───────┘
        ▲        Prozess wird von CPU verdrängt     │
        │                                           │ blockiert (wartet auf Ressource)
        │  Prozess hat alle Ressourcen erhalten     ▼
        │                                     ┌───────────┐
        └──────────────────────────────────── │ blockiert │
                                              └───────────┘
```

Wichtig: blockiert → **bereit** (nicht direkt aktiv!), aktiv → bereit nur durch Verdrängung.

### 2.4 Threads ⭐

**Problem seriell:** Alles in einem Prozess auf einem Kern → komplexer Programmfluss, Mehrkern-CPUs nicht ausgelastet, Anwendung stockt, wenn eine Aufgabe hängt.
**Problem mehrere Prozesse:** Jeder Prozess hat komplett getrennten Kontext → Datenaustausch umständlich (Dateien, Hin- und Herschicken).
**Lösung Thread (Faden):** leichtgewichtiger Unterprozess, der sich viele Ressourcen mit anderen Threads desselben Prozesses teilt, aber **eigenen Ausführungszustand** hat.

| | Prozess | Thread |
|---|---|---|
| Programmcode / Variablen / Heap | getrennt | **geteilt** innerhalb des Prozesses |
| Eigener Zustand | alles | **eigener Stapel, aktuelle Anweisung, Registerzustand (Kern)** |
| Erzeugen / Löschen / Wechsel | teuer | **leichtgewichtig, schnell** |
| Datenaustausch | umständlich | einfach |
| Absturz | betrifft nur sich | **Thread-Absturz reißt den ganzen Prozess mit** |
| Sicherheit | gut getrennt | Daten **ungeschützt geteilt**, kompromittierte Threads gefährlich |
| Race Conditions / Deadlocks | selten | **deutlich anfälliger** |

Ein Prozess startet mit einem **Hauptthread** (beginnt in `main`). `t.join()` wartet, bis Thread `t` beendet ist.

### 2.5 Scheduling ⭐🧮

- **Scheduler/Dispatcher** (im Kern, unterste OS-Schicht) verwaltet Warteschlangen, benachrichtigt bei Ressourcenverfügbarkeit, führt Prozesswechsel durch.
- **Scheduling** = Planung der Reihenfolge der CPU-Zuteilung. **Dispatching** = tatsächliche Zuteilung inkl. Prozesswechsel.
- **Kontextwechsel:** Kontext des verdrängten Prozesses sichern, zuvor gesicherten Kontext des neuen laden.

**Modell pro Prozess Pᵢ:**

| Symbol | Name | Bedeutung |
|---|---|---|
| rᵢ | Bereitzeitpunkt (ready time) | wann Pᵢ bereit wird |
| sᵢ | Startzeitpunkt (start time) | wann Pᵢ erstmals läuft |
| cᵢ | Endzeitpunkt (completion time) | wann Pᵢ fertig ist |
| dᵢ | Frist (deadline) | bis wann Pᵢ fertig sein muss |
| eᵢ | Rechenzeit (execution time) | reine CPU-Zeit |
| wᵢ | Wartezeit | Zeit in der Bereit-Warteschlange |
| fᵢ | Bearbeitungszeit (flow time) | **fᵢ = cᵢ − rᵢ** (= wᵢ + eᵢ, wenn am Stück bearbeitet) |

**Bewertungskriterien:**
- **Auslastung** = Σeᵢ / T (T = Betrachtungszeitraum, z. B. [0, c_max]). Ziel 100 %, typisch erreichbar 40 … 90 %.
- **Mittlere Bearbeitungszeit** f_mean = (1/n) · Σfᵢ.
- **Zielkonflikt:** Kurze Prozesse bevorzugen → kürzere mittlere Bearbeitungszeit, aber geringere Auslastung. Lange bevorzugen → höhere Auslastung, längere mittlere Bearbeitungszeit. **Es gibt keinen idealen Scheduling-Algorithmus für jede Situation.**

**Algorithmen:**

| Verfahren | Annahme | Vorgehen | Vorteile | Nachteile |
|---|---|---|---|---|
| **First-Come-First-Serve (FCFS)** | Prozess(teile) müssen **am Stück** laufen | Reihenfolge der Bereitmeldung (FIFO-Queue) | einfach, jeder kommt dran (kein Verhungern) | langer, früh bereiter Prozess verzögert alle späteren |
| **Earliest-Deadline-First (EDF)** | feste, kritische Deadlines (z. B. Fahrassistent) | Prozess mit der **frühesten Deadline** zuerst | bei wenig Last werden Deadlines relativ sicher eingehalten | bei hoher Last können Prozesse mit später Deadline **verhungern**, auch wenn eine Lösung existieren würde |
| **Zeitscheiben (Round Robin-artig, Desktop-OS)** | Prozesse dürfen beliebig **verdrängt** werden (preemptive multitasking) | Zeit in Zeitscheiben (timeslices) teilen, pro Scheibe Prozess nach Kriterien (Priorität, Wartezeit) wählen | guter Kompromiss Bearbeitungszeit/Auslastung | heuristisch, Zeitscheibenteile gehen durch blockierende Prozesse verloren, braucht Zusatzinfo vom Anwender (zeitkritisch? Hintergrund?) |

🧮 **Beispiel FCFS** ➕ (selbst gerechnet): A (r=0, e=5), B (r=1, e=2), C (r=2, e=1)
→ A: 0–5, B: 5–7, C: 7–8. Flow times: f_A = 5, f_B = 6, f_C = 6 → f_mean = 17/3 ≈ 5,67. Wartezeiten: w_A = 0, w_B = 4, w_C = 5. Auslastung = 8/8 = 100 %.

### 2.6 Race Conditions ⭐🧮

**Definition:** Race Condition (auch *data race*): Das Gesamtergebnis ist nur korrekt, wenn jeder Thread/Prozess seine Berechnung in einer **kritischen Sektion (critical section)** zufällig **am Stück** durchführt. Heimtückisch, schwer reproduzierbar. Folgen: falsche Werte, Datenkorruption, Absturz, undefiniertes Verhalten.

**Warum?** Eine CPU rechnet in drei Schritten: (1) Variable aus Hauptspeicher in **Register laden**, (2) im Register rechnen, (3) Ergebnis **zurückschreiben**. Ein Kontextwechsel kann zwischen diesen Teilschritten passieren („each abstraction leaks").

🧮 **Klassiker:** zwei Threads führen je `++result; ++result;` aus (result = 0) → erwartet 4, möglich u. a. **3**:

```
A: lade 0 → r0        A: r0 = 1        A: schreibe 1
B: lade 1 → r1
A: lade 1 → r0
B: r1 = 2             B: schreibe 2    (überschreibt …)
A: r0 = 2             A: schreibe 2
B: lade 2 → r1        B: r1 = 3        B: schreibe 3   → Ergebnis 3
```

Auch eine einzelne Rechenoperation besteht aus Teilstücken. Bei Prozessen seltener, weil (fast) keine geteilten Variablen.

**Lösung: Mutex** (*Mutual Exclusion*, „Belegungsflagge")
- `m.lock()`: warte, bis frei, dann belegen. `m.unlock()`: freigeben.
- Nur **ein** Thread gleichzeitig kann den Mutex halten, andere warten (idle waiting oder Wechsel in Zustand *blockiert*).
- Lock/Unlock sind Systemaufrufe (kümmern sich auch um Register-/Cache-Synchronisation).
- Die Reihenfolge *vor* dem Mutex bleibt undefiniert (z. B. Ergebnis „Alice" oder „Bob"), aber kein undefiniertes Verhalten mehr.
- **Threadsichere Methode:** darf von beliebigen Threads aufgerufen werden (Mutex als Membervariable). **Threadsichere Klasse:** alle mehrfach aufrufbaren Methoden threadsicher (alle außer Konstruktor/Destruktor).
- Bei `get()` Rückgabe **per Kopie**, nicht per Referenz.

**Achtung:** Auch mit Mutex kann es Race Conditions geben, wenn zu fein gesperrt wird (z. B. `vorname` und `nachname` einzeln gelockt → „Bob Liddell" möglich). Ob etwas eine Race Condition ist, hängt von der **Anwendung** ab.

### 2.7 Deadlocks ⭐🧮

**Definition:** Zwei (oder mehr) Threads warten unbegrenzt auf die Freigabe eines Mutex, den der jeweils andere hält. Da beide warten, kann keiner freigeben.
Symptom: Programm hängt manchmal („zufällig"), nur bei ungünstiger Abarbeitungsreihenfolge.

**Beispiel:** Thread A: `lock(m_vorname)`, dann `lock(m_nachname)`; Thread B: `lock(m_nachname)`, dann `lock(m_vorname)`. Wenn B seinen ersten Lock zwischen A's erstem und zweitem Lock macht → Deadlock.

**Die 4 Bedingungen (Coffman) – alle gleichzeitig nötig und hinreichend:** ⭐
1. **Mutual Exclusion:** Mutexe sind exklusiv.
2. **No Preemption:** keine externe Freigabe, nur der belegende Thread gibt frei.
3. **Hold and Wait:** Thread hält einen Mutex und wartet auf einen weiteren.
4. **Circular Wait:** Zyklus aufeinander wartender Threads.

- *Hinreichend:* sind alle vier erfüllt → immer Deadlock. *Notwendig:* tritt ein Deadlock auf → alle vier erfüllt. → **Es genügt, eine Bedingung zu vermeiden.**
- Darstellung am **Betriebsmittelgraphen** (Zyklus beim Warten = Deadlock).

**Gegenmaßnahmen je Bedingung:**

| Bedingung | Maßnahme | Bewertung |
|---|---|---|
| 1 Exklusivität | – | liegt in der Natur der Sache, kaum Wahl |
| 2 No Preemption | wartende Threads müssen nach Wartedauer alle Mutexe freigeben und neu probieren | hofft auf passende Reihenfolge, umständlicher Programmfluss |
| 3 Hold and Wait | nur **ein** Mutex für alles (dann braucht man keine Threads) **oder** alle Mutexe gleichzeitig belegen | OS unterstützt Letzteres oft nicht richtig |
| 4 Circular Wait | **Ressourcen immer in derselben Reihenfolge belegen** (und umgekehrt freigeben) | **Praxislösung** |

---

## 3. Speicherverwaltung

### 3.1 Speicherhierarchie (Stand ca. 2020) ⭐

Näher am Rechenwerk = schneller, teurer, kleiner. Weiter weg = langsamer, billiger, größer.

| Ebene | Größe | Zugriffszeit | Besonderheit |
|---|---|---|---|
| **CPU-Register** | ca. 100–1000 Byte pro Kern (x64: 50–100 nutzbare Register à 8 Byte) | direkt am Rechenwerk | Verwaltung durch OS und Programme |
| **CPU-Cache** (L1–L3) | 1 kB … 100 MB | ca. 1–5 ns | Verwaltung **automatisch durch CPU** |
| **Hauptspeicher** | ca. 4 … 256 GB | ca. 5–20 ns | **flüchtig**, Zuteilung durch OS, direkter Zugriff |
| **Datenträger** | 100 GB … 20 TB | ca. 5–10 ms | **nicht flüchtig**, indirekter Zugriff über Systemaufrufe |

### 3.2 Hauptspeichermodell

- Folge von **Speicherzellen**, ab **0** lückenlos nummeriert. Die Nummer ist die **Adresse** (hexadezimal, z. B. `0xC1AABDCB`).
- Jede Zelle = **1 Byte** (Wert 0 … 255). Bits haben keine eigene Adresse.
- **Adresse ≠ Wert** (Analogie: Kontonummer ≠ Kontostand).
- Adresse 0 wird nicht für Daten genutzt → Marker `nullptr`/`NULL`.
- **Adressbreite b Bit → 2ᵇ Byte adressierbarer Hauptspeicher** (32 Bit: 2³² = 4 GB; 64 Bit: 2⁶⁴ ≈ 9 EB theoretisch).
- **Physisch verfügbarer** Hauptspeicher ist meist kleiner als der adressierbare. Zu den übrigen Adressen gibt es keine Zellen.
- **Bus:** Adressbus (wählt Zelle, Breite gibt Adressbreite vor) + Datenbus (überträgt Wert).
- **Wertvariable:** mehrere aufeinanderfolgende Zellen (z. B. `int` = 4 Zellen). **Zeigervariable:** Wertvariable, die die (erste) Adresse einer anderen Variable speichert.

### 3.3 Die vier Probleme der Speicherverwaltung ⭐

Annahme: Prozesse brauchen ihren Speicher **am Stück** (Partition), evtl. mehr als physisch vorhanden.

| # | Problem | Beschreibung | Naive Lösungen |
|---|---|---|---|
| 1 | **Fragmentierung** | Hauptspeicher zerfällt in Lücken, die zusammen genug Platz hätten, aber nicht am Stück. **Externer Verschnitt** = freie Lücken zwischen Partitionen. **Interner Verschnitt** = allozierter, aber ungenutzter Teil einer Partition. | – (Lösung: virtueller Speicher) |
| 2 | **Zusatzbelegung** | Prozess weiß vorher nicht, wie viel Speicher er braucht, Partition muss wachsen können. | viel zu viel vorsorglich reservieren; in freien Nachbarspeicher wachsen; Prozess auslagern und woanders einlagern |
| 3 | **Speicherschutz** | Prozesse könnten fremde Daten lesen/ändern (Fehler oder Absicht). | Zugriff nur über (langsame) Systemaufrufe; CPU-Schutzcodes; **Basis-/Grenzregister** |
| 4 | **Relokation** | Adressen (Verweise) in Programm gehen kaputt, wenn die Partition verschoben oder an anderer Stelle geladen wird. | alle Verweise beim Laden/Verschieben anpassen; Adressmodifikation mit Basis-/Grenzregistern |

**Lösung aller vier: virtueller Speicher.**

### 3.4 Virtueller Speicher ⭐🧮

- Jeder Prozess hat einen **eigenen virtuellen Adressraum** (pro Prozess neu durchgezählt, ohne echte Zellen).
- Eine **Adressabbildung** übersetzt virtuelle in **physische Adressen**.
- Folgen: Es gibt virtuelle Adressen ohne physische und umgekehrt. Dieselbe virtuelle Adresse kann bei zwei Prozessen auf verschiedene Daten zeigen.

**Seiten und Rahmen (Paging):**
- Virtueller Adressraum wird in **Seiten (pages)** fester Größe zerlegt, Hauptspeicher in **Rahmen (frames)** gleicher Größe.
- Seiten werden auf Rahmen abgebildet, oder auf Sonderfälle (unbenutzt, ausgelagert).

**Adressaufbau:**

```
virtuelle Adresse:   | Seitennummer | Seitenoffset |
                          │               │ (bleibt unverändert)
                    Seitentabelle           │
                          ▼               ▼
physische Adresse:   | Rahmennummer | Seitenoffset |
```

- Seitennummer = Abstand der Seite (in Seiten) vom Anfang des Adressraums. Offset = Byte-Abstand innerhalb der Seite.
- Seiten- und Rahmennummern haben **dieselbe Bit-Breite**. Es gibt Rahmennummern, zu denen kein Rahmen existiert.

**Seitentabelle (pro Prozess):** nach Seitennummer sortierte Tabelle mit Rahmennummer.

| Bit/Feld | Bedeutung |
|---|---|
| **Present-Bit** | Seite liegt aktuell im Hauptspeicher (0 = ausgelagert → **Seitenfehler**) |
| **Reference-Bit / R-Bit** | kürzlich auf Seite zugegriffen |
| **Modify-/Used-Bit** | seit Einlagerung wurde auf die Seite geschrieben |
| **Schutz-Modus / Read-Only-Bit** | Schreibzugriff führt zum Prozessabbruch / Zugriffsfehler |
| Prozess-ID | wem gehört die Tabelle |

Bewertung: einfache Seitentabellen sind billig (Zeigerarithmetik), brauchen aber Platz für **alle** Seiten, auch unbelegte → hoher Speicherbedarf pro Prozess. Abhilfe: hierarchische oder invertierte Seitentabellen (nicht Prüfungsstoff der VL).

🧮 **Rechenschema Adressbreite:** ➕
- Adressbreite b Bit, Seitennummer p Bit → Offset = b − p Bit.
- Virtueller Adressraum = 2ᵇ Byte. Seitengröße = 2^(b−p) Byte. Anzahl Seiten = 2ᵖ.
- Physischer Hauptspeicher ≤ 2ᵇ Byte, Anzahl Rahmen = Speichergröße / Rahmengröße.

🧮 **Vollständiges Folienbeispiel (5-Bit-OS, 3 Bit Seitennummer):**
- 2⁵ = 32 virtuelle Adressen → Adressraum 32 Byte. Offset = 5 − 3 = **2 Bit** → Seite/Rahmen = 2² = **4 Byte**. 8 Seiten.

| Seite | Rahmen | Present | Used | Read-Only |
|---|---|---|---|---|
| 000 | 100 | 1 | 1 | 1 |
| 001 | 000 | 0 | 0 | 0 |
| 010 | 000 | 1 | 1 | 0 |
| 011 | 000 | 0 | 0 | 0 |
| 100 | 010 | 1 | 1 | 0 |
| 101 | 101 | 1 | 1 | 0 |
| 110 | 000 | 0 | 1 | 0 |
| 111 | 011 | 1 | 1 | 0 |

- **Lesen von 11110:** Seite 111 → Rahmen 011, Offset 10 → physisch **01110**.
- **Schreiben auf 00000:** Seite 000 → Rahmen 100 → physisch 10000, aber Read-Only = 1 → **Zugriffsfehler** (Prozessabbruch).
- **Schreiben auf 11011:** Seite 110, Present = 0 → **Seitenfehler**, Seite muss nachgeladen werden.

**Vorgehen in der Klausur:** 1. Adresse in Seitennummer + Offset zerlegen. 2. Seitentabellenzeile suchen. 3. Present-Bit prüfen (0 → Seitenfehler). 4. Rechte prüfen (Read-Only → Zugriffsfehler). 5. Rahmennummer + Offset zusammensetzen.

### 3.5 Behandlung von Seitenfehlern ⭐

**Seitenfehler:** Zugriff auf eine Seite, der kein Rahmen zugewiesen ist (nie benutzt oder ausgelagert).

**Allokation allgemein:** Beim Start bekommt der Prozess vom OS vorbereitete Seiten (Code, Stack des Hauptthreads). Danach: (a) Prozess fordert per Systemaufruf (`malloc`) Speicher an → OS weist neue Seiten/Rahmen zu und passt die Tabelle an; (b) Prozess greift per Maschinencode auf virtuelle Adresse zu → CPU übersetzt über die Seitentabelle oder meldet Seitenfehler ans OS.

**10 Schritte der Seitenfehlerbehandlung:**
1. CPU bemerkt den Seitenfehler, sichert den Instruktionszähler, löst **Kernel-Trap** aus.
2. OS sichert die Registerinhalte des laufenden Prozesses.
3. OS bestimmt die aufgerufene virtuelle Seite.
4. OS prüft Zugriffsrechte und sucht einen **freien Rahmen**.
5. Ist keiner frei: OS **verdrängt** eine Seite (suspendiert evtl. deren Prozess X) und sichert den Inhalt auf den Datenträger. *(Prozesswechsel zu anderem bereiten Prozess möglich.)*
6. OS liest die angeforderte Seite vom Datenträger in den Rahmen.
7. OS aktualisiert die Seitentabelle.
8. OS setzt den Instruktionszähler auf den fehlerverursachenden Befehl.
9. OS versetzt den evtl. suspendierten Prozess X in *bereit*.
10. OS restauriert den Prozess und setzt die Ausführung fort (Prozess wird bereit).

**Verdrängungsstrategien** (welche Seite fliegt raus, wenn alle Rahmen belegt sind?). Eingabe: **Referenzkette** = Folge der zugegriffenen Seitennummern.

| Strategie | Idee | Bewertung |
|---|---|---|
| **FIFO** | verdränge die Seite, die am längsten im Speicher ist (Umsetzung: **Clock-Algorithmus**, wandernder Zeiger auf älteste Seite) | einfach, aber auch oft benutzte Seiten fliegen raus; in der Praxis selten; **Beladys Anomalie** |
| **Belady / OPT** (1966) | verdränge die Seite, die **in Zukunft am längsten nicht gebraucht wird** | **minimale** Seitenfehlerzahl, aber Zukunft unbekannt → nur als **Maßstab** |
| **Aging** | pro Seite R-Bit + Schieberegister: in jedem Takt (z. B. 20 ms) R-Bit **links** einschieben, Register nach rechts schieben, R-Bit zurücksetzen; **verdränge Seite mit kleinstem Registerwert** | heuristisch, berücksichtigt letzte Zugriffszeit **und** Häufigkeit |

🧮 **Referenzkette der Folien:** `0 1 2 3 0 1 4 0 1 2 3 4`

| Verfahren | Rahmen | Seitenfehler |
|---|---|---|
| FIFO | 3 | **9** |
| FIFO | 4 | **10** ← mehr Rahmen, mehr Fehler = **Beladys Anomalie** |
| OPT (Belady) | 4 | **6** ➕ (selbst nachgerechnet) |

**Beladys Anomalie:** Intuitiv gilt „mehr Rahmen → weniger Seitenfehler". Das stimmt bei FIFO **nicht immer** (Gegenbeispiel oben).

🧮 **FIFO-Rechenschema mit 3 Rahmen** ➕ (zum Üben nachvollziehen):

| Zugriff | 0 | 1 | 2 | 3 | 0 | 1 | 4 | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rahmen 0 | 0 | 0 | 0 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 4 | 4 |
| Rahmen 1 | | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 2 |
| Rahmen 2 | | | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 3 | 3 |
| Fehler? | F | F | F | F | F | F | F | – | – | F | F | – |

= 9 Fehler.

🧮 **Aging-Beispiel (Folie):** Nach Takt 4 stehen die Register A = 01111000, B = 10110000, C = 10001000, D = 00100000, E = 01011000, F = 00101000. **Kleinster Wert = D → D wird verdrängt.**
Rechenweg je Takt: Register alt >> 1, dann R-Bit als neues linkes Bit.

---

## 4. Dateiverwaltung

### 4.1 Warum Dateien? (Motivation)

Hauptspeicher ist **begrenzt, flüchtig, pro Prozess virtualisiert, prozesszentriert** (für Endnutzer unverständlich). → Daten in größerem, **nicht flüchtigem**, **zwischen Prozessen geteiltem**, für Nutzer verständlich organisiertem Speicher = **Dateien auf einem Dateisystem**.

### 4.2 Kernbegriffe ⭐

| Begriff | Definition |
|---|---|
| **Datei** (file) | Dateneinheit zur **persistenten** Speicherung auf Datenträgern |
| **Dateisystem** (FS) | Strukturierung der Dateien und Verwaltungsinformationen auf Datenträgern (FAT, NTFS, HFS, ZFS, ext2 …) |
| **Dateiname** | Name zum Wiederauffinden; wird bei Löschen/Umbenennen freigegeben |
| **Dateiendung** | Konvention (kein Zwang!) für das Format, erlaubt Verknüpfung mit OS-Reaktion; keine oder mehrere Endungen möglich |

Regeln für Namen variieren: Zeichentabelle (ASCII, UTF-8, UCS2), erlaubte Zeichen, max. Länge (NTFS 256), Groß-/Kleinschreibung.

### 4.3 Dateiarten ⭐

| Art | Beschreibung |
|---|---|
| **Gewöhnliche Dateien** – Textdateien | nur Zeichen nach Zeichentabelle, Zeilenende OS-abhängig (`\n`, `\r\n`, `\r`), menschenlesbar |
| **Gewöhnliche Dateien** – Binärdateien | beliebige Bytefolge, Semantik durch **Dateiformat**, speichereffizienter, nicht zwingend lesbar |
| **Verzeichnisse** | binäre Systemdateien zur Verwaltung des Dateisystems |
| **Gerätedateien** (Spezialdateien) | virtuelle Dateien, die Daten speziell behandeln: **zeichenorientiert** (byteweise, z. B. Terminal), **blockorientiert** (größere Blöcke, z. B. Hardware), **Pseudo-Geräte** (algorithmisch erzeugter Inhalt, z. B. Zufallszahlen) |

### 4.4 Links ⭐

| Link | Beschreibung |
|---|---|
| **Hard Link** | zusätzlicher Verzeichniseintrag, der einen Namen mit **derselben Datei** (Metadaten) verbindet; Datei in mehreren Verzeichnissen; Verwaltung z. B. per **Referenzzähler** |
| **Sym-Link** (soft link) | eigene Datei, die das OS automatisch zur Zieldatei auflöst. **Slow:** Pfad steht in einer extra Datei. **Fast:** Pfad steht in den Metadaten |

### 4.5 Dateiattribute (Metadaten)

Beispiele: Schutzinfos, Passwort, Erzeuger, Eigentümer, Read-Only-, Hidden-, System-, Archive-, ASCII/Binary-, Random-Access-, Temporary-, Lock-Flag, Zeiten (Erzeugung, letzter Zugriff, letzte Änderung), aktuelle Größe, Maximalgröße.

**Linux-Rechte** ⭐: 3 Kategorien × 3 Rechte.
- Kategorien: **u** (user), **g** (group), **o** (other). Rechte: **r**ead, **w**rite, e**x**ecute.
- `-rw-r--r--` = Datei (`-`; `d` = Verzeichnis), Besitzer rw, Gruppe r, andere r.

### 4.6 Dateizugriff und -struktur

| Zugriff | Beschreibung |
|---|---|
| **Sequentiell** | nur der Reihe nach von Anfang an (Magnetband); Zurückspulen teuer |
| **Wahlfrei (random access)** | beliebige Reihenfolge (Festplatte, USB-Stick), über **Positionszeiger**: `read()`/`write()` verschieben ihn, `seek()` verschiebt ihn ohne Lesen/Schreiben |

| Struktur | Beschreibung |
|---|---|
| **byte-sequentiell** | lückenlose Folge von Bytes (Systemaufrufe heute) |
| **block-sequentiell** | Folge disjunkter, meist gleich großer Blöcke (Hardware heute) |
| **hierarchisch** | Baum aus Eltern- und Kindblöcken, effizientes Suchen/Austauschen |

**Dateioperationen (Systemaufrufe):** `create`, `delete`, `rename`, `open`, `close`, `read`, `write`, `seek`, `getAttributes`, `setAttributes`.

### 4.7 Verzeichnisse ⭐

- Lösen das Problem rechnerweit eindeutiger Namen: Name muss nur **innerhalb des Verzeichnisses** eindeutig sein. Meist selbst als Datei realisiert, ein Eintrag pro Datei.
- **Verzeichnisbaum:** Wurzelverzeichnis hat kein Elternverzeichnis, ein Verzeichnis darf sich nicht selbst enthalten (auch nicht indirekt).
- Ältere/seltene Varianten: ein Verzeichnis für den ganzen Rechner; ein Verzeichnis pro Benutzer; ein Baum pro Benutzer.
- **Datei öffnen:** OS durchsucht die Verzeichnisdatei nach dem Namen, holt Attribute und Plattenadresse, legt sie in einer Tabelle im Hauptspeicher ab (**Datei-Handle**); weitere Zugriffe nutzen diese Infos.
- **Verzeichnisoperationen:** `create_dir`, `delete_dir`, `open_dir`, `close_dir`, `read_dir`.

### 4.8 Pfade ⭐🧮

| Begriff | Bedeutung | Beispiel |
|---|---|---|
| **Pfadname** | Folge von Verzeichnisnamen mit Trennzeichen (`/` Linux, `\` Windows, `>` MULTICS) | |
| **absoluter Pfad** | ausgehend vom Wurzelverzeichnis | `C:\Windows\notepad.exe`, `/bin/cd` |
| **relativer Pfad** | ausgehend vom **Arbeitsverzeichnis** (pro Prozess wählbar) | `images\cat.jpg` |
| **Pseudo-Verzeichnisse** | `..` = übergeordnetes, `.` = aktuelles Verzeichnis | |
| **kanonischer Pfad** | genormt, **ohne** Pseudo-Verzeichnisse | `C:\Windows\notepad.exe` (absolut + kanonisch); `Documents/Texts/../Images/image.jpg` (relativ, **nicht** kanonisch) |

**Wozu kanonisch?** Zwei nicht-kanonische Pfade können dieselbe Datei meinen. Ein String-Vergleich genügt dann nicht → erst in kanonische Form umwandeln, dann vergleichen.

🧮 **Übung:** Arbeitsverzeichnis `C:\Programme\Photoshop`, relativer Pfad `dog\.\..\Steam\Steam.exe` → `dog` betreten, `.` bleibt, `..` zurück → `C:\Programme\Photoshop\Steam\Steam.exe`. *(Die Folie löst auf `C:\Programme\Steam\Steam.exe` auf. Rechne beim Üben immer Schritt für Schritt und beachte das Arbeitsverzeichnis!)*

### 4.9 Datenträger, Partitionen, Booten

**Datenträgermodell:** Folge von Speicherzellen mit Adressen. Adressierbare Größe hängt vom **Dateisystem** ab (typisch 2³² … 2⁶⁴ Byte), nicht von der CPU.

**Partitionen:**
- Datenträger enthält mehrere unabhängige Partitionen (je eigenes Dateisystem).
- **GPT** (GUID-Partitionstabelle) gibt Start/Ende der Partitionen an. **MBR** ist veraltet.
- Typische Partition: **Bootblock** (Einstiegsprogramm für OS) | **Superblock** (Parameter des Dateisystems) | **Freispeicherverwaltung** | **I-Nodes** | **Wurzelverzeichnis** | Dateien/Verzeichnisse.

**Booten (UEFI, BIOS ähnlich):**
1. UEFI prüft Hardware (**POST**, power-on self-tests).
2. UEFI bestimmt zu bootendes OS (bei GPT) bzw. Datenträger (bei MBR).
3. UEFI startet OS-spezifischen **Bootloader** (GPT: aus separater **EFI-Partition**; MBR: allgemeiner Bootloader im MBR → Bootloader der aktiv markierten Partition).
4. Bootloader startet das OS.
5. OS sucht Gerätetreiber und lädt sie in den Kern.
6. OS erzeugt Verwaltungstabellen und Hintergrundprozesse.
7. OS startet GUI mit Login.

BIOS (seit ca. 2010 veraltet) vs. **UEFI** (ab ca. 2000): UEFI unterstützt Datenträger > 2 TB und GPT, Grafik beim Booten, **Secure Boot**.

### 4.10 Allokationsverfahren (Wo liegen die Blöcke einer Datei?) ⭐🧮

| Verfahren | Idee | Vorteile | Nachteile |
|---|---|---|---|
| **Kontinuierlich** | Datei = zusammenhängende Blöcke | einfach, **sehr schneller Zugriff** (ein Stück) | maximale Dateigröße im Voraus nötig; **externe Fragmentierung** durch Löschen |
| **Verkettete Liste** | erstes Wort jedes Blocks = Zeiger auf nächsten Block; Verzeichnis kennt nur Startblock | **keine** externe Fragmentierung, sequentiell effizient | **wahlfreier Zugriff langsam** (Liste ablaufen); Nutzdaten pro Block **keine Zweierpotenz** |
| **FAT** (File Allocation Table) | Zeiger der Liste in **separater Tabelle** (Index = Block-ID, Eintrag = nächster Block, `NIL` = Ende); FAT liegt im Hauptspeicher | wahlfreier Zugriff effizient (nur gesuchter Block von Platte), Blockgröße wieder Zweierpotenz | **FAT braucht viel Hauptspeicher** (für die ganze Platte) |
| **I-Nodes** (Index-Knoten) | eine Struktur fester Größe pro Datei mit Attributen + Blockadressen; nur für **geöffnete** Dateien im Hauptspeicher | geringerer Speicherbedarf | feste Größe → nur begrenzt viele Blockadressen |
| **Mehrstufige I-Nodes** | für große Dateien verweisen Einträge auf Blöcke, die selbst Adressen enthalten (einfach-, zweifach-, dreifach-indirekt) | skaliert für große Dateien | zusätzliche Zugriffe |

Praxis-Idee der I-Nodes: viele kleine Dateien, wenige große → I-Node für übliche Größen auslegen, Sonderlösung (indirekte Blöcke) für große.

🧮 **FAT-Größe (Folienbeispiel):** 8 TB Platte, 16 KB Blöcke → 2⁴³ / 2¹⁴ = **2²⁹ Einträge**, je 5 Byte → ca. **2,5 GB** FAT im Hauptspeicher.
Allgemein ➕: Einträge = Plattengröße / Blockgröße; FAT-Größe = Einträge × Eintragsgröße.

🧮 **Verkettete Liste / FAT lesen (Folienbeispiel):** Datei A, Startblock 4: 4 → 7 → 2 → 10 → 12 → NIL (5 Blöcke). Datei B, Startblock 6: 6 → 3 → 11 → 14 → NIL.

### 4.11 Praxisbeispiele Dateisysteme

**MS-DOS / FAT:**
- Kein Benutzerkonzept, Baumstruktur ohne Links, Verzeichniseinträge **32 Byte**, Namen **8 + 3** Großbuchstaben, Größe max. 4 GB, erste Blocknummer verweist in die FAT.
- Eintrag: 8 B Name, 3 B Typ, 1 B Attribute, 10 B ungenutzt, 2 B Uhrzeit, 2 B Datum, 2 B Blocknummer, 4 B Größe.
- **FAT12/16/32:** 12, 16 bzw. 28 Bit für Plattenadressen. Plattenblockgröße = Vielfaches von 512 Byte. Max. 4 Partitionen unter MS-DOS.
- Größere Blöcke → größere Partitionen, aber **mehr Verschnitt bei kleinen Dateien**.
- **exFAT:** für Flash-Speicher, Dateien bis 16 EB, Rechtevergabe.

**NTFS** (ab Windows NT): 64-Bit-Adressen, Dateien aus mehreren **Datenströmen** (`file1:stream2`), Pfad ≤ 255 Unicode-Zeichen (ab Win 10 beliebig lang), **ACLs**, **Master File Table (MFT)** mit Bitmap für freie Blöcke und einem MFT-Eintrag pro Datei. Eintrag = Kopf, Standardinfo, Dateiname, Info über Datenblöcke als **Läufe (Runs)**: Blocknummer + Länge (z. B. Blöcke 20–23, 64–65, 80–82).

**UNIX / ext2:**
- Verzeichniseintrag nur **Dateiname (14 B) + I-Node-Nummer (2 B)**; alles andere im I-Node. I-Node des Wurzelverzeichnisses liegt an fester Stelle.
- ext2-I-Node: Modus (z. B. `rw-rw-r--`), Link Count, Owner UID/GID, Größe, 3 Zeitstempel (Erzeugung, letzter Zugriff, letzte Änderung), **Adressen der ersten 12 Blöcke**, dann **1-, 2-, 3-fach indirekt**.

🧮 **Pfadauflösung in UNIX, z. B. `/usr/ast/mbox`** ⭐:
1. Wurzelverzeichnis (fester I-Node) durchsuchen → `usr` hat I-Node 6.
2. I-Node 6 → Verzeichnis `/usr` liegt in Block 132. Dort `ast` → I-Node 26.
3. I-Node 26 → Verzeichnis `/usr/ast` in Block 406. Dort `mbox` → I-Node 60.
4. I-Node 60 → Plattenblöcke der Datei.
Relative Pfade analog, aber Start im Arbeitsverzeichnis.

**Journaling-Dateisystem:** Zeichnet Aktionen in einem **Journal** auf, **bevor** sie ausgeführt werden. Nicht ausgeführte Aktionen (Absturz) werden nachgeholt → robust gegen Abstürze (NTFS, ext4, ReiserFS, OS X).
Bedingungen: jede Aktion **idempotent** (mehrfache Ausführung wirkt wie einmalige, z. B. „markiere Block 127 als frei"), zusätzlich **atomar** (ganz oder gar nicht).

**Überblick (Auswahl):**

| FS | Hersteller | Jahr | Max. Datei | Journal | Bemerkung |
|---|---|---|---|---|---|
| FAT16 | Microsoft | 1987 | 2 GB | nein | 8.3-Namen |
| ext2 | R. Card | 1993 | 16 GB … 2 TB | nein | Linux, Hard- und Soft-Links |
| NTFS | Microsoft | 1993 | 16 EB | ja | Soft-Links |
| FAT32 | Microsoft | 1996 | 4 GB | nein | 8.3-Namen |
| ext4 | versch. | 2006 | 16 GB … 16 TB | ja | Linux |
| exFAT | Microsoft | 2006 | 16 EB | nein | Flash |

---

## 5. Ein- und Ausgabeverwaltung

### 5.1 Aufgaben und Geräteklassen

**Aufgaben des OS:** Schnittstelle zwischen Geräten und Rest bereitstellen; Steuerung und Überwachung aller E/A-Geräte: **Kommandos weiterleiten, Unterbrechungen abfangen, Fehler behandeln**.
Leitfrage: *Wie gelangen Daten von einem Peripheriegerät in den Hauptspeicher oder umgekehrt?*

| Klasse | Eigenschaft | Beispiele |
|---|---|---|
| **blockorientiert** (block devices) | Blöcke einzeln und unabhängig adressierbar | Festplatte |
| **zeichenorientiert** (character devices) | reine Zeichenströme | Tastatur, Drucker |

Klassifikation ist unvollständig (z. B. analoge Ausgaben fehlen), aber nutzbar für den geräteunabhängigen Softwareteil. Datenraten unterscheiden sich enorm (Tastatur 80 Bit/s … USB 3.0 4,8 GBit/s).

### 5.2 Geräte und Controller ⭐

- **Gerät (device):** extern vorhandene, früher oft mechanische Komponente.
- **Steuereinheit (controller):** elektrische Komponente, die ein oder mehrere **identische** Geräte steuert. Schnittstelle Controller ↔ Gerät meist standardisiert (PCI, SCSI, SATA, USB, IDE). Bietet eine komfortable OS-Schnittstelle.
- **Beispiel Festplatten-Controller:** wandelt zwischen **seriellem Bitstrom und Blöcken aus Bytes**, führt bei Bedarf **Fehlerkorrektur** durch, stellt das Ergebnis im Hauptspeicher bereit.
- Abstraktionsebenen: Anwendung („Datei lesen") → OS/Treiber („Byte 50321 der Platte lesen") → Controller („Spannung an Motor/Kopf legen").

### 5.3 Kommunikation mit Geräten ⭐

OS steuert ein Gerät durch Lesen/Schreiben von **Controller-Registern** bzw. eines **Datenpuffers**.

| Variante | Beschreibung | Eigenschaften |
|---|---|---|
| **Port-basierte E/A** | Register über spezielle Port-Befehle (z. B. `IN Reg3, Port7`) | nur über direkte Maschinenbefehle, **getrennte Adressräume** |
| **Speicherbasierte E/A (memory-mapped)** | Register sind in unbenutzten Hauptspeicherbereich eingeblendet | **reine Hochsprache möglich**, Schutz über virtuellen Speicher, **gemeinsamer Adressraum** |
| **Hybrid** | Ports für Controller-Register + speicherabgebildete **Datenpuffer** | getrennte Adressräume für Register |

**Probleme speicherbasierter E/A:**
- **Caching** muss für den abgebildeten Bereich (selektiv) ausgeschaltet sein.
- **Ein-Bus-Architektur:** alle Geräte und Speichermodule müssen immer den Adressbus abhören.
- **Zwei-Bus-Architektur:** Geräte können nicht auf die eingeblendeten E/A-Adressen reagieren. Lösungen: CPU schickt E/A-Befehl auf den E/A-Bus, falls der Speicher nach **Time-Out** nicht reagiert; oder Zusatzhardware (z. B. **PCI-Brücke**) überträgt E/A-Adressen vom Speicherbus auf den E/A-Bus.

### 5.4 DMA (Direct Memory Access) ⭐

**Problem:** Wortweises Kopieren durch die CPU kostet viel CPU-Zeit.
**Lösung:** separater **DMA-Controller** (heute meist in der Peripherie integriert).

**Ablauf:**
1. **CPU programmiert den DMA-Controller** (Adresse, Anzahl, Kontrolle) und den Laufwerk-Controller.
2. DMA fragt den Datentransfer beim Laufwerk-Controller an.
3. Daten werden vom Controller in den Hauptspeicher übertragen (zyklisch Wort für Wort).
4. Controller bestätigt (**ACK**).
5. Wenn fertig: **Unterbrechung (Interrupt)** an die CPU.

### 5.5 Unterbrechungen (Interrupts) ⭐

1. Controller (Gerät oder DMA) signalisiert ein Ereignis (z. B. E/A-Ende). Das **Unterbrechungswerk (Interrupt-Controller)** wählt die Unterbrechung mit der **höchsten Priorität** aus und speichert die anderen.
2. Unterbrechungswerk legt die **Geräte-ID (Unterbrechungsvektor)** auf den E/A-Bus und unterbricht die CPU.
3. CPU behandelt die Unterbrechung mit einer eigenen Routine (analog zu Systemaufrufen/Traps).

| | Präzise Unterbrechung | Unpräzise Unterbrechung |
|---|---|---|
| Eigenschaften | (1) **PC gespeichert**, (2) **alle Befehle vor dem PC beendet**, (3) **kein Befehl nach dem PC beendet**, (4) **Ausführungsstand des PC-Befehls bekannt** | Befehle um den PC haben unterschiedlichen Ausführungsstand |
| Folge | Befehle nach PC dürfen angefangen sein, aber alle Änderungen an Register/Speicher müssen rückgängig gemacht sein | CPU speichert den Zustand auf dem Stapel → **verlangsamt** die Behandlung |

### 5.6 Ziele der E/A-Software ⭐

| Ziel | Inhalt |
|---|---|
| **Geräteunabhängigkeit** | Programme greifen auf alle Geräte gleichartig zu, Gerät muss nicht vorher spezifiziert werden |
| **Benennungsschemata** | einheitliche Namen (Zeichenkette/Nummer), unabhängig von Hardware |
| **Fehlerbehandlung** | möglichst **nahe an der Hardware** (Verursacherprinzip) |
| **Synchrone Programmierung** | Übertragung synchron programmieren, **asynchron ausführen** |
| **Datenpufferung** | ermöglicht Analyse, entkoppelt unterschiedliche Übertragungsraten, **aber** Kopieraufwand |
| **Flexible Gerätenutzung** | gemeinsame und exklusive Nutzung möglich, ermöglicht aber **Deadlocks** |

### 5.7 Drei Arten der E/A-Steuerung ⭐🧮

Beispiel: Anwendung will einen Puffer der Länge `count` ausdrucken. Vorbereitung: (1) Prozess belegt Gerät (ggf. blockiert), (2) übergibt per Systemaufruf Daten an den Druckertreiber, (3) OS **kopiert** die Daten in den Kernpuffer `p[]`, (4) Ausgabe je nach Verfahren.

| | **Programmgesteuert (Polling)** | **Unterbrechungsgesteuert** | **DMA-gesteuert** |
|---|---|---|---|
| Ablauf | OS prüft in Schleife, bis Gerät bereit, sendet dann nächstes Zeichen | Systemaufruf schickt erstes Zeichen, Prozess wird blockiert; Gerät unterbricht CPU, wenn fertig; Handler sendet nächstes Zeichen | DMA-Controller führt die Übertragung durch, CPU wird nur am Ende unterbrochen |
| Vorteil | einfach programmierbar | **keine Blockierung** des OS | **keine CPU-Zeit verschwendet**, nur **eine** Unterbrechung pro Pufferfüllung |
| Nachteil | **Busy Waiting**, OS blockiert | **hohe CPU-Belastung**: eine Unterbrechung pro Zeichen | DMA-Controller **langsamer als die CPU**; bei unterbeschäftigter CPU sind Polling/Interrupt schneller |

Code-Muster Polling: `while (*printer_status_reg != READY) {}` dann `*printer_data_register = p[i];` in einer Schleife über alle Zeichen.
Nach Übertragungsende wird der Anwendungsprozess wieder **bereit** gesetzt (`unblock_user()`).

### 5.8 Schichtenmodell der E/A-Software ⭐

Eine Funktionalität pro Schicht, wohldefinierte Schnittstellen. Von oben nach unten (Anforderung) bzw. unten nach oben (Antwort):

```
4) Benutzer-Software mit E/A        (Bibliotheken, Spooling)
3) geräteunabhängige OS-Software    (uniforme Schnittstelle, Pufferung, Fehler, …)
2) Gerätetreiber
1) Unterbrechungsbehandlung
   Hardware
```

**Schicht 1 – Unterbrechungsbehandlung:** am besten vor der Anwendung versteckt. E/A-Operation blockiert die Anwendung, bis die Unterbrechung das E/A-Ende anzeigt; die Behandlungsroutine führt die E/A durch und **deblockiert** die Anwendung. Schritte (Reihenfolge maschinenabhängig): Register sichern, Kontext für Routine erzeugen (TLB, MMU, Paging), Stapel erzeugen, andere Unterbrechungen wieder zulassen, Register in Prozesstabelle kopieren, eigentliche Behandlung, nächsten Prozess wählen, MMU-Kontext des nächsten Prozesses initialisieren (inkl. TLB, Cache), Prozessregister laden, Prozess starten.

**Schicht 2 – Gerätetreiber:**
- Geräteabhängige Steuerungssoftware, **vom Gerätehersteller** pro Gerätetyp und OS.
- Läuft teilweise **im OS-Kern** → Installation nötig, **OS-Absturz durch Treiber möglich**.
- Sinnvolle Funktionen: Gerät initialisieren, Befehle ausführen, Gerät kontrollieren, Fehler melden, **wiedereintrittsfähig (reentrant)**, Geräte zur Laufzeit an-/abstecken (**hot pluggable**).

**Schicht 3 – geräteunabhängige E/A-Software:**
- **Uniforme Schnittstelle für Treiber** (z. B. als Datei im Dateisystem): reduziert OS-Anpassungsbedarf, erleichtert OS- und Treiber-Programmierung, aber Gerätefunktionalität nicht voll genutzt.
- **Pufferung**, **Fehlerbericht** (Rahmenwerk geräteunabhängig: bei Software-Fehler Fehlernummer an Anwendung, bei Hardware-Fehler bestimmt der Treiber die Reaktion), **Anforderung/Freigabe** exklusiver Geräte, **geräteunabhängige Blockgrößen** (Blockgrößen verstecken, Blöcke zusammenfassen).
- Die Grenze zwischen geräteabhängig und -unabhängig hängt von Gerät und OS ab.

**Schicht 4 – Benutzer-E/A-Software:** Bibliotheksroutinen (`write(fd, buf, n)`), Formatierung (`printf`), **Spooling-Dämon** für nur exklusiv nutzbare Geräte (verwaltet und serialisiert überlappende Aufträge).

### 5.9 Pufferungsvarianten ⭐

| Variante | Beschreibung | Eigenschaft |
|---|---|---|
| **Ungepuffert** | Anwendung blockiert bis zur E/A jedes nächsten Zeichens | **ineffizient** |
| **Pufferung im Benutzerraum** | E/A von n Zeichen in/aus Benutzerpuffer | Puffer ist **nicht auslagerbar** |
| **Pufferung im OS-Kern** | E/A in Kernpuffer, danach Kopie in/aus Benutzerraum | Kopieren und E/A **nicht gleichzeitig** |
| **Doppelte Pufferung** | E/A abwechselnd in zwei Kernpuffer, während der andere in den Benutzerraum kopiert wird | **überlappt Kopieren und E/A** |

**Nachteil jeder Pufferung:** häufiges **Kopieren** der Daten → E/A wird langsam. (Netzwerkbeispiel: Kern-Puffer → Treiber → Controller → Bus/Empfänger → Treiber → Anwendung: bis zu 5 Kopien.)

### 5.10 USB (Beispiel)

- **Hardware:** USB 3.0: 2 Strom- + 7 bit-serielle Datenleitungen, 4,8 GBit/s duplex. USB 3.1: 10 GBit/s, 100 W Power Delivery, symmetrischer Typ-C-Stecker. **Zentraler Host-Controller** koordiniert **≤ 127** sternförmig verbundene Geräte; durch **Hubs** physikalisch ein Baum mit logischen Punkt-zu-Punkt-Verbindungen. **Hot pluggable.**
- **Software:** generische Treiber für **Geräteklassen** (z. B. 01h Audio, 02h Kommunikation, 03h HID), individuelle Treiber nachladbar.
- **Übertragungsmodi:** **isochron** (feste Datenrate), **Interrupt** (begrenzte Latenz), **Bulk** (restliche Bandbreite), **Control** (kurze Nachrichten).

### 5.11 Sekundärspeicher und RAID ⭐

| Medium | Einsatz |
|---|---|
| Magnetische Festplatte (HD) | Dateisystem, Seitenauslagerung |
| Optische Medien (CD, DVD, Blu-ray) | kostengünstige Verteilung von Daten |
| SSD | schneller als HD, ohne bewegte Teile |
| RAID | hohe Zuverlässigkeit |

**RAID (Redundant Array of Inexpensive Disks):** logischer Datenträger aus mehreren physischen. Daten werden verteilt (**Striping**) → **höhere Leistung** durch parallelen Zugriff auf Strips, **höhere Zuverlässigkeit** durch Redundanz.

| Level | Prinzip | Redundanz |
|---|---|---|
| **RAID 0** | Striping | **keine** (nur Leistung) |
| **RAID 1** | Mirroring (Spiegelung) | Kopie auf zweiter Platte |
| **RAID 2** | Bit-Level-Striping (z. B. 7 Bit auf 7 Platten) | Fehlerkorrekturcode ➕ (Hamming) |
| **RAID 3** | Byte-Level-Striping | eine **Parity**-Platte |
| **RAID 4** | Block-Level-Striping (Strips) | eine **Parity**-Platte (P 0–3, P 4–7 …) |
| **RAID 5** | wie RAID 4, aber Parity **verteilt** über alle Platten | verteilte Parity, vermeidet Engpass der Parity-Platte ➕ |

➕ Parity wird als **XOR** der Datenstrips gebildet. Fällt eine Platte aus, lässt sich ihr Inhalt aus den übrigen Strips und der Parity rekonstruieren. Bei RAID 4 wird die Parity-Platte bei jedem Schreiben beansprucht, bei RAID 5 verteilt sich diese Last.

---

## X. Angriffe auf die Seitentabelle (Spectre / Meltdown)

### X.1 Instruktionsverarbeitung

**Von-Neumann-Architektur (ca. 1945):** CPU (= **Rechenwerk/ALU** + **Steuerwerk**), Hauptspeicher, Peripherie, verbunden über einen **Bus**. Maschinencode liegt **wie normale Daten** im Hauptspeicher.
- **Befehlszähler** (`$isp`, Instruction Pointer): Register mit der Adresse des nächsten Befehls. Steuerwerk bedient das Rechenwerk und setzt den Zähler danach weiter.

**4 Teilschritte eines Befehls** ⭐:
1. **Instruction Fetch:** Befehl über `$isp` aus dem Hauptspeicher holen.
2. **Instruction Decode:** dekodieren, Parameter nachladen.
3. **Execution:** im Rechenwerk ausführen.
4. **Write Back:** Ergebnisse zurückschreiben (Register, Speicher, `$isp`).

**Pipelining:** Teilschritte **späterer** Befehle beginnen, bevor frühere fertig sind → höherer Durchsatz.
🧮 4 Stufen, 3 Befehle: **6 Takte** statt **12** ohne Pipeline. ➕ Allgemein: k Stufen, n Befehle → **k + n − 1** Takte (Pipeline) bzw. **k · n** (ohne).

**Pipeline Hazard / Stall:** Ein Teilschritt eines späteren Befehls kann nicht laufen, weil frühere Befehle noch nicht fertig sind → frühere Stufen werden **angehalten (Stall)**.

| Hazard-Art | Ursache | Beispiel |
|---|---|---|
| **Datenkonflikt** | Vorbefehl berechnet Eingabe des Folgebefehls (Read-After-Write, analog Write-After-Read, Write-After-Write) | `add $r0,$r1,$r2` dann `addc $r2,1,$r4` |
| **Steuerkonflikt** | Befehl ändert den Befehlszähler (Sprung), nächster Befehl unbekannt | `set $isp, $r0` |

**Out-Of-Order-Execution:** Steuerwerk **ordnet unabhängige Befehle neu an**, um Bus/Rechenwerk/Steuerwerk besser auszulasten. Befehle mit Abhängigkeiten behalten ihre relative Reihenfolge. Das Ergebnis bleibt gleich.

**Bedingte Sprünge** (z. B. `beqc $r5, 1, adr` für `if (input == 1) …`): CPU weiß vorab nicht, ob gesprungen wird → Pipeline/OoO müssten warten → schlechte Auslastung.

**Branch Prediction (Sprungvorhersage)** ⭐:
- CPU **schätzt** den Ausgang nach Heuristik und füllt die Pipeline **spekulativ** mit Befehlen des geschätzten Pfades. Die Bedingung wird parallel ausgewertet.
- Richtig geschätzt → nichts zu tun. **Falsch geschätzt → fälschliche Folgeoperationen werden rückgängig gemacht.**
- Heuristik: pro bedingtem Sprungbefehl (Adresse) ein kleiner **CPU-interner Zähler** (z. B. −3 … +4), der bei genommenem Sprung +1, sonst −1 zählt. Sinnvoll, weil laut **Pareto-Prinzip** der Aufwand in wenigen inneren Schleifen liegt.

### X.2 Funktionales vs. nicht-funktionales Verhalten ⭐

| | Funktional | Nicht-funktional |
|---|---|---|
| Definition | durch Spezifikation festgelegt (z. B. was eine Rechnung ergibt) | nicht oder nur schwammig festgelegt (z. B. **wie lange** etwas dauert, in welchem Register Variablen liegen) |
| Programme | dürfen sich darauf verlassen | **Bug, wenn sich ein Programm darauf verlässt** |
| Bei Fehlschätzung | CPU **muss zurückabwickeln** | CPU **muss nicht** zurückabwickeln |

Warum wird nicht-funktionales nicht zurückgenommen? Korrekte Programme dürfen sich ohnehin nicht darauf verlassen, manches ist technisch kaum rückgängig zu machen, und das Ignorieren eröffnet Optimierungspotenzial.

**Beispiele nicht-funktionalen Verhaltens (= Seitenkanäle):**
- **Cache-Inhalt:** Liegt ein Datum schon im Cache, ist der Zugriff schneller (ca. 4 ns statt 20 ns in der Folie). Beim Laden kommt eine ganze **Cache Line** (z. B. 64 Byte) mit.
- **Seitentabelle:** Ob für eine allokierte Seite schon ein Rahmen vorbereitet ist, beeinflusst nur die Zugriffsdauer (erster Zugriff nach `malloc` dauert länger).
- Erweiterte Seitentabelle: **Alloc-Bit** (OS hat dem Prozess Platz eingeräumt), **Present-Bit**, **Used-Bit** (jemals Daten geschrieben), **Allow-Bits** (Zugriffsrechte).

**Nicht vollständig getrennte Seitentabellen:** Theoretisch perfekter Schutz durch überlappungsfreie Einträge. Praktisch werden Fremddaten zur Optimierung eingeblendet (geteilte Seiten, DLLs, OS-Seiten für Systemaufrufe, offene Dateien). Schutz erfolgt dann über **Zugriffsrechte** (z. B. Kernel-Mode-Bit) → Speicherzugriffsverletzung bei fehlendem Recht.

### X.3 Spectre (seit ca. 2017) ⭐

**Art:** **Seitenkanalattacke** (Beobachtung von nicht-funktionalem Verhalten) auf die Sprungvorhersage, nutzt den **Cache als Seitenkanal**.

**Ablauf:**
1. **Training:** Sprungvorhersage in einem bekannten Befehl (z. B. Bounds-Check `if (index < size_)` in `at()`) mit **gültigen** Abfragen trainieren, sodass „Sprung wird genommen" erwartet wird.
2. **Angriff:** Funktion mit **ungültigem Index** aufrufen (zeigt per Zeigerarithmetik auf geschütztes Datum). Die Bedingung ist eigentlich false, aber die CPU rechnet **spekulativ** weiter und liest das geschützte Datum. Es entsteht **kein Fehler**, weil der Sprung funktional nie genommen wird.
3. **Verraten über Cache:** Mit dem gelesenen Wert wird `attack_array[wert][0]` angesprochen (Array mit 256 cacheline-großen Teilarrays) → genau dieses Teilarray **landet im Cache**. Die funktionalen Folgen werden zurückgenommen, die **Cache-Änderung nicht**.
4. **Auswertung:** Alle 256 Teilarrays durchmessen (Zeitmessung). Das **schnellste** (z. B. 4 ns statt 20 ns) zeigt den gestohlenen Wert (im Beispiel Index 71 = Wert 71). Dafür braucht man einen **hochpräzisen Timer** (z. B. `QueryPerformanceCounter`), sonst Angriff wiederholen und Zeiten akkumulieren.

**Vorbereitung:** Cache leeren (z. B. 64 MB zufällige Daten schreiben/ausgeben), `attack_array` anlegen und Seitenzuteilung sicherstellen.
**Warum geht das?** `if`-Prüfungen sichern in Hochsprachen jeden Array-Zugriff, und jedes Array ist letztlich ein C-Array → solche Funktionen gibt es sehr oft.
🧮 `attack_index = steal_address − s.data()` (Zeigerarithmetik, Folienbeispiel: 949 − 143 = **806**).
Wichtig: Ein direktes Ausgeben von `attack_ref` im `try`-Block wäre funktional und würde zurückgenommen, deshalb der Umweg über den Cache.

### X.4 Meltdown (seit ca. 2017) ⭐

- Greift die **Out-Of-Order-Ausführung** direkt an, **ohne** bedingten Sprung → deutlich größere Angriffsfläche.
- Ablauf: Lesebefehl auf eine Speicherzelle **ohne Rechte** → die CPU meldet den Fehler dem OS, **legt aber trotzdem den Wert im Register ab**. Ein nachfolgender Zugriff `attack_array[wert][0]` wird per Out-of-Order **vor** der Fehlermeldung ausgeführt → Cache wird aktualisiert → Auswertung per Zeitmessung wie bei Spectre.
- Praktisch **zwei Threads** im selben Prozess: der **angreifende** Thread wird vom OS beendet, der **auswertende** misst weiter.
- **Unterschied zu Spectre:** Meltdown braucht nur Out-of-Order-Execution (kein Training der Sprungvorhersage).

### X.5 Schutzmechanismen ⭐

| Maßnahme | Wirkung | Kosten |
|---|---|---|
| CPU-Caching deaktivieren | nimmt den Seitenkanal weg | extrem, ca. **4-fache** Laufzeit |
| Out-of-Order-Execution/Sprungvorhersage deaktivieren (Microcode/Firmware) | verhindert spekulative Zugriffe | ca. **1,1- bis 1,2-fach** |
| Cache-Änderungen nach falscher Vorhersage zurücksetzen | schließt den Seitenkanal | zusätzliche Hardware, frisst Gewinn auf, ca. 1,1- bis 1,2-fach |
| OS: bei Seitenzugriffsfehler **ganzen Prozess** beenden (nicht nur Thread) | verhindert, dass der auswertende Thread weiterläuft (gegen Meltdown) | gering |
| **Page Table Isolation** | im User-Mode keine Seiten von OS/anderen Prozessen einblenden; zwei Seitentabellen (Kernel-Mode mit, User-Mode ohne Einblendungen), Wechsel bei Systemaufruf/Rücksprung | Wechsel zwischen Threads/Aufrufen **deutlich teurer** |
| **Jitter** | Zeitmessung verfälschen (Abrunden, Störsignal), sodass Cache-vs.-RAM-Unterschied (ns) nicht messbar ist | Fehler bei Anwendungen mit extrem genauer Zeit (z. B. Physik) |

---

## 6. Schnell-Check: Typische Klausurfragen

### Wissensfragen (ca. 25 %)
- [ ] Definiere: Prozess, Prozesskontext, Thread, Deadlock, Race Condition, Mutex, kritische Sektion, Datei, Dateisystem, Seitenfehler, DMA, Interrupt, Controller, Treiber.
- [ ] Nenne die **drei Prozesszustände** und die **vier Deadlock-Bedingungen**.
- [ ] Erkläre die **vier Probleme der Speicherverwaltung** und wie virtueller Speicher sie löst.
- [ ] Unterschied **Bottom-Up/Top-Down**, **Betriebsarten**, **OS-Strukturen**.
- [ ] Unterschied **Prozess ↔ Thread** (Tabelle in 2.4).
- [ ] **Ablauf eines Systemaufrufs** (8 Teilschritte).
- [ ] **Polling vs. Interrupt vs. DMA** mit Vor-/Nachteilen.
- [ ] **E/A-Schichtenmodell** und Aufgaben jeder Schicht.
- [ ] Unterschied **funktionales ↔ nicht-funktionales Verhalten**; wie funktionieren Spectre/Meltdown; welche Schutzmaßnahmen mit welchen Kosten?
- [ ] **Allokationsverfahren** (kontinuierlich, verkettet, FAT, I-Node) mit Vor-/Nachteilen.
- [ ] Was ist ein **Journaling-FS**? Warum idempotent/atomar?

### Anwendungsaufgaben (ca. 50 %) 🧮
- [ ] **Seitenersetzung** FIFO / OPT / Aging mit Referenzkette und n Rahmen, Seitenfehler zählen.
- [ ] **Adressübersetzung** virtuell → physisch mit gegebener Seitentabelle (inkl. Seitenfehler/Zugriffsfehler erkennen); Adress- und Seitengrößen aus Bitbreiten ableiten.
- [ ] **Scheduling:** Gantt-Diagramm für FCFS/EDF/Zeitscheiben, f_i, w_i, f_mean, Auslastung berechnen.
- [ ] **Race Condition:** mögliche Ergebnisse einer Verschränkung bestimmen; Mutex sinnvoll einsetzen.
- [ ] **Deadlock:** Betriebsmittelgraph zeichnen, Zyklus erkennen, Lösung durch feste Lock-Reihenfolge.
- [ ] **Pfade:** relative Pfade auflösen, kanonische Form bilden.
- [ ] **FAT/Verkettete Liste:** Blockfolge einer Datei verfolgen; FAT-Größe berechnen.
- [ ] **UNIX-Pfadauflösung** über I-Nodes und Verzeichnisblöcke.
- [ ] **Pipeline:** Takte mit/ohne Pipeline, Hazards identifizieren, Out-of-Order-Umsortierung.
- [ ] **Spectre:** `attack_index` per Zeigerarithmetik berechnen, Cache-Timing deuten.

### Theorie (ca. 25 %)
- [ ] Warum sind die vier Deadlock-Bedingungen **notwendig und hinreichend**, warum genügt es, eine zu verhindern?
- [ ] Warum ist OPT optimal, aber nicht umsetzbar? Warum kann FIFO bei mehr Rahmen schlechter werden?
- [ ] Warum gibt es keinen idealen Scheduler (Zielkonflikt Auslastung ↔ Bearbeitungszeit)?
- [ ] Warum müssen Seiten- und Rahmennummern gleich breit sein? Warum bleibt der Offset unverändert?
- [ ] Warum bleiben Cache-Effekte nach einer Fehlschätzung bestehen?

---

## 7. Mini-Glossar (Deutsch ↔ Englisch)

| Deutsch | Englisch |
|---|---|
| Betriebssystem / Kern | operating system (OS) / kernel |
| Systemaufruf | system call |
| Benutzermodus / Kernmodus | user mode / kernel mode |
| Prozess / Faden | process / thread |
| Kontextwechsel | context switch |
| Bereit-Warteschlange | ready queue |
| Verdrängung | preemption |
| Wettlaufsituation | race condition |
| kritische Sektion | critical section |
| Belegungsflagge | mutex (mutual exclusion) |
| Verklemmung | deadlock |
| Zeitscheibe | timeslice |
| Seite / Rahmen | page / frame |
| Seitentabelle | page table |
| Seitenfehler | page fault |
| Verdrängungsstrategie | page replacement |
| Referenzkette | reference string |
| Fragmentierung (extern/intern) | fragmentation |
| Steuereinheit | controller |
| Unterbrechung | interrupt |
| Unterbrechungswerk | interrupt controller |
| direkter Speicherzugriff | direct memory access (DMA) |
| Gerätetreiber | device driver |
| Wiedereintrittsfähigkeit | reentrancy |
| Datenträgerpartition | partition |
| Index-Knoten | I-Node |
| Sprungvorhersage | branch prediction |
| Seitenkanalangriff | side-channel attack |
| Befehlszähler | program/instruction counter (PC, `$isp`) |
