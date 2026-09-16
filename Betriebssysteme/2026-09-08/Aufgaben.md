![](../2026-09-08/Betriebssysteme%20-%203%20-%20ÜB%20-%20Speicherverwaltung.pdf)

## By Claude

# Betriebssysteme – 3: Speicherverwaltung
### Zusammenfassung der Vorlesung + Lösungen zur Übung (mit Bewertung deiner Antworten)

---

## Teil A – Die Themen der Vorlesung erklärt

### 1. Speicherarchitektur

Computerspeicher ist **hierarchisch** aufgebaut: Je näher ein Speicher am Rechenwerk liegt, desto schneller, teurer und kleiner ist er; je weiter entfernt, desto langsamer, günstiger und größer.

| Speicherart | Ort | Größe (ca.) | Zugriffszeit (ca.) | Flüchtig? |
|---|---|---|---|---|
| Register | CPU-Die | 100–1000 Byte/Kern | quasi sofort | ja |
| Cache (L1–L3) | CPU-Die | 1 kB – 100 MB | 1–5 ns | ja |
| Hauptspeicher (RAM) | über Systembus | 4–256 GB | 5–20 ns | ja |
| Datenträger (SSD/HDD) | über Systembus, indirekt | 100 GB – 20 TB | 5–10 ms | nein |

**Speichermodell:** Der Hauptspeicher wird als lückenlose Folge von Speicherzellen (je 1 Byte) gedacht, durchnummeriert ab 0. Diese Nummer ist die **Adresse**. Wert und Adresse sind zwei verschiedene Dinge (vgl. Kontonummer vs. Kontostand).

- **Adressierbarer Hauptspeicher:** die Menge an Speicherzellen, die mit der gegebenen Adressbreite überhaupt angesprochen werden *könnte* (b Bit Adresse → 2^b Byte adressierbar).
- **Physisch verfügbarer Hauptspeicher:** die tatsächlich verbaute Menge – kann kleiner sein als das theoretische Maximum.
- Adresse 0 wird konventionell nicht belegt (dient als `null`-Marker).
- **Zeigervariable:** eine Variable, die sich die Adresse einer anderen Variable merkt.

---

### 2. Die vier Probleme der Speicherverwaltung

Wenn man Prozessen einfach Speicher „am Stück“ (Partitionen) zuteilt, entstehen vier grundsätzliche Probleme:

1. **Speicherfragmentierung**
   - *Interner Verschnitt:* Der einem Prozess zugeteilte Speicher wird vom Prozess nicht vollständig genutzt (Verschwendung *innerhalb* einer Partition).
   - *Externer Verschnitt:* Über die Zeit entstehen viele kleine, ungenutzte Lücken *zwischen* Partitionen, die in Summe zwar genug Platz böten, aber nicht am Stück verfügbar sind.

2. **Speicherzusatzbelegung** – Prozesse wissen oft nicht im Voraus, wie viel Speicher sie brauchen werden (z. B. wachsende Datenstrukturen). Eine feste Partition kann nicht ohne Weiteres wachsen.

3. **Speicherschutz** – Ohne Kontrolle könnten Prozesse fremde Speicherbereiche lesen/schreiben (versehentlich oder böswillig).

4. **Relokation** – Verweise (Adressen) in einem Programm werden ungültig, sobald die Partition im Speicher verschoben wird (z. B. beim Laden, bei Kompaktierung).

---

### 3. Virtueller Speicher

**Idee:** Jeder Prozess bekommt einen eigenen, in sich geschlossenen **virtuellen Adressraum**. Eine **Adressabbildung** (Seitentabelle) übersetzt virtuelle in physische Adressen.

- Der virtuelle Adressraum wird in **Seiten (Pages)** fester Größe zerlegt, der physische Hauptspeicher in **Rahmen (Frames)** gleicher Größe.
- Eine virtuelle Adresse zerfällt in **Seitennummer** (vordere Bits) + **Seitenoffset** (hintere Bits). Beim Zugriff wird nur die Seitennummer durch die aktuell zugeordnete Rahmennummer ersetzt, der Offset bleibt unverändert.
- **Seiten- und Rahmennummern müssen dieselbe Bitbreite besitzen.**
- Die **Seitentabelle** enthält pro Seite mindestens: Rahmennummer + Present-Bit (ist die Seite gerade eingelagert oder auf dem Datenträger ausgelagert?). Erweiterte Tabellen führen zusätzlich Reference-Bit, Modify-Bit, Schutzmodus etc.
- Warum löst virtueller Speicher die vier Probleme?
  - **Fragmentierung:** i. d. R. **vollständig gelöst** (extern), da jede Seite in jeden beliebigen freien Rahmen passt – es gibt keine „krummen“ Lücken mehr. Interner Verschnitt bleibt minimal bestehen (die letzte, evtl. nur teilweise genutzte Seite eines Prozesses).
  - **Zusatzbelegung:** **entschärft** – neue Seiten können jederzeit einem freien Rahmen zugeordnet werden, ohne dass Speicher am Stück vorhanden sein muss.
  - **Speicherschutz:** **gelöst** – jeder Prozess sieht nur seinen eigenen virtuellen Adressraum und kann technisch gar keine fremde physische Adresse referenzieren.
  - **Relokation:** **gelöst** – die virtuelle Adresse eines Prozesses bleibt stets gleich, nur die Abbildung auf den physischen Rahmen wird bei Bedarf angepasst.

---

### 4. Behandlung von Seitenfehlern

Ein **Seitenfehler** tritt auf, wenn auf eine virtuelle Seite zugegriffen wird, der kein Rahmen zugeordnet ist (z. B. weil sie ausgelagert ist). Das Betriebssystem behandelt dies in ca. 10 Schritten (Trap auslösen, Register sichern, Seite bestimmen, Rechte prüfen, ggf. eine andere Seite verdrängen, Seite vom Datenträger laden, Seitentabelle aktualisieren, Ausführung fortsetzen).

**Verdrängungsstrategien** (welche Seite fliegt raus, wenn alle Rahmen belegt sind?):

- **FIFO:** Verdränge die am längsten im Speicher befindliche Seite. Einfach, aber schlecht – auch häufig genutzte Seiten fliegen irgendwann raus. Zeigt zudem **Beladys Anomalie**: mehr Rahmen können bei FIFO paradoxerweise zu *mehr* Seitenfehlern führen.
- **Belady/Optimal (1966):** Verdränge die Seite, die am längsten in der Zukunft nicht mehr gebraucht wird. Theoretisch optimal (minimale Anzahl Seitenfehler), aber in der Praxis nicht umsetzbar, da die Zukunft unbekannt ist.
- **Aging-Algorithmus:** heuristische Annäherung an LRU – pro Seite wird regelmäßig ein Zugriffsbit in ein Schieberegister eingetragen, sodass sowohl Häufigkeit als auch Aktualität der Zugriffe abgebildet werden.

---

## Teil B – Lösungen zur Übung

## Aufgabe 1: Grundkonzepte

### a) Parkplatz-Analogie

**Was hat das mit Speicherverwaltung zu tun?**
Die Autos stehen unregelmäßig verteilt, sodass zwischen ihnen viele kleine, einzeln nutzlose Lücken entstehen. In Summe wäre genug Platz für ein weiteres Auto da – aber nicht am Stück. Das ist die Parkplatz-Analogie zur **Speicherfragmentierung**.

**Interner vs. externer Verschnitt:** Die Lücken *zwischen* den Autos entsprechen **externem Verschnitt** – Speicher, der zwischen belegten „Partitionen“ übrig, aber nicht am Stück nutzbar ist. Interner Verschnitt würde erst auftreten, wenn es feste Parkfelder gäbe, die größer als das jeweilige Auto sind (Platzverschwendung *innerhalb* einer Partition).

**Bewertung der Lösungsvorschläge:**

| Vorschlag | Löst das Problem allgemein? | Begründung |
|---|---|---|
| Regelmäßig zufällig umparken | Nein | Reine Zufallsumverteilung garantiert keine kompakte Anordnung – die Fragmentierung kann genauso gut wieder entstehen. Kein systematischer Fix. |
| Nur Parkplatzmarkierungen | Nein / nur teilweise | Markierungen sind lediglich eine Richtlinie ohne Durchsetzung; Fahrer können trotzdem „falsch“ parken, das Grundproblem bleibt bestehen. |
| Markierungen **+ konsequentes Abschleppen** | **Ja, im Allgemeinen** | Das erzwingt eine feste Rasterung des Speichers – exakt das Prinzip von **Seiten fester Größe**. Damit passt jedes Auto (jede Seite) exakt in ein Feld (einen Rahmen); externer Verschnitt wird strukturell verhindert. (Als Kompromiss kann dabei interner Verschnitt entstehen, wenn ein Auto kleiner als sein Feld ist.) |
| Alle Autos kleiner wählen | Nein, nur situativ | Reduziert höchstens die Auswirkung im konkreten Beispiel, verhindert aber nicht grundsätzlich, dass durch ungleichmäßiges Parken Lücken entstehen. |
| Schlüssel für alle Autos (jederzeit umparken) | **Ja, im Allgemeinen, aber teuer** | Das entspricht **Kompaktierung**: Man kann jederzeit alle „Partitionen“ verschieben, um Lücken zu beseitigen. Das löst das Problem grundsätzlich, ist aber aufwendig/störend (Autos/Prozesse müssten dafür ggf. „angehalten“ werden). |

**Fazit:** Am praxisnächsten und allgemeinsten ist die Kombination aus **Markierung + Durchsetzung** (= feste Seitengröße/Paging). Die „Schlüssel“-Lösung ist die theoretisch ebenso vollständige, aber kostenintensive Variante (= Kompaktierung).

### b) Transferrate vs. Latenz

- **Latenz** ist die Wartezeit, bis ein Datentransfer überhaupt beginnt (z. B. Zugriffs-/Suchzeit).
- **Transferrate** ist die Geschwindigkeit, mit der Daten übertragen werden, *sobald* der Transfer läuft (Durchsatz, z. B. MB/s bzw. GB/s).

Typische Werte (laut VL, Stand ca. 2020):
- Hauptspeicher: Zugriffszeit ca. 5–20 ns
- Datenträger (SSD/HDD): Zugriffszeit ca. 5–10 ms – also ca. eine **Million Mal langsamer** in der Latenz als RAM.

**Erkenntnis für die Seitengröße:** Da beim Auslagern auf einen Datenträger die Latenz (der feste „Rüstaufwand“ pro Zugriff) im Vergleich zur eigentlichen Transferzeit riesig ist, lohnt es sich, **möglichst große Seiten** pro Zugriff zu übertragen. So verteilt sich die hohe, feste Latenz auf mehr transportierte Bytes, und man vermeidet viele kleine, latenzdominierte Einzelzugriffe. Deshalb sind Seiten für die Auslagerung typischerweise recht groß (mehrere KB, z. B. 4–16 KB), nicht nur wenige Byte.

### c) Cache-Vorteil beim Prüfen eines int-Arrays auf Primzahlen

**Deine Antwort:** *„In einem Array werden nebenliegende Einträge direkt in den Cache geladen, was die Zugriffszeiten massiv verringert.“*

**Bewertung: Im Kern richtig! 👍** Präzisiert:
Ein Array liegt im Speicher **zusammenhängend** (sequenziell). Wenn die CPU auf ein Element zugreift, lädt der Cache automatisch eine ganze **Cache-Zeile** (mehrere zusammenhängende Bytes, z. B. 64 Byte) auf einmal aus dem Hauptspeicher. Da man beim Durchlaufen des Arrays die Elemente der Reihe nach liest, befinden sich die nächsten paar Werte durch diesen Effekt (**räumliche Lokalität**) meist schon im schnellen Cache, bevor man überhaupt explizit darauf zugreift. Man spart sich also viele einzelne, langsame Hauptspeicherzugriffe (ns statt evtl. ms bei Auslagerung).

---

## Aufgabe 2: Virtueller Speicher

### a) Relokationsproblem am Beispiel `robot r = new robot();` bzw. `robot *r = new robot();`

`new robot()` legt das eigentliche `robot`-Objekt irgendwo im (virtuellen) Speicher ab; `r` ist eine **Zeiger-/Referenzvariable**, die sich lediglich die **Adresse** dieses Objekts merkt. Das Relokationsproblem entsteht, sobald sich die physische (bzw. auch virtuelle) Lage des Objekts ändert – etwa durch Kompaktierung, Garbage Collection, oder weil der Prozess neu geladen/verschoben wird: Die in `r` gespeicherte Adresse zeigt dann plötzlich ins Leere oder auf falsche Daten, weil sie nicht automatisch mit aktualisiert wird. Genau dieses „Verweise brechen beim Verschieben“ ist das Relokationsproblem.

### b) Wie geht virtueller Speicher die vier Probleme an?

| Problem | Wirkung durch virtuellen Speicher | Grad |
|---|---|---|
| Fragmentierung | Jede Seite passt in jeden freien Rahmen gleicher Größe → keine „krummen“ Lücken mehr möglich | **vollständig gelöst** (extern); minimaler interner Verschnitt bleibt (letzte, teilgenutzte Seite) |
| Zusatzbelegung | Neue Seiten können bei Bedarf jedem freien Rahmen zugeordnet werden, ohne zusammenhängenden Speicher zu benötigen | **entschärft** |
| Speicherschutz | Jeder Prozess hat einen eigenen, isolierten virtuellen Adressraum; er kann technisch gar keine physische Adresse eines anderen Prozesses referenzieren | **gelöst** |
| Relokation | Die virtuelle Adresse eines Prozesses bleibt konstant; nur die Abbildung auf den physischen Rahmen wird bei Verschiebung in der Seitentabelle angepasst | **gelöst** |

### c) Warum können Threads Daten teilen, Prozesse aber nicht?

Threads gehören zum selben Prozess und teilen sich damit **dieselbe Seitentabelle / denselben virtuellen Adressraum**. Wenn zwei Threads dieselbe virtuelle Adresse verwenden, zeigt diese also auf denselben physischen Rahmen – sie sehen automatisch dieselben Daten.

Prozesse hingegen haben **jeweils eigene, unabhängige Adressabbildungen**. Dieselbe virtuelle Adresse in zwei verschiedenen Prozessen zeigt in der Regel auf **unterschiedliche** physische Rahmen (oder auf gar keinen). Ohne explizite Mechanismen (z. B. Shared Memory, bei dem beide Seitentabellen bewusst auf denselben Rahmen zeigen) haben Prozesse also keinen gemeinsamen Datenzugriff.

### d) Rechenaufgabe: 192 Byte Hauptspeicher, 10-Bit virtuelle Adressen, 16 Seiten

**1) Wie groß ist eine Speicherseite?**

**Deine Antwort:** *„16 Seiten entspricht binär 10000, also 5 Bit. Das heißt von den 10 Bit sind noch 5 für die Speicherseite frei.“*

**Bewertung: Leider ein Denkfehler ❌ (häufiger Klausur-Stolperstein!)**
Du hast berechnet, wie viele Bits man braucht, um die *Zahl 16 selbst* darzustellen (16 = 10000₂ = 5 Bit). Gesucht ist aber etwas anderes: wie viele Bits man braucht, um **16 verschiedene Seiten durchzunummerieren** (Seite 0 bis Seite 15). Das sind **log₂(16) = 4 Bit** (0000 bis 1111 deckt genau 16 Werte ab).

**Korrekter Rechenweg:**
- 16 Seiten → benötigte Bits für die Seitennummer: log₂(16) = **4 Bit**
- Virtuelle Adresse = 10 Bit gesamt → Offset = 10 − 4 = **6 Bit**
- Seitengröße = 2⁶ = **64 Byte**

**2) Wie viele Rahmen gibt es im Hauptspeicher?**

**Deine Antwort:** *„16 Rahmen pro Seite, 16 * 16“*

**Bewertung: Leider nicht korrekt ❌**, das folgt vermutlich aus dem Fehler in Teilaufgabe 1. Rahmen müssen (wegen der geforderten gleichen Bitbreite von Seiten- und Rahmennummer) **genauso groß wie eine Seite** sein, also ebenfalls 64 Byte.

**Korrekter Rechenweg:**
- Hauptspeicher = 192 Byte, Rahmengröße = Seitengröße = 64 Byte
- Anzahl Rahmen = 192 / 64 = **3 Rahmen**

**3) Seitennummer und Offset zur virtuellen Adresse `0110110100`**

**Deine Antwort:** Seitennummer: `01101`, Offset: `10100`

**Bewertung: Nicht korrekt ❌** (folgt aus dem 5-Bit-Fehler oben – zudem hat deine Aufteilung sogar nur 9 statt 10 Bit ergeben, das solltest du als Kontrolle immer gegenrechnen!).

**Korrekter Rechenweg:** Mit 4 Bit Seitennummer + 6 Bit Offset:
- Adresse: `0110 110100`
- **Seitennummer = 0110₂ = 6 (dezimal)**
- **Offset = 110100₂ = 52 (dezimal)**

**4) Physische Adresse, wenn die Seite in den zweiten Rahmen eingelagert ist** *(diese Teilfrage fehlt noch in deinen Notizen)*

- Rahmennummern haben dieselbe Bitbreite wie Seitennummern → **4 Bit**
- „Zweiter Rahmen“ = Rahmen Nr. 1 (0-indiziert: 1. Rahmen = Nr. 0, 2. Rahmen = Nr. 1) → binär `0001`
- Physische Adresse = Rahmennummer + Offset = `0001 110100`
- Umgerechnet: **116 (dezimal)**, binär **0001110100**

### e) Warum muss man die Seitennummern nicht in der Seitentabelle selbst abspeichern?

**Deine Antwort:** *„Weil dort nur die Adresse stehen muss?“*

**Bewertung: Richtige Intuition, aber noch zu ungenau formuliert 🙂** Der eigentliche Grund: Eine einfache Seitentabelle ist wie ein **Array**, das nach Seitennummer sortiert bzw. direkt danach indiziert ist. Die **Position (der Index) eines Eintrags in der Tabelle *ist* implizit die Seitennummer** – der 0-te Eintrag gehört zu Seite 0, der 1-te zu Seite 1 usw. Deshalb muss pro Zeile nur noch die zugeordnete **Rahmennummer** (plus Zusatzbits wie Present-Bit) gespeichert werden – die Seitennummer selbst wäre redundant, weil sie aus der Position folgt.

### f) Ein Prozess greift (mit virtueller Speicherverwaltung) auf die **physische** Adresse 0 zu – ein Problem?

**Deine Antwort:** *„Konventionsgemäß ist die Adresse 0 nicht belegt: null. Wenn es rein lesender Zugriff ist, ist es theoretisch kein unmittelbares Problem, wenn es aber ein schreibender Zugriff ist, dann wird dieser konventionelle Wert […] geändert.“*

**Bewertung: Das beschreibt eine wichtige, aber andere Konvention – hier liegt eine kleine Verwechslung vor ❌➜🙂**
Die „Adresse 0 = null/reserviert“-Konvention aus der VL bezieht sich auf die **virtuelle** Adresse 0 (die per Konvention von Software nicht belegt wird, um sie als „Zeiger ins Leere“ zu erkennen). Hier ist aber nach der **physischen** Adresse 0 gefragt.

**Der entscheidende Punkt:** Bei virtueller Speicherverwaltung greift ein Prozess **nie direkt auf physische Adressen zu** – das ist genau der Sinn der Adressabbildung! Der Prozess arbeitet ausschließlich mit virtuellen Adressen; welche physische Adresse (und damit welcher Rahmen) tatsächlich dahintersteckt, entscheidet die Seitentabelle/das OS, und ist für den Prozess unsichtbar. Physische Adresse 0 ist einfach eine ganz normale Speicherzelle wie jede andere – es gibt (anders als bei virtueller Adresse 0) keine besondere Konvention, dass sie frei bleiben müsste. **Kein Problem**, solange das OS die Zuordnung korrekt (und mit passenden Schutzrechten) vorgenommen hat.

### g) Kann virtuelle Adresse = physische Adresse sein?

**Ja, das kann vorkommen** – allerdings nur zufällig/für einzelne Adressen, nicht systematisch. Da der Offset-Teil einer Adresse bei der Übersetzung unverändert bleibt, müsste dafür lediglich die **Seitennummer zufällig mit der zugeordneten Rahmennummer übereinstimmen** (z. B. wenn Seite Nr. 3 gerade in Rahmen Nr. 3 eingelagert ist). Es gibt keinen Mechanismus, der das erzwingt oder verhindert – es ist reiner Zufall der aktuellen Zuordnung (in der Praxis z. B. häufiger bei „Identity Mapping“ für Betriebssystem-Bereiche).

### h) Warum sind einfache Seitentabellen speicherhungrig?

- **Ungenutzte Seite:** eine virtuelle Seite, für die der Prozess (noch) keine Daten abgelegt hat / die er nicht tatsächlich verwendet (z. B. noch nicht durch `malloc` angeforderter Bereich des Adressraums).
- **Warum verbraucht die Tabelle trotzdem Speicher dafür?** Weil eine *einfache* Seitentabelle wie ein durchgehendes Array funktioniert: Sie muss für **jede mögliche Seitennummer des gesamten virtuellen Adressraums** einen Eintrag bereithalten (auch für nie genutzte!), da die Position im Array die Seitennummer implizit codiert (vgl. Aufgabe e) – man kann keine Lücken „auslassen“.

**Rechenbeispiel (64-Bit-Adressen, 16 384 Byte = 2¹⁴ Byte Seitengröße, voller virtueller Adressraum nutzbar):**

- Anzahl Seiten = 2⁶⁴ / 2¹⁴ = **2⁵⁰ Seiten**
- Pro Eintrag wird laut Aufgabe nur die Rahmennummer gespeichert; diese braucht (gleiche Bitbreite wie Seitennummer) ebenfalls **50 Bit** ≈ aufgerundet 7 Byte (bzw. praktisch oft auf 8 Byte/Maschinenwort aufgerundet).
- Tabellengröße ≈ 2⁵⁰ × 7 Byte ≈ **7,9 · 10¹⁵ Byte ≈ 7 Petabyte** (bzw. bei 8-Byte-Einträgen: 2⁵³ Byte = genau **8 Pebibyte**).

**Zweite Teilfrage:** *„Prüfen Sie, wie viele Prozesse auf Ihrem System gerade laufen…“* – das ist eine Selbstbeobachtungsaufgabe (z. B. Task-Manager unter Windows, `ps aux | wc -l` bzw. `htop` unter Linux/macOS öffnen). Typischerweise laufen auf einem normalen PC **gleichzeitig mehrere Dutzend bis einige Hundert Prozesse**.

**Warum ist das ein Problem?** Wenn jeder einzelne Prozess (selbst bei kaum genutztem Adressraum) eine mehrere **Petabyte** große Seitentabelle bräuchte, wäre das mit einem normalen Rechner (wenige GB bis TB RAM) für **einen einzigen** Prozess schon unmöglich – bei Dutzenden bis Hunderten gleichzeitig laufenden Prozessen erst recht. Einfache (flache) Seitentabellen sind deshalb in der Praxis **nicht einsetzbar**; man braucht hierarchische oder invertierte Seitentabellen, die nur für tatsächlich genutzte Bereiche Speicher belegen.

### i) Referenzkette `3 5 0 4 1 2 3 0 5 0 0 1 2`, 3 Rahmen – FIFO vs. Optimal (Belady)

**FIFO-Verdrängung:**

| Zeit | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Referenz | 3 | 5 | 0 | 4 | 1 | 2 | 3 | 0 | 5 | 0 | 0 | 1 | 2 |
| Rahmen 0 | 3 | 3 | 3 | 4 | 4 | 4 | 3 | 3 | 3 | 3 | 3 | 1 | 1 |
| Rahmen 1 | – | 5 | 5 | 5 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 2 |
| Rahmen 2 | – | – | 0 | 0 | 0 | 2 | 2 | 2 | 5 | 5 | 5 | 5 | 5 |
| Seitenfehler? | F | F | F | F | F | F | F | F | F | · | · | F | F |

→ **11 Seitenfehler** bei FIFO.

**Optimale (Belady-)Verdrängung:**

| Zeit | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Referenz | 3 | 5 | 0 | 4 | 1 | 2 | 3 | 0 | 5 | 0 | 0 | 1 | 2 |
| Rahmen 0 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 5 | 5 | 5 | 1 | 1 |
| Rahmen 1 | – | 5 | 5 | 4 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| Rahmen 2 | – | – | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Seitenfehler? | F | F | F | F | F | F | · | · | F | · | · | F | · |

→ **8 Seitenfehler** bei Optimal (deutlich weniger als FIFO – wie erwartet, da Belady die theoretische Untergrenze darstellt).

### j) Belady-Verdrängung in der Praxis

- **Warum meist nicht nutzbar?** Belady benötigt Wissen über **zukünftige** Speicherzugriffe – in einem laufenden, allgemeinen System ist die Zukunft aber grundsätzlich unbekannt (abhängig von Nutzereingaben, Programmverzweigungen etc.).
- **Unter welcher harten Einschränkung dennoch einsetzbar?** Wenn die komplette Zugriffsfolge bereits **vorab vollständig bekannt** ist – z. B. bei einem deterministischen Batch-Programm ohne externe Eingaben, dessen Ablauf man vorher exakt kennt oder aufgezeichnet hat.
- **Sinnvolle Anwendung trotzdem:** Als **Vergleichsmaßstab (Benchmark)**: Man zeichnet die tatsächliche Zugriffsfolge eines realen Programmlaufs auf (z. B. per Profiler/Trace) und simuliert Belady im Nachhinein („offline“) auf diesen aufgezeichneten Daten. So erhält man die theoretisch minimal mögliche Anzahl an Seitenfehlern und kann damit bewerten, wie nah reale Algorithmen (FIFO, Aging, LRU, …) an dieses Optimum herankommen.

---

## Aufgabe 3: Ehemalige Klausuraufgabe

**Gegeben:** virtuelle Adresse `110101101` (9 Bit) ↔ physische Adresse `000101101` (9 Bit); insgesamt 8 Rahmen im Hauptspeicher.

**Wie viele Speicherzellen enthält der virtuelle Adressraum?**
Virtuelle Adressen sind 9 Bit breit → 2⁹ = **512 Speicherzellen (Byte)**.

**Wie viele Bit braucht die Rahmen-/Seitennummer?**
8 Rahmen → benötigt log₂(8) = **3 Bit**, um alle Rahmen (0–7) durchzunummerieren. Seiten- und Rahmennummer müssen gleiche Bitbreite haben → ebenfalls 3 Bit für die Seitennummer.
→ Offset = 9 − 3 = **6 Bit**.

**Welches Seitenoffset gehört zur physischen Adresse `000101101`?**
Aufteilung: `000` (Rahmennummer, 3 Bit) + `101101` (Offset, 6 Bit)
→ Offset = 101101₂ = **45 (dezimal)**.

**Wie lautet die Seitennummer der virtuellen Adresse `110101101`?**
Aufteilung: `110` (Seitennummer, 3 Bit) + `101101` (Offset, 6 Bit)
→ Seitennummer = 110₂ = **6 (dezimal)**.
*(Kontrolle: Der Offset-Teil ist bei beiden Adressen identisch `101101` – das muss so sein, da sich beim Übersetzen nur die Nummer, nie der Offset ändert. ✓)*

**Wie viele Bytes passen auf einen Speicherrahmen?**
Rahmengröße = 2^(Offset-Bits) = 2⁶ = **64 Byte**.

*Kleiner Hinweis am Rande:* Im Aufgabentext heißt es, die Adresse liege „im dritten Speicherrahmen“ – rechnerisch würden die führenden 3 Bit der physischen Adresse (`000`) aber Rahmen Nr. 0 (also den *ersten*, 0-indizierten Rahmen) codieren. Das ist eine kleine Ungenauigkeit in der Aufgabenformulierung; sie beeinflusst die eigentlichen Berechnungen (Bitbreiten, Offset, Seitengröße) aber nicht.

**Könnte man die Performance erhöhen, indem man durch zusätzliche Speichermodule das Auslagern reduziert?**
**Nein – hier nicht.** Der physische Adressraum ist durch die 9-Bit-Adressbreite auf maximal 2⁹ = 512 Byte begrenzt. Genau das ist bereits vollständig ausgeschöpft: 8 Rahmen × 64 Byte = 512 Byte. Selbst wenn man mehr physischen RAM einbauen würde, könnte das System ihn **gar nicht ansprechen**, da die Adressbreite (der eigentliche Flaschenhals) unverändert bliebe. Um mehr physischen Speicher sinnvoll nutzen zu können, müsste man stattdessen die **Adressbreite** erhöhen (mehr Bit pro Adresse).

---

## Kurzfazit zu deinen Antworten

| Aufgabe | Einschätzung |
|---|---|
| 1a | (nicht separat als Antwort formuliert, aber sinngemäß richtig erkannt: unregelmäßige Platzierung = externer Verschnitt) |
| 1c | ✅ Kern korrekt (räumliche Lokalität / Cache-Zeilen) |
| 2d-1 (Seitengröße) | ❌ Bit-Anzahl-Fehler: 16 *Werte* brauchen 4 Bit, nicht 16 als Zahl (5 Bit) |
| 2d-2 (Rahmenanzahl) | ❌ folgt aus obigem Fehler; korrekt: 3 Rahmen |
| 2d-3 (Seitennummer/Offset) | ❌ folgt aus obigem Fehler; korrekt: Seite 6, Offset 52 |
| 2e | 🙂 richtige Intuition, Begründung noch unvollständig |
| 2f | ❌➜🙂 Verwechslung von virtueller und physischer Adresse 0 – Kernaussage (Prozess hat gar keinen direkten physischen Zugriff) fehlte |

Der durchgängige Stolperstein ist der **Unterschied zwischen „Bits zur Darstellung der Zahl N“ und „Bits zur Durchnummerierung von N Objekten“** (log₂(N) statt Bitlänge von N selbst) – das lohnt sich, nochmal explizit einzuüben, da es in Klausuren sehr häufig gefragt wird.