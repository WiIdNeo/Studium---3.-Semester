# Betriebssysteme – Lernleitfaden zur Probeklausur 2026

> **Ziel:** Alles, was du brauchst, um diese Probeklausur zu verstehen und Aufgaben dieser Art selbst zu lösen – auch wenn du in der Vorlesung kaum mitgekommen bist.
> **Hinweis:** Die Klausur fragt mehrfach nach Begriffen "gemäß VL". Ich verwende die Standardbegriffe der Betriebssystem-Lehre. Gleiche am Ende kurz mit deinem Skript ab, ob Namen (z. B. Zustandsnamen im Prozessdiagramm, Schreibweise "Belady-Verdrängung") genauso benutzt werden.

---

## 0. Überblick: Was wird abgefragt?

| Aufgabe | Thema | Punkte | Was du können musst |
|---|---|---|---|
| 1 | Grundlagen | 5 | Aufgaben eines OS, Mikrokernel, Mehrbenutzerbetrieb, Pfade (kanonisch/relativ) |
| 2a | Prozessverwaltung | 5 | Prozesszustände, Quasi-Parallelität, Blockiert-Zustand, Scheduling-Heuristik |
| 2b | Synchronisation / Deadlocks | 5 | Race Condition, Mutex, Deadlock + die 4 Bedingungen, Zyklusfreiheit |
| 3a | Seitenersetzung | 5 | FIFO-Tabelle rechnen, Belady-Verdrängung (= optimal) verstehen |
| 3b | Virtuelle Adressierung | 5 | Seiten/Rahmen/Offset rechnen, Seitentabelle lesen, Present-Bit |

**Gesamt: 25 Punkte.** Jede Teilfrage ist meist 1 Punkt, also: **kurze, präzise Antworten mit dem richtigen Fachwort + einer Begründung**.

**Lernreihenfolge nach Aufwand/Nutzen:**
1. **Aufgabe 3** (reine Rechenaufgaben, komplett erlernbar, 10 Punkte)
2. **Aufgabe 2b** (Fachwörter + 4 Deadlock-Bedingungen, 5 Punkte)
3. **Aufgabe 2a + 1** (Definitionen auswendig, 10 Punkte)

---

# Teil 1 – Grundlagen (Aufgabe 1)

## 1.1 Aufgaben eines Betriebssystems

Ein Betriebssystem (OS) hat **zwei grundsätzliche Aufgaben**:

### 1. Ressourcenverwaltung (Resource Manager)
- Das OS teilt knappe Betriebsmittel (CPU-Zeit, Hauptspeicher, Festplatte, Netzwerk, Drucker …) **zeitlich und räumlich** unter den Prozessen auf.
- **Zeitlich:** *wann* darf wer? (z. B. welcher Prozess darf wann auf die CPU / auf eine Datei zugreifen)
- **Räumlich:** *wo/wie viel* bekommt wer? (z. B. welcher Speicherbereich, wo liegt eine Datei auf der Platte)
- **Beispiel:** Wo liegt eine Datei auf der Festplatte, und wann darf welcher Prozess darauf zugreifen?

### 2. Hardware-Abstraktion (Virtuelle / erweiterte Maschine)
- Das OS versteckt die konkrete Hardware hinter **einheitlichen Schnittstellen** (Systemaufrufe / *system calls*).
- Anwendungen müssen nicht wissen, ob unter ihnen eine SSD, HDD oder ein USB-Stick liegt.
- **Beispiel:** Der Systemaufruf `open()` funktioniert gleich, egal welcher Datenträger oder welches Dateisystem dahinter steckt.

> **Merksatz:** *Verwalten* (Ressourcen fair und sicher verteilen) + *Verstecken* (Hardware abstrahieren).

## 1.2 Kernel, User Mode, Systemaufrufe (Hintergrundwissen)

- **Kernel** = der "eigentliche" Kern des OS, läuft im privilegierten **Kernel-Modus**.
- Anwendungen laufen im **User-Modus** und dürfen Hardware nicht direkt ansprechen.
- Will eine Anwendung etwas (Datei lesen, Speicher anfordern, Netzwerk nutzen), löst sie einen **Systemaufruf** aus (*trap*). Die CPU wechselt in den Kernel-Modus, das OS führt die Aktion aus und wechselt zurück.
- Vorteil: Ein fehlerhaftes Anwendungsprogramm kann nicht das ganze System zerstören.

## 1.3 Betriebssystem-Architekturen: Monolith vs. Mikrokernel

| | **Monolithischer Kernel** | **Mikrokernel** |
|---|---|---|
| Idee | Alle OS-Funktionen (Dateisystem, Treiber, Speicherverwaltung, Netzwerk …) laufen im Kernel | Kernel ist minimal, alles andere läuft als normale Prozesse ("Server") |
| Beispiele | klassisches Linux, klassisches Unix | Minix, QNX, L4, Mach |
| Vorteile | schnell (wenig Wechsel/Kommunikationsaufwand) | robust, modular, kleiner vertrauenswürdiger Kern; ein Treiber-Absturz reißt nicht das System mit |
| Nachteile | Fehler in einem Treiber kann das ganze System abstürzen lassen | langsamer wegen viel Nachrichtenaustausch |

### Was ist ein Mikro-Kernel? (Klausurantwort, 1P)
Bei Betriebssystemen mit **Client-Server-Architektur** ist das "eigentliche" OS, der Kernel, auf ein **Nachrichtenübermittlungssystem** zusammengestutzt. Dieses **startet, beendet und verwaltet Prozesse** und **vermittelt Nachrichten zwischen ihnen**. Weitere typische Kernelfunktionen (z. B. **Dateiverwaltung**) sind **nicht** Teil des Mikrokerns, sondern in **laufende Anwendungsprozesse ausgelagert**.

## 1.4 Mehrbenutzer-Betrieb (Multi-User)

Abgrenzung, die häufig verwechselt wird:

| Begriff | Bedeutung |
|---|---|
| **Mehrbenutzerbetrieb (Multi-User)** | Mehrere **angemeldete Benutzer** werden (i. d. R. gleichzeitig) bedient, jeder mit eigenen Rechten, Dateien und Prozessen |
| **Mehrprogrammbetrieb / Multitasking** | Mehrere **Prozesse** laufen (quasi-)gleichzeitig |
| **Multiprocessing** | Mehrere **CPUs/Kerne** rechnen echt parallel |
| **Multithreading** | Mehrere **Threads** innerhalb eines Prozesses |

### Klausurantwort (1P)
Das OS unterstützt die (in der Regel) **gleichzeitige Bedienung mehrerer angemeldeter Benutzer**. Beispiel: Ein Server, auf dem sich mehrere User anmelden und jeweils eigene Prozesse starten können. (Dazu gehören Benutzerkonten, Rechteverwaltung, Trennung der Benutzer voneinander.)

## 1.5 Pfade: absolut, relativ, kanonisch

### Absolut vs. relativ
- **Absoluter Pfad:** beginnt an der **Wurzel** des Dateisystems.
  - Unix/Linux: `/home/anna/test.txt`
  - Windows: `C:\Users\Anna\test.txt`
- **Relativer Pfad:** beginnt **nicht** an der Wurzel, sondern wird **relativ zum aktuellen Arbeitsverzeichnis** interpretiert.
  - `testordner/test.txt`, `../bilder/foto.png`, `./skript.sh`

### Kanonisch vs. nicht kanonisch
- **Kanonischer Pfad:** eine **eindeutige, bereinigte Form** ohne **Pseudo-Verzeichnisse** (`.` = aktuelles Verzeichnis, `..` = Elternverzeichnis) (und ohne überflüssige Trennzeichen wie `//`).
- **Nicht kanonisch:** enthält `.` oder `..`, z. B. `/home/anna/../bob/./datei.txt` (kanonisch wäre `/home/bob/datei.txt`).

### Die vier Kombinationen

| | absolut | relativ |
|---|---|---|
| **kanonisch** | `/home/bob/datei.txt` | `testordner/test.txt` |
| **nicht kanonisch** | `/home/anna/../bob/datei.txt` | `../ordner/./datei.txt` |

### Klausurantwort (1P)
**Ja, das geht.** `testordner/test.txt` ist **kanonisch** (enthält keine Pseudo-Verzeichnisse `.`/`..`) und **relativ** (fängt nicht an der Wurzel `C:/` bzw. `/` an).

> Achtung: `../test.txt` wäre relativ, aber **nicht** kanonisch, weil `..` ein Pseudo-Verzeichnis ist.

---

# Teil 2 – Prozessverwaltung (Aufgabe 2a)

## 2.1 Grundbegriffe

- **Programm:** passive Datei mit Code auf der Platte.
- **Prozess:** ein **laufendes Programm** samt seinem Zustand (Adressraum, Register, offene Dateien …).
- **Prozesskontrollblock (PCB):** Datenstruktur des OS, in der es alles über einen Prozess speichert (Zustand, Programmzähler, Registerinhalte, Speicherinfos …).
- **Kontextwechsel (context switch):** Das OS sichert den Zustand des aktuellen Prozesses (in den PCB) und lädt den Zustand des nächsten. Kostet Zeit, ist aber die Grundlage des Multitaskings.
- **Scheduler:** Komponente, die entscheidet, **welcher Prozess als Nächstes auf die CPU darf**.
- **Dispatcher:** führt den Wechsel tatsächlich durch.

## 2.2 Prozesszustände (Prozessdiagramm)

Das klassische Diagramm hat (je nach Vorlesung leicht andere Namen) diese Zustände:

```
                 +--------+
   Start ------> | Bereit |<---------------------+
                 +--------+                      |
                  |   ^                          |
     Scheduler    |   |  Verdrängung             |  Ereignis eingetreten
     wählt aus    |   |  (Zeitscheibe abgelaufen)|  (Daten da / Ressource frei)
                  v   |                          |
                 +--------+  Warten auf E/A     +-----------+
                 | Aktiv  |-------------------->| Blockiert |
                 | (läuft)|                     +-----------+
                 +--------+
                     |
                     v
                 +----------+
                 | Beendet  |
                 +----------+
```

| Zustand | Bedeutung |
|---|---|
| **Aktiv / Laufend (running)** | Prozess rechnet **gerade auf einem CPU-Kern** |
| **Bereit (ready)** | Prozess könnte sofort rechnen, wartet nur auf **freie CPU** |
| **Blockiert (blocked / waiting)** | Prozess wartet auf ein **Ereignis** (z. B. Daten von der Platte); kann **nicht** rechnen, auch wenn CPU frei wäre |
| Erzeugt / Beendet | Anfangs- und Endzustand |

**Die wichtigen Übergänge:**
- **Bereit → Aktiv:** Scheduler wählt den Prozess aus.
- **Aktiv → Bereit:** Prozess wird **verdrängt** (Zeitscheibe abgelaufen oder höher priorisierter Prozess).
- **Aktiv → Blockiert:** Prozess fordert eine Ressource an, die nicht sofort verfügbar ist (z. B. Datei lesen).
- **Blockiert → Bereit:** **Das OS** weckt den Prozess, wenn das Ereignis eingetreten ist (nicht der Prozess selbst!).
- **Blockiert → Aktiv gibt es NICHT direkt!** Erst muss der Prozess wieder Bereit werden und vom Scheduler ausgewählt werden.

## 2.3 Die Teilfragen aus Aufgabe 2a

### (1) 4 Rechenkerne – wie viele Prozesse gleichzeitig im Zustand "Aktiv"?
**Antwort: 4.** Jeder Kern führt zu einem Zeitpunkt genau einen Prozess aus, also sind **echt-gleichzeitig 4** Prozesse aktiv. (Annahme: ein Prozess pro Kern; Hyper-Threading etc. wird nicht betrachtet.)

### (2) Was ist Quasi-Parallelität?
Das OS **wechselt bzw. verdrängt die aktiven Prozesse in schneller Folge** (z. B. im Takt weniger Millisekunden, sog. **Zeitscheiben/Time Slices**). Dadurch entsteht für den Anwender der **Eindruck**, dass viel mehr Prozesse **gleichzeitig** laufen, als der Prozessor **tatsächlich** parallel bearbeiten könnte.
- **Echte Parallelität** = mehrere Kerne rechnen wirklich zeitgleich.
- **Quasi-Parallelität** = ein Kern wechselt so schnell zwischen Prozessen, dass es *wie* Parallelität wirkt.

### (3) Typischer Grund für den Wechsel in den Zustand Blockiert
Der Prozess hat (in der Regel per **Systemaufruf**) auf eine **Ressource außer der CPU** zugegriffen (Datenträger, Netzwerk, Tastatur …), und die **angeforderten Daten stehen noch nicht im Hauptspeicher** zur Verfügung. Damit der Prozess die **CPU nicht unnötig belegt (Busy Waiting)**, setzt das OS ihn auf **Blockiert** und nimmt ihn vom Kern. Der Kern kann so einem anderen Prozess dienen.

### (4) Warum können Prozesse nicht selbst aus Blockiert erwachen?
**Blockierte Prozesse sind nie auf der CPU aktiv.** Sie können also keinen Code ausführen und daher auch **nicht selbst prüfen**, ob die Ressource inzwischen bereit ist. Ein anderer muss sie aufwecken: **das OS** (typischerweise ausgelöst durch einen **Interrupt** der Hardware, z. B. "Platte hat Daten geliefert") setzt den Prozess wieder auf **Bereit**.

### (5) Was ist eine Heuristik zur Ablaufplanung (Scheduling)?
Ein **in der Praxis bewährtes, aber nicht beweisbar optimales Verfahren**, um zu entscheiden, **welcher Prozess auf die CPU darf** (z. B. unter Berücksichtigung früherer Rechenzeiten oder Prioritäten). Warum Heuristik? Das OS kennt die Zukunft nicht (z. B. wie lange ein Prozess rechnen wird), muss also mit Erfahrungswerten arbeiten.

## 2.4 Scheduling-Verfahren (Hintergrund, hilft beim Verständnis)

| Verfahren | Idee | Eigenschaft |
|---|---|---|
| **FCFS** (First Come First Served) | Wer zuerst kommt, rechnet bis er fertig ist | einfach, aber lange Prozesse blockieren kurze ("Konvoi-Effekt"); nicht verdrängend |
| **SJF** (Shortest Job First) | Kürzester Job zuerst | optimal für mittlere Wartezeit, aber Laufzeit ist vorher unbekannt; kann lange Jobs verhungern lassen |
| **Round Robin** | Jeder Prozess bekommt reihum eine Zeitscheibe | fair, verdrängend; Zeitscheibe muss sinnvoll gewählt werden |
| **Prioritäten-Scheduling** | Höchste Priorität zuerst | Gefahr von **Verhungern (Starvation)**; Abhilfe: *Aging* |
| **Multilevel Feedback Queue** | Mehrere Warteschlangen, Prozesse steigen je nach Verhalten auf/ab | in der Praxis verbreitet, klassische Heuristik |

- **Verdrängend (preemptive):** OS darf Prozess jederzeit von der CPU nehmen.
- **Nicht verdrängend (kooperativ/non-preemptive):** Prozess gibt CPU selbst ab oder ist fertig.

---

# Teil 3 – Synchronisation, Race Conditions, Deadlocks (Aufgabe 2b)

Das ist die "Story-Aufgabe" mit den Bürokräften Alice, Bob und Cheryl. Sie ist ein **Analogiebeispiel**: Statt Prozessen und Betriebsmitteln greifen Menschen auf Dateien zu. Übersetze das Szenario in OS-Begriffe:

| Szenario | OS-Begriff |
|---|---|
| Bürokraft | Prozess (oder Thread) |
| Dateien P, Q auf dem Server | gemeinsam genutzte **Ressourcen / Daten** |
| Herunterladen → Bearbeiten → Hochladen | **kritischer Abschnitt** (Lesen, Verändern, Schreiben) |
| "in Bearbeitung"-Markierung | **Mutex / Sperre (Lock)** |

## 3.1 Race Condition (Wettlaufsituation)

**Definition:** Das Ergebnis einer Berechnung hängt von der **zeitlichen Reihenfolge/Verzahnung** ab, in der mehrere Prozesse auf gemeinsame Daten zugreifen. Bei "Glück" ist das Ergebnis korrekt, bei "Pech" falsch – und das nicht reproduzierbar.

**Typisches Muster: "Lost Update"** (verlorene Änderung): Zwei Prozesse lesen den gleichen Stand, ändern ihn unabhängig und schreiben zurück. Die zweite Schreibaktion überschreibt die erste.

### Konkrete Abfolge für Vorgehen V1 (fehlerhaft):

| Zeit | Aktion | Serverstand von P |
|---|---|---|
| t1 | **A** lädt P herunter (Stand S₀) | S₀ |
| t2 | **B** lädt P herunter (Stand S₀) | S₀ |
| t3 | A bearbeitet, lädt P hoch | S₀ + Änderung A |
| t4 | B bearbeitet, lädt P hoch → **überschreibt** | S₀ + Änderung **B** (A's Änderungen **verloren**) |

**Zum Vergleich, "Glücksfall":** A lädt herunter, bearbeitet, lädt hoch, **erst danach** lädt B herunter, bearbeitet, lädt hoch → kein Fehler, alle Änderungen sind da.

**Fachwort: Race Condition.** (Zusatz: Der Bereich "herunterladen bis hochladen" ist der **kritische Abschnitt**, der **nicht atomar/geschützt** ist.)

## 3.2 Kritischer Abschnitt und wechselseitiger Ausschluss

- **Kritischer Abschnitt:** Codebereich (oder Vorgang), in dem auf gemeinsame Ressourcen zugegriffen wird und der **nicht von mehreren gleichzeitig** ausgeführt werden darf.
- **Wechselseitiger Ausschluss (Mutual Exclusion):** Es darf sich immer nur **ein** Prozess im kritischen Abschnitt befinden.

### Mutex / Sperre / Lock
- Ein **Mutex** (*mutual exclusion*) ist eine **Belegungsflagge**: frei oder belegt.
- Wer in den kritischen Abschnitt will, **sperrt** ihn (*lock*). Ist er schon gesperrt, muss er **warten**.
- Beim Verlassen wird **entsperrt** (*unlock*).
- Verwandt: **Semaphor** (Zähler, erlaubt bis zu n gleichzeitige Nutzer; Mutex = binärer Semaphor).

## 3.3 Vorgehen V2: Mutex löst die Race Condition

V2 = beim Herunterladen wird die Datei als **"in Bearbeitung" markiert** und ist für andere **gesperrt**, bis sie hochgeladen ist.

**Fachwort: Mutex** (wechselseitiger Ausschluss, Sperre). Der kritische Abschnitt ist hier "vom Herunterladen bis zum Hochladen".

**Löst V2 das Problem?** **Ja** (für das V1-Problem): B kann die Datei nicht mehr herunterladen, solange A sie bearbeitet. B bekommt erst den **fertigen Stand von A**, sodass **keine Änderungen verloren gehen**. Die Race Condition ist beseitigt.

> Die Aufgabe sagt ausdrücklich: *"Dieser Gesamtvorgang solle als Annahme immer irgendwann fertig sein."* Das heißt: die Bürokraft bleibt nicht ewig mit gesperrter Datei hängen. Diese Annahme brauchst du bei der Begründung (sonst wäre Blockade durch vergessene Freigabe denkbar).

## 3.4 Deadlock (Verklemmung)

**Definition:** Eine Menge von Prozessen ist im Deadlock, wenn **jeder auf ein Ereignis wartet, das nur ein anderer Prozess der Menge auslösen kann** (z. B. Freigabe einer Ressource) – und keiner kann weitermachen. Endlose Wartesituation.

### Die 4 notwendigen Bedingungen für einen Deadlock (Coffman-Bedingungen)
**Alle vier** müssen gleichzeitig gelten, damit ein Deadlock entstehen kann:

| # | Bedingung (Fachwort) | Bedeutung | Im Beispiel (V2 mit zwei Dateien) |
|---|---|---|---|
| 1 | **Wechselseitiger Ausschluss** (Mutual Exclusion) | Ressource kann nur von **einem** Prozess gleichzeitig benutzt werden | Datei ist "in Bearbeitung" = gesperrt (Mutex) |
| 2 | **Belegen und Warten / Zusatzbelegung** (Hold and Wait) | Ein Prozess hält bereits Ressourcen und fordert **zusätzliche** an | A hält P und will zusätzlich Q; B hält Q und will zusätzlich P |
| 3 | **Keine Verdrängung / keine externe Freigabe** (No Preemption) | Ressource kann dem Prozess **nicht gewaltsam entzogen** werden, nur der Besitzer gibt sie frei | Datei wird nur freigegeben, wenn der komplette Vorgang auf beiden Dateien abgeschlossen ist |
| 4 | **Zyklisches Warten** (Circular Wait) | Es gibt einen **Zyklus** in den Belegungs-/Wartewünschen | A wartet auf B (für Q), B wartet auf A (für P): P→Q und Q→P |

### Konkrete Abfolge (Klausurantwort)
1. **A** lädt **P** herunter → P ist gesperrt (A hält P).
2. **B** lädt **Q** herunter → Q ist gesperrt (B hält Q).
3. A merkt: Q muss auch geändert werden → A will Q herunterladen → **wartet** auf B.
4. B merkt: P muss auch geändert werden → B will P herunterladen → **wartet** auf A.
5. A gibt P erst nach Abschluss **beider** Dateien frei; B gibt Q erst nach Abschluss **beider** frei. **Keiner kommt weiter → Deadlock.**
6. **Cheryl (C)** merkt es ebenfalls: sie will P oder Q, findet beide gesperrt und wartet dauerhaft mit.

**Wie äußert sich das Problem?** Alle Beteiligten sehen den Hinweis "bitte warten, bis Bearbeitung abgeschlossen ist" – und dieser Hinweis verschwindet **nie**. Die Arbeit steht still.

**Wichtig für die Klausur:** Benenne das Fachwort **Deadlock** und nenne (kurz) die **vier Bedingungen** mit dem konkreten Bezug auf das Beispiel (wie in der Musterlösung).

## 3.5 Deadlock verhindern: Zyklus entfernen (letzte Teilfrage)

**Szenario:** Bearbeitung von **P** führt nie dazu, dass auch Q nötig ist. Bearbeitung von **Q** kann dazu führen, dass auch P nötig ist (Reihenfolge immer **erst Q, dann P**).

**Kann etwas schiefgehen? → Nein, kein Deadlock.**

Begründung:
- Es gibt **keinen Zyklus** mehr in den Belegungswünschen: Es gibt nur die Richtung **Q → P**, niemals **P → Q**. Die **4. Bedingung (zyklisches Warten) ist verletzt**. Da alle vier gleichzeitig nötig sind, kann kein Deadlock entstehen.
- Denkweise: Wer **P** hält, will nie mehr etwas anderes → er wird **immer irgendwann fertig** und gibt P frei (das ist die Annahme aus V2). Damit kann jeder, der auf P wartet (auch der Q-Halter), irgendwann P bekommen, fertig werden und Q freigeben. Also schließt die Bearbeitung von P immer irgendwann ab, **danach auch die von Q**.

### Verallgemeinerung: Ressourcen-Ordnung (Deadlock-Prävention)
Man nummeriert alle Ressourcen und verlangt, dass **jeder Prozess Ressourcen nur in aufsteigender Reihenfolge anfordert** (hier: erst Q, dann P). Dann kann kein Zyklus entstehen.

## 3.6 Deadlock-Strategien (Hintergrundwissen)

| Strategie | Idee |
|---|---|
| **Ignorieren** ("Vogel-Strauß-Algorithmus") | Deadlocks sind selten, Aufwand lohnt nicht (Unix/Windows machen das oft) |
| **Erkennen und beheben** (Detection & Recovery) | Zyklus im Ressourcen-Belegungsgraphen suchen, dann Prozess abbrechen oder Ressource entziehen |
| **Vermeiden** (Avoidance) | Vor jeder Vergabe prüfen, ob der Zustand "sicher" bleibt (**Bankier-Algorithmus**) |
| **Verhindern** (Prevention) | **Eine der 4 Bedingungen** dauerhaft unmöglich machen, z. B.:<br>• Alle Ressourcen **auf einmal** anfordern (bricht Hold-and-Wait)<br>• **Ressourcen-Ordnung** (bricht Circular Wait)<br>• **Entzug erlauben** (bricht No Preemption)<br>• Ressource **teilbar** machen (bricht Mutual Exclusion) |

**Verwandte Probleme (nicht verwechseln!):**
- **Starvation (Verhungern):** ein Prozess kommt dauerhaft nie an die Reihe, obwohl das System insgesamt weiterläuft (z. B. niedrige Priorität).
- **Livelock:** Prozesse sind aktiv, machen aber keinen Fortschritt (z. B. zwei Leute weichen sich auf dem Flur gegenseitig aus).

---

# Teil 4 – Speicherverwaltung (Aufgabe 3)

## 4.1 Warum virtueller Speicher?

- Hauptspeicher (RAM) ist **knapp**, Programme brauchen oft mehr, als physisch da ist.
- **Virtueller Speicher:** Jeder Prozess "sieht" einen eigenen, großen, zusammenhängenden **virtuellen Adressraum**. Das OS (mit Hilfe der Hardware, der **MMU**) bildet ihn auf den **physischen Speicher** ab. Nicht benötigte Teile liegen **ausgelagert auf der Festplatte** (Swap).
- Vorteile: Isolation der Prozesse, mehr Speicher als RAM, einfache Programmierung.

## 4.2 Paging: Seiten und Rahmen

| Begriff | Bedeutung |
|---|---|
| **Seite (Page)** | Fester Block im **virtuellen** Adressraum |
| **Rahmen / Seitenrahmen (Frame)** | Fester Block im **physischen** Hauptspeicher |
| **Seitengröße = Rahmengröße** | **Immer gleich groß**, damit jede Seite in **genau einen** Rahmen passt |
| **Seitentabelle (Page Table)** | Pro Prozess: ordnet jeder Seite einen Rahmen zu (+ Present-Bit u. a.) |
| **Present-Bit** (auch Valid/Resident) | 1 / *yes* = Seite ist **gerade im Hauptspeicher**; 0 / *no* = **ausgelagert** |
| **Seitenfehler (Page Fault)** | Zugriff auf eine Seite mit Present = no |

### Seitenfehler-Behandlung (Ablauf)
1. CPU greift auf virtuelle Adresse zu → MMU schaut in die Seitentabelle → Present-Bit = **no** → **Trap** an das OS.
2. OS sucht die Seite auf der Platte.
3. Ist ein **Rahmen frei**, wird die Seite dort hineingeladen. Sonst wird per **Ersetzungsalgorithmus** ein **Opfer** gewählt und ausgelagert (bei Änderung erst zurückschreiben).
4. Seitentabelle aktualisieren (Rahmennummer eintragen, Present = yes; beim Opfer Present = no).
5. Befehl wiederholen.
6. Solange die Platte lädt, ist der Prozess **Blockiert** (Verbindung zu Aufgabe 2a!) – Seitenfehler sind sehr teuer.

## 4.3 Adressen rechnen

### Formeln (das ist der Kern von Aufgabe 3b)

Gegeben: Adressbreite **n Bit**, Seitengröße **S Byte**, Rahmenanzahl **R**.

| Größe | Formel |
|---|---|
| Größe des virtuellen Adressraums | **2ⁿ** Byte (bei Byte-Adressierung) |
| Bits für das **Offset** | **log₂(S)** |
| Bits für die **Seitennummer** | **n − log₂(S)** |
| Anzahl virtueller Seiten | **2ⁿ / S** = 2^(Seitennummer-Bits) |
| Größe eines Rahmens | **= Seitengröße S** |
| Physischer Hauptspeicher | **R · S** |
| Virtuelle Adresse = | **[ Seitennummer | Offset ]** (höchste Bits = Seitennummer) |
| Physische Adresse = | **[ Rahmennummer | Offset ]** = Rahmennummer · S + Offset |

**Wichtig:** Das **Offset bleibt bei der Übersetzung unverändert.** Nur die Seitennummer wird durch die Rahmennummer ersetzt.

## 4.4 Aufgabe 3b komplett durchgerechnet

**Gegeben:** 8-Bit-Adressen (vorzeichenlos), 1 Byte pro Zelle, Seite = 32 Byte, 6 Rahmen.

### (a) Wie viele Bytes passen in einen Rahmen?
Rahmen = Seitengröße, damit jede Seite in **genau einen** Rahmen passt → **32 Byte**.

### (b) Wie viele Seiten gibt es im virtuellen Adressraum?
- Adressraum: 2⁸ = **256** Adressen (= 256 Byte)
- Seiten: 256 / 32 = **8 Seiten**

### (c) Wie groß ist der physische Hauptspeicher?
Rahmen decken den Hauptspeicher **vollständig** ab: 6 · 32 = **192 Byte**.

> Beachte: virtuell 256 Byte > physisch 192 Byte. Das ist genau der Sinn virtuellen Speichers: Der Adressraum darf größer sein als der RAM. Es können **nicht alle 8 Seiten gleichzeitig** im Speicher sein (nur 6).

### (d) Adresse `11010001` in Seitennummer und Offset zerlegen
1. Offset-Bits: 32 = 2⁵ → **5 Bit** Offset.
2. Seitennummer-Bits: 8 − 5 = **3 Bit** (passt: 8 Seiten = 2³, Werte 000 bis 111).
3. Aufteilen: `110` | `10001`
   - **Seitennummer** = `110`₂ = **6**
   - **Offset** = `10001`₂ = 16 + 1 = **17**
4. Kontrolle: 6 · 32 + 17 = 192 + 17 = **209** = `11010001`₂ ✓ (128+64+16+1 = 209)

→ Byte mit Index **17** auf der Seite mit Index **6** (insgesamt Byte **209** im virtuellen Adressraum).

### (e) Seitentabelle: physische Adresse zu `01001110`?

| Seitennummer | Rahmennummer | Present? |
|---|---|---|
| 000 | 010 | yes |
| 001 | 011 | yes |
| 010 | 000 | **no** |
| 011 | 000 | yes |
| 100 | 001 | yes |
| 101 | 000 | no |
| 110 | 101 | yes |
| 111 | 100 | yes |

1. Zerlegen: `010` | `01110` → Seitennummer **2**, Offset **14**.
2. Seitentabelle, Zeile `010`: **Present = no**.
3. **Es gibt keine physische Adresse.** Die Seite ist **nicht im Hauptspeicher**, sondern **ausgelagert auf der Festplatte**. Der Zugriff löst einen **Seitenfehler (Page Fault)** aus, das OS muss die Seite erst nachladen.

> Die Rahmennummer `000` in der Zeile `010` ist **bedeutungslos**, weil Present = no. Das ist die "Falle" der Aufgabe: nicht einfach Rahmen 000 einsetzen!

### Zusatzübung: Was wäre bei einer Adresse mit Present = yes?
Für `11010001` (Seite `110`): Zeile `110` → Rahmen `101` = 5, Present = yes.
Physische Adresse = Rahmennummer `101` + Offset `10001` = `10110001`₂ = 5 · 32 + 17 = **177**. (177 < 192 ✓, liegt im vorhandenen Hauptspeicher.)

**Merke:** Frames gibt es hier nur 0 bis 5. Die Rahmennummern `110` (6) und `111` (7) kommen in der Tabelle nicht vor, weil es sie physisch nicht gibt.

---

## 4.5 Seitenersetzung (Page Replacement) – Aufgabe 3a

### Das Problem
Ist ein Seitenfehler aufgetreten und **alle Rahmen sind belegt**, muss das OS entscheiden: **Welche Seite wird verdrängt (ausgelagert)?** Ziel: möglichst **wenige Seitenfehler** insgesamt.

**Eingabe:** eine **Referenzkette** = Folge von Seitennummern, auf die nacheinander zugegriffen wird.

### Die wichtigsten Verfahren

| Verfahren | Regel | Eigenschaften |
|---|---|---|
| **FIFO** (First In, First Out) | Verdränge die Seite, die **am längsten im Speicher** ist (älteste **Einlagerung**) | einfach; kann schlecht sein; **Belady-Anomalie** möglich |
| **LRU** (Least Recently Used) | Verdränge die Seite, deren **letzter Zugriff am längsten zurückliegt** | gut in der Praxis; aufwendig exakt umzusetzen |
| **Belady-Verdrängung / OPT / MIN** (optimal) | Verdränge die Seite, die **in Zukunft am längsten nicht mehr gebraucht wird** | **beweisbar minimale Seitenfehlerzahl**, aber **nicht realisierbar** (Zukunft unbekannt) → nur als **Vergleichsmaßstab** |
| **Second Chance / Clock** | FIFO + Referenzbit: Wurde die Seite zuletzt genutzt, bekommt sie eine "zweite Chance" | günstige Näherung an LRU |
| **NRU** | Verdränge nach Referenz-/Modifiziert-Bits (Klassen) | Näherung mit wenig Aufwand |

> **Achtung, Namensfalle:** "**Belady-Verdrängung**" (= optimaler Algorithmus) ist **nicht** dasselbe wie die "**Belady-Anomalie**" (FIFO kann mit *mehr* Rahmen *mehr* Seitenfehler machen). Beide stammen von László Bélády. In der Klausur ist mit Belady-Verdrängung der **optimale Algorithmus** gemeint (siehe Begründung der Musterlösung).

### So füllst du die Rahmenbelegungstabelle (FIFO) Schritt für Schritt

**Aufbau der Tabelle** (wie in der VL gefordert: mit Kopfzeile, Kopfspalte und Legende):
- **Kopfzeile:** die Referenzkette (jede Spalte = ein Zugriff).
- **Kopfspalte:** Rahmennummern 0 bis (Rahmenzahl − 1).
- **Legende:** z. B. "Zahl = Seitennummer im Rahmen, **unterstrichen = Seitenfehler (neu eingelagert)**, leer = Rahmen noch unbenutzt".

**Vorgehen pro Zugriff:**
1. Ist die Seite **schon in einem Rahmen**? → **Treffer (Hit)**, Tabelle einfach übernehmen, **nichts unterstreichen**.
2. Sonst → **Seitenfehler**:
   - Ist ein **Rahmen frei**? → nimm den **niedrigsten freien Rahmen** (0, 1, 2, …).
   - Sonst: **FIFO → älteste eingelagerte Seite verdrängen**, die neue Seite in *deren Rahmen* schreiben. **Neue Seite unterstreichen.**
3. **Wichtig bei FIFO:** Ein **Treffer ändert die Reihenfolge NICHT.** (Bei LRU dagegen schon!)

**Tipp:** Führe daneben eine Hilfsliste "Einlagerungsreihenfolge (ältester zuerst)", z. B. `[Rahmen1, Rahmen2, Rahmen3, Rahmen0]`. Der vorderste Eintrag ist der nächste Kandidat zum Verdrängen.

### Die Klausur-Aufgabe gerechnet

**4 Rahmen, Referenzkette:** `5, 2, 4, 1, 0, 1, 2, 5, 2, 4, 1, 0`

| Zugriff | Ergebnis | Rahmen 0 | Rahmen 1 | Rahmen 2 | Rahmen 3 | Verdrängt |
|---|---|---|---|---|---|---|
| 5 | **Fehler** (Rahmen frei) | **5** | – | – | – | – |
| 2 | **Fehler** | 5 | **2** | – | – | – |
| 4 | **Fehler** | 5 | 2 | **4** | – | – |
| 1 | **Fehler** | 5 | 2 | 4 | **1** | – |
| 0 | **Fehler** (älteste: 5) | **0** | 2 | 4 | 1 | 5 |
| 1 | Treffer | 0 | 2 | 4 | 1 | – |
| 2 | Treffer | 0 | 2 | 4 | 1 | – |
| 5 | **Fehler** (älteste: 2) | 0 | **5** | 4 | 1 | 2 |
| 2 | **Fehler** (älteste: 4) | 0 | 5 | **2** | 1 | 4 |
| 4 | **Fehler** (älteste: 1) | 0 | 5 | 2 | **4** | 1 |
| 1 | **Fehler** (älteste: 0) | **1** | 5 | 2 | 4 | 0 |
| 0 | **Fehler** (älteste: 5) | 1 | **0** | 2 | 4 | 5 |

**Seitenfehler gesamt: 10** (Zugriffe 1–5 und 8–12; nur die Zugriffe 6 und 7 sind Treffer).

**Die Tabelle im Klausurformat** (fett = in der Klausur unterstreichen):

| | **5** | **2** | **4** | **1** | **0** | **1** | **2** | **5** | **2** | **4** | **1** | **0** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Rahmen 0** | **5** | 5 | 5 | 5 | **0** | 0 | 0 | 0 | 0 | 0 | **1** | 1 |
| **Rahmen 1** | | **2** | 2 | 2 | 2 | 2 | 2 | **5** | 5 | 5 | 5 | **0** |
| **Rahmen 2** | | | **4** | 4 | 4 | 4 | 4 | 4 | **2** | 2 | 2 | 2 |
| **Rahmen 3** | | | | **1** | 1 | 1 | 1 | 1 | 1 | **4** | 4 | 4 |

Legende: Zahl = Seitennummer im Rahmen · **fett/unterstrichen = Seitenfehler (neu eingelagert)** · leer = Rahmen noch frei.

> **Punktabzug-Hinweis der Klausur:** Zellen nicht mehr befüllen, die noch nie belegt waren (z. B. Rahmen 1 in Spalte 1). Leere Zellen bleiben leer!

### Vergleich: Wie schneiden LRU und OPT bei derselben Kette ab?
(Zum Üben und Verstehen; **nicht** verlangt.)

- **FIFO: 10** Seitenfehler
- **LRU: 8** Seitenfehler
- **OPT (Belady): 6** Seitenfehler – die absolute Untergrenze bei dieser Kette

OPT-Tabelle zur Kontrolle (bei Gleichstand beliebige Seite wählbar):

| | **5** | **2** | **4** | **1** | **0** | **1** | **2** | **5** | **2** | **4** | **1** | **0** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Rahmen 0** | **5** | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | **4** | 4 | 4 |
| **Rahmen 1** | | **2** | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| **Rahmen 2** | | | **4** | 4 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Rahmen 3** | | | | **1** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Beim Zugriff auf `0` wird `4` verdrängt (nächster Gebrauch am weitesten weg, ab Zugriff 10). Beim zweiten Zugriff auf `4` wird `5` oder `2` verdrängt, weil beide nie mehr vorkommen.

### Belady-Anomalie (Extra-Wissen, klassisches Beispiel)
Referenzkette `1,2,3,4,1,2,5,1,2,3,4,5` mit FIFO:
- **3 Rahmen → 9 Seitenfehler**
- **4 Rahmen → 10 Seitenfehler** (mehr Speicher, mehr Fehler!)

Das kann bei FIFO passieren, bei LRU und OPT nicht (sog. Stack-Algorithmen).

## 4.6 Die Begründungsfrage: "Kommilitone erhält mit Belady-Verdrängung 11 Seitenfehler – vertan?"

**Antwort: Ja, er hat sich vertan.**

Begründung:
1. Die **Belady-Verdrängung (OPT)** erzeugt **die minimal mögliche Anzahl** an Seitenfehlern. Kein korrekter Algorithmus kann für dieselbe Referenzkette und dieselbe Rahmenzahl **weniger** Fehler erzeugen.
2. Unser **korrekt durchgeführtes FIFO hat 10** Seitenfehler.
3. Belady muss also **höchstens 10** haben (immer ≤ jedes andere Verfahren). **11 ist mehr als FIFO, das kann nicht sein.** Also Rechenfehler.

> **Achtung, Formulierung in der Musterlösung:** Dort steht sinngemäß, FIFO habe Belady "unterboten". Logisch richtig ist: Belady darf **nie schlechter** (mehr Fehler) sein als ein anderes Verfahren. Formuliere in der Klausur lieber: "*Belady ist optimal, also ≤ 10. 11 > 10 → Widerspruch.*" (Tatsächlich ergibt OPT hier 6.)

---

# Teil 5 – Kommentierte Musterlösungen im Klausurstil

So kurz und präzise erwartet die Klausur die Antworten (je 1 Punkt = 1 präziser Gedanke).

### Aufgabe 1 (5 P)
| Frage | Kernaussagen |
|---|---|
| Zwei Aufgaben + Beispiel (2 P) | **Ressourcenverwaltung** (zeitlich/räumlich; Bsp. Datei auf Platte, Zugriffsrechte/-zeitpunkt) · **Hardware-Abstraktion** (virtuelle Maschine über Systemaufrufe; Bsp. `open()` unabhängig vom Datenträger) |
| Mikrokernel (1 P) | Kernel nur noch **Nachrichtenübermittlung + Prozessverwaltung**, Rest (z. B. Dateisystem) als **Anwendungsprozesse/Server** |
| Mehrbenutzerbetrieb (1 P) | mehrere **angemeldete Benutzer gleichzeitig**, jeder mit eigenen Prozessen |
| Kanonisch und relativ? (1 P) | **Ja**: `testordner/test.txt` – keine `.`/`..` (kanonisch), beginnt nicht an der Wurzel (relativ) |

### Aufgabe 2a (5 P)
| Frage | Kernaussagen |
|---|---|
| Aktive Prozesse bei 4 Kernen | **4** (pro Kern einer, echt-gleichzeitig) |
| Quasi-Parallelität | **schneller Wechsel/Verdrängen** der Prozesse (Millisekunden) → **scheinbare Gleichzeitigkeit** |
| Grund für Blockiert | Zugriff auf **Nicht-CPU-Ressource** (Platte, Netz), **Daten noch nicht im Hauptspeicher** → CPU nicht unnötig belegen |
| Warum nicht selbst aufwachen | Blockierte Prozesse laufen **nie auf der CPU**, können also nichts prüfen → **OS** muss sie wecken |
| Heuristik | **bewährtes, aber nicht beweisbar optimales** Verfahren zur Wahl des nächsten Prozesses |

### Aufgabe 2b (5 P)
| Frage | Kernaussagen |
|---|---|
| Was geht bei V1 schief? (2 P) | Konkrete Abfolge: A lädt, B lädt, A lädt hoch, B lädt hoch → **A's Änderungen überschrieben**. Fachwort **Race Condition** (Lost Update); bei "günstiger" Reihenfolge kein Fehler |
| V2 – Fachwort + löst es? (1 P) | **Mutex** (wechselseitiger Ausschluss, Belegungsflagge). **Ja**, denn B kann erst laden, wenn A den finalen Stand hochgeladen hat |
| Zwei Dateien: was geht schief? (1 P) | **Deadlock**. Ablauf: A hält P, B hält Q, A will Q, B will P → endloses Warten. Die **4 Bedingungen** benennen (Mutex, Zusatzbelegung, keine Verdrängung, Zyklus) |
| Nur Q→P, nie P→Q (1 P) | **Nein, kein Deadlock**: **kein Zyklus** in den Belegungswünschen → 4. Bedingung verletzt; P-Bearbeitung endet immer, dann auch Q |

### Aufgabe 3a (5 P)
| Frage | Kernaussagen |
|---|---|
| FIFO-Tabelle (4 P) | Tabelle mit Kopfzeile (Referenzkette), Kopfspalte (Rahmen 0–3), Legende; **10 Seitenfehler** unterstrichen; keine überzähligen Einträge |
| Belady-Frage (1 P) | Belady = **Optimum**, ≤ FIFO = 10. **11 unmöglich** → Kommilitone hat sich vertan |

### Aufgabe 3b (5 P)
| Frage | Ergebnis |
|---|---|
| Bytes pro Rahmen | **32** (Rahmen = Seitengröße) |
| Seiten im virtuellen Adressraum | 2⁸ / 32 = **8** |
| Physischer Hauptspeicher | 6 · 32 = **192 Byte** |
| `11010001` zerlegen | 3 Bit Seite, 5 Bit Offset → **Seite 6 (`110`), Offset 17 (`10001`)**; Byte 209 |
| `01001110` physische Adresse | **Keine**, Seite `010` hat Present = **no** → ausgelagert (Seitenfehler) |

---

# Teil 6 – Übungsaufgaben (mit Lösungen)

## Übung 1 – FIFO mit 3 Rahmen
Referenzkette: `7, 0, 1, 2, 0, 3, 0, 4, 2, 3` – FIFO, **3 Rahmen**. Wie viele Seitenfehler?

<details><summary>Lösung</summary>

| Zugriff | Ergebnis | R0 | R1 | R2 | Verdrängt |
|---|---|---|---|---|---|
| 7 | Fehler | 7 | | | |
| 0 | Fehler | 7 | 0 | | |
| 1 | Fehler | 7 | 0 | 1 | |
| 2 | Fehler | 2 | 0 | 1 | 7 |
| 0 | Treffer | 2 | 0 | 1 | |
| 3 | Fehler | 2 | 3 | 1 | 0 |
| 0 | Fehler | 2 | 3 | 0 | 1 |
| 4 | Fehler | 4 | 3 | 0 | 2 |
| 2 | Fehler | 4 | 2 | 0 | 3 |
| 3 | Fehler | 4 | 2 | 3 | 0 |

**9 Seitenfehler** (nur der 5. Zugriff ist ein Treffer).
</details>

## Übung 2 – Adressen
System: **10-Bit-Adressen**, Seitengröße **64 Byte**, **12 Rahmen**.
a) Wie viele Bits für das Offset? b) Wie viele virtuelle Seiten? c) Größe des Hauptspeichers? d) Zerlege `1011001101`.

<details><summary>Lösung</summary>

a) 64 = 2⁶ → **6 Bit** Offset.
b) Seitennummer-Bits: 10 − 6 = 4 → 2⁴ = **16 Seiten** (Kontrolle: 1024 / 64 = 16).
c) 12 · 64 = **768 Byte**.
d) `1011` | `001101` → Seitennummer `1011` = **11**, Offset `001101` = **13**. (Kontrolle: 11·64 + 13 = 717.)
</details>

## Übung 3 – Physische Adresse
System aus Aufgabe 3b (8 Bit, Seite 32 Byte). Seitentabelle wie in der Klausur. Berechne die physische Adresse zu `10001010`, `11100011` und `10100000`.

<details><summary>Lösung</summary>

- `10001010` → Seite `100`, Offset `01010` (10). Tabelle: `100` → Rahmen `001`, yes → physisch `001` `01010` = `00101010`₂ = 1·32 + 10 = **42**.
- `11100011` → Seite `111`, Offset `00011` (3). Tabelle: `111` → Rahmen `100` (4), yes → `100` `00011` = `10000011`₂ = 4·32 + 3 = **131**.
- `10100000` → Seite `101`, Offset 0. Tabelle: `101` → Present = **no** → **keine physische Adresse**, Seitenfehler.
</details>

## Übung 4 – Deadlock erkennen
Prozess X hält Drucker D und fordert Scanner S. Prozess Y hält Scanner S und fordert Drucker D. Beide geben nur nach Abschluss der gesamten Aufgabe frei. Deadlock? Welche Bedingungen sind erfüllt? Wie verhindert man ihn?

<details><summary>Lösung</summary>

**Ja, Deadlock.** Alle vier Bedingungen: (1) D und S sind exklusiv nutzbar (Mutual Exclusion), (2) beide halten eine Ressource und fordern eine weitere an (Hold and Wait), (3) Freigabe nur durch den Besitzer, kein Entzug (No Preemption), (4) X wartet auf Y, Y wartet auf X (Zyklus).
**Verhindern:** z. B. **Ressourcen-Ordnung** (immer erst D, dann S), oder beide Ressourcen **gleichzeitig** anfordern, oder **Entzug/Timeout** erlauben.
</details>

## Übung 5 – Begriffe erkennen
Ordne zu: (a) Zwei Threads erhöhen gleichzeitig denselben Zähler, das Ergebnis ist falsch. (b) Ein Prozess mit niedriger Priorität kommt nie an die CPU. (c) Zwei Prozesse warten zyklisch aufeinander. (d) Ein Prozess wartet auf Plattendaten und belegt die CPU nicht.

<details><summary>Lösung</summary>

(a) **Race Condition** (b) **Starvation / Verhungern** (c) **Deadlock** (d) Zustand **Blockiert**.
</details>

---

# Teil 7 – Spickzettel (zum Auswendiglernen)

### Die wichtigsten Definitionen in einem Satz
- **OS-Aufgaben:** Ressourcenverwaltung (zeitlich + räumlich) und Hardware-Abstraktion (virtuelle Maschine über Systemaufrufe).
- **Mikrokernel:** Kernel = nur Prozessverwaltung + Nachrichtenaustausch, alles andere (z. B. Dateisystem) läuft als Prozess.
- **Mehrbenutzerbetrieb:** mehrere angemeldete Benutzer gleichzeitig.
- **Kanonisch:** ohne `.`/`..` · **Relativ:** beginnt nicht an der Wurzel (beides kombinierbar).
- **Aktiv/Bereit/Blockiert:** rechnet · wartet auf CPU · wartet auf Ereignis.
- **Quasi-Parallelität:** schneller Wechsel → scheinbare Gleichzeitigkeit.
- **Blockiert → Bereit:** durch das **OS**, nie durch den Prozess selbst.
- **Heuristik:** bewährt, nicht beweisbar optimal.
- **Race Condition:** Ergebnis hängt von der Reihenfolge der Zugriffe ab.
- **Mutex:** Belegungsflagge, wechselseitiger Ausschluss.
- **Deadlock-Bedingungen (alle 4 nötig):** Mutual Exclusion · Hold and Wait (Zusatzbelegung) · No Preemption (keine externe Freigabe) · Circular Wait (Zyklus).
- **Kein Zyklus → kein Deadlock.**
- **Seite/Rahmen:** gleich groß; Seite virtuell, Rahmen physisch.
- **Present-Bit = no:** Seite ausgelagert → Seitenfehler, keine physische Adresse.
- **FIFO:** älteste Einlagerung raus; Treffer ändern nichts.
- **LRU:** am längsten ungenutzt raus.
- **Belady/OPT:** am spätesten wieder benötigt raus; **minimale** Fehlerzahl; nicht praktisch umsetzbar.
- **Belady-Anomalie:** bei FIFO kann mehr Speicher mehr Seitenfehler bringen.

### Rechen-Spickzettel (Paging)
```
Offset-Bits          = log2(Seitengröße)
Seitennummer-Bits    = Adressbits − Offset-Bits
Anzahl Seiten        = 2^(Seitennummer-Bits) = 2^Adressbits / Seitengröße
Rahmengröße          = Seitengröße
Hauptspeichergröße   = Rahmenanzahl · Seitengröße
Virtuelle Adresse    = [ Seitennummer | Offset ]
Physische Adresse    = [ Rahmennummer | Offset ]   (Offset bleibt gleich!)
Present = no         → keine physische Adresse, Seitenfehler
```

### Potenzen von 2 (Kopfrechnen!)
`2⁰=1 · 2¹=2 · 2²=4 · 2³=8 · 2⁴=16 · 2⁵=32 · 2⁶=64 · 2⁷=128 · 2⁸=256 · 2⁹=512 · 2¹⁰=1024`

### Bitmuster lesen (8 Bit)
Stellenwerte: `128 · 64 · 32 · 16 · 8 · 4 · 2 · 1`
Beispiel `11010001` = 128 + 64 + 16 + 1 = **209**

---

# Teil 8 – Lernplan für "quasi alles lernen"

| Schritt | Was | Zeit (Richtwert) |
|---|---|---|
| 1 | **Teil 4 durcharbeiten**: Formeln verstehen, 3b selbst nachrechnen, FIFO-Tabelle ohne Hilfe wiederholen (Übung 1–3) | 2–3 h |
| 2 | **Teil 3 lesen**: Race Condition → Mutex → Deadlock → 4 Bedingungen. Konkretes A/B/P/Q-Beispiel **mündlich** erklären können | 1–2 h |
| 3 | **Teil 2**: Prozessdiagramm zeichnen können, die 5 Kurzfragen aus 2a antworten können | 1 h |
| 4 | **Teil 1**: Definitionen auswendig, Pfad-Tabelle verstehen | 30–45 min |
| 5 | **Übungen 4–5 + Spickzettel**, dann die Probeklausur **ohne Hilfe** als Simulation | 1–2 h |
| 6 | Mit dem **Vorlesungsskript abgleichen**: Begriffe, Zustandsnamen, Legende der Rahmentabelle | 30 min |

**Klausurtipps:**
- Bei Erklär-Fragen: **Fachwort nennen + kurze Begründung + konkretes Beispiel** (Story-Aufgaben: konkrete Abfolge mit Namen A, B, P, Q hinschreiben!).
- Bei Rechenaufgaben: **Rechenweg mitschreiben**, auch wenn das Ergebnis trivial wirkt (Punkte gibt es für Begründung).
- **Nur mit Kugelschreiber/Füller** schreiben; nichts überflüssig in die Tabelle eintragen (Punktabzug bei überzähligen Einträgen).
- Tabelle 3a: **Kopfzeile, Kopfspalte und Legende nicht vergessen** (sonst gehen Punkte verloren).
- Auf **Formulierungen wie "Begründen Sie" achten**: Ohne Begründung gibt es keinen Punkt.