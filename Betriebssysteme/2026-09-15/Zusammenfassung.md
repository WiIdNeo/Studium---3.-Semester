# Betriebssysteme X – Angriffe auf die Seitentabelle
## Zusammenfassung der Vorlesung + Lösungen zur Übung

---

## Teil 1: Zusammenfassung der Vorlesung

### 1. Instruktionsverarbeitung

**Von-Neumann-Architektur:** Ein Rechner besteht aus CPU (mit Rechenwerk/ALU und Steuerwerk), Hauptspeicher und Peripherie, verbunden über ein Bus-System (Adressbus + Datenbus). Da Maschinencode wie normale Daten im Speicher liegt, lässt er sich zur Laufzeit wie Daten behandeln.

**Befehlsabarbeitung** läuft typischerweise in vier Teilschritten ab:
1. **Instruction Fetch** – Befehl anhand des Befehlszählers ($isp) laden
2. **Instruction Decode** – Opcode interpretieren, Parameter/Register laden
3. **Execution** – Befehl im Rechenwerk ausführen
4. **Write Back** – Ergebnisse zurückschreiben (Register, Speicher, $isp)

**Pipelining:** Da während der naiven Abarbeitung meist nur ein Teil der CPU beschäftigt ist, lassen sich Teilschritte aufeinanderfolgender Befehle überlappend ausführen → höherer Durchsatz.

**Pipeline Hazards** verhindern nahtloses Pipelining:
- *Datenkonflikte* (z. B. Read-After-Write): ein Befehl braucht ein Ergebnis eines Vorgängerbefehls
- *Steuerkonflikte*: ein Befehl verändert den Befehlszähler, sodass der Folgebefehl vorher unbekannt ist

Ein Hazard führt zu einem **Pipeline Stall** (Anhalten früherer Pipeline-Stufen).

**Out-Of-Order-Execution:** Befehle ohne gegenseitige Abhängigkeit dürfen umsortiert werden, um Stalls zu vermeiden und die Auslastung zu erhöhen – das Endergebnis bleibt gleich.

**Branch Prediction (Sprungvorhersage):** Bei bedingten Sprüngen (z. B. `if`, `while`) kennt die CPU vorab nicht den tatsächlichen Ausgang. Über einen kleinen, adressbezogenen Zähler (Lookup-Struktur) schätzt die CPU anhand des bisherigen Verhaltens den wahrscheinlichen Ausgang und führt die Pipeline/Out-Of-Order-Execution spekulativ mit den vermuteten Folgebefehlen weiter. Stellt sich die Schätzung als falsch heraus, werden die *funktionalen* Folgen rückgängig gemacht.

---

### 2. Bekannte Angriffe

**Funktionales vs. nicht-funktionales Verhalten:** Funktionales Verhalten ist durch die Spezifikation festgelegt (z. B. Rechenergebnisse); nicht-funktionales Verhalten (z. B. Laufzeit, Cache-Belegung) ist nicht oder nur schwammig spezifiziert. Korrekte Programme dürfen sich nicht auf nicht-funktionales Verhalten verlassen.

- **Cache** ist ein klassisches Beispiel für nicht-funktionales Verhalten: Ob ein Datum im Cache liegt, beeinflusst nur die Zugriffszeit, nicht das funktionale Ergebnis.
- **Seitentabelle:** Auch hier gibt es nicht-funktionales Verhalten – z. B. bekommt eine allozierte Seite erst beim ersten Zugriff tatsächlich einen (vorbereiteten) Rahmen zugewiesen, was die Zugriffszeit, aber nicht das Ergebnis beeinflusst. Erweiterte Seitentabellen führen dazu u. a. Alloc-, Present-, Used- und Allow-Bits.

**Zentrale Beobachtung für Angriffe:** Bei einer Fehlschätzung eines bedingten Sprungs macht die CPU nur das *funktionale* Verhalten rückgängig – nicht-funktionale Nebeneffekte (insbesondere Cache-Änderungen) bleiben bestehen, weil man sich als korrektes Programm ohnehin nicht darauf verlassen darf und weil eine vollständige Rückabwicklung technisch aufwendig wäre.

Zusätzlich verschärfend: Seitentabellen sind aus Optimierungsgründen **nicht vollständig getrennt** – geteilte Seiten (z. B. DLLs, offene Dateien, Kernel-Bereiche) werden über Zugriffsrechte statt über physische Trennung geschützt.

#### Spectre (seit ca. 2017)
Seitenkanalangriff über Beobachtung nicht-funktionalen Verhaltens:
1. Die Sprungvorhersage eines bekannten, bedingten Zugriffsbefehls (z. B. einer bounds-check-Prüfung wie `at()`) wird mit gültigen, im Speicher liegenden Eingaben trainiert, sodass der geprüfte Zugriff normalerweise erlaubt wird.
2. Anschließend wird der Befehl mit einem eigentlich ungültigen Index aufgerufen, der über Zeigerarithmetik auf eine geschützte Speicherzelle zeigt. Die CPU sagt aufgrund des Trainings (fälschlich) vorher, dass der Zugriff erlaubt ist, und führt ihn spekulativ durch – ohne dass sich der eigentliche Fehler bereits functional äußert.
3. Der so spekulativ gelesene, geheime Wert wird über einen **indexierten Zugriff auf ein präpariertes Hilfsarray** (`attack_array`) in den Cache "geschrieben" – bevor die Sprungvorhersage als falsch erkannt und funktional zurückgenommen wird.
4. Nach der Rückabwicklung durchmisst der Angreifer alle möglichen Indizes des Hilfsarrays per Zeitmessung; das Teilarray mit sehr kurzer Zugriffszeit (Cache-Hit) verrät den gestohlenen Wert.

> **Korrektur (Folie 26):** Im Code-Beispiel der angreifbaren `at()`-Funktion muss die Bereichsprüfung `0 <= index && index < size_` lauten (nicht `0 < index && index < size_`). Mit `<` wäre der gültige Index `0` fälschlich ausgeschlossen; die untere Schranke muss inklusiv (`<=`) geprüft werden, damit die Funktion tatsächlich alle gültigen Indizes `0 … size_-1` zulässt.

#### Meltdown (seit ca. 2017)
Greift statt der Sprungvorhersage direkt die Out-Of-Order-Execution an – dadurch deutlich größere Angriffsfläche:
1. Ein Lesebefehl auf eine geschützte Speicherzelle wird ausgeführt und das Ergebnis in einem Register abgelegt, obwohl der Befehl eigentlich auf einen Zugriffsfehler läuft, den das OS behandeln muss (Prozess-/Thread-Abbruch).
2. Noch bevor die Fehlerbehandlung durch das OS greift, wird – dank Out-Of-Order-Execution – bereits ein vom gelesenen (eigentlich verbotenen) Wert abhängiger Zugriff auf ein Hilfsarray ausgeführt, der den Cache verändert.
3. Über einen zweiten Thread, der den abstürzenden Thread überlebt, wird der Cache-Inhalt wie bei Spectre per Zeitmessung ausgewertet.

---

### 3. Schutzmechanismen

**Einfache Maßnahmen:**
- Caching, Out-Of-Order-Execution bzw. Sprungvorhersage per Microcode/Firmware deaktivieren (großer bis mittlerer Performance-Verlust, ca. 4-fache bzw. 1,1–1,2-fache Laufzeit)
- Cache-Änderungen nach Fehlvorhersage aktiv zurücksetzen (kostet ebenfalls Performance und zusätzlichen Speicherplatz)
- Bei Zugriffsfehlern konsequent den ganzen Prozess statt nur den Thread beenden

**Komplexere Maßnahmen:**
- **Page Table Isolation (KPTI):** getrennte Seitentabellen für Kernel- und User-Mode, sodass im User-Mode keine fremden/Kernel-Seiten mehr eingeblendet sind; Wechsel bei Systemaufrufen/Rücksprüngen nötig (macht Threadwechsel teurer)
- **Jitter:** Zeitmessung künstlich verrauschen/abrunden, damit der Zeitunterschied zwischen Cache- und Hauptspeicherzugriff nicht mehr messbar ist (Nachteil für zeitkritische Anwendungen, z. B. Messtechnik/Physik)

---

## Teil 2: Lösungen zur Übung

### Aufgabe 1: Grundkonzepte

**a) Vorteil der Trennung Steuerwerk/Rechenwerk**

Die Trennung ermöglicht *Separation of Concerns*: Das Steuerwerk entscheidet, *welche* Operation ausgeführt wird und steuert den Ablauf, während das Rechenwerk nur die eigentliche Berechnung durchführt. Dadurch kann dasselbe Rechenwerk für verschiedenste Befehle wiederverwendet werden, die Hardware wird modularer und einfacher zu entwerfen/verifizieren. Diese klare Trennung ist zudem die Grundlage dafür, dass Steuerwerk und Rechenwerk (teilweise) parallel arbeiten können – eine Voraussetzung für Optimierungen wie Pipelining und Out-Of-Order-Execution.

**b) Speicherschutz durch Seitentabelle und virtuelle Adressen**

Jeder Prozess adressiert Speicher ausschließlich über seinen eigenen virtuellen Adressraum. Die CPU übersetzt bei jedem Zugriff die virtuelle Adresse über die *aktive*, prozesseigene Seitentabelle in eine physische Adresse. Da diese Seitentabelle nur Einträge für die dem Prozess tatsächlich zugewiesenen physischen Rahmen enthält (abgesehen von bewusst geteilten Seiten), kann ein Prozess über normale Adressierung gar nicht auf physische Adressen zugreifen, die anderen Prozessen gehören – es gibt schlicht keinen gültigen Übersetzungseintrag dafür. Zusätzlich sichern Zugriffsrechte (z. B. Kernel-Mode-Bit, Allow-Bits) auch geteilte Seiten gegen unbefugten Zugriff ab.

**c) Dekodieren**

- *Warum nötig:* Maschinencode liegt als reine Bytefolge im Speicher. Erst der Opcode legt fest, um welchen Befehl es sich handelt, wie viele und welche Parameter folgen und wie diese zu interpretieren sind. Ohne Dekodierung "weiß" die CPU nicht, was sie mit den folgenden Bytes anfangen soll.
- *Was passiert:* Der Opcode wird ausgelesen und anhand einer internen Zuordnung interpretiert; daraufhin werden die zugehörigen Parameter (z. B. Registernummern, Konstanten, Adressen) nachgeladen und die benötigten Register mit den Operanden gefüllt.
- *Warum der Befehlszähler ohne Dekodieren nicht korrekt inkrementiert werden kann:* Maschinencodebefehle haben unterschiedliche Längen (z. B. Opcode + variable Parameteranzahl + ggf. Padding, siehe `add`-Beispiel mit 8 Byte Gesamtlänge). Erst das Dekodieren verrät, wie viele Bytes der aktuelle Befehl tatsächlich belegt – ohne dieses Wissen könnte der Befehlszähler nicht zuverlässig auf den Beginn des nächsten Befehls gesetzt werden.

**d) Speedup**

- *Speedup einer n-stufigen Pipeline:* Im Idealfall (keine Hazards, vollständig gefüllte Pipeline) lässt sich ein Speedup von näherungsweise Faktor **n** erzielen.
- *Maximal erreichbarer Speedup bei beliebig vielen Stufen:* Rein rechnerisch ist der Speedup dann unbegrenzt (er geht gegen ∞), wenn man die Stufenanzahl beliebig erhöht.
- *Warum in der Praxis nicht erreichbar (zwei Argumente):*
  1. **Pipeline Hazards:** Daten- und Steuerkonflikte erzwingen immer wieder Stalls, sodass die Pipeline nicht durchgehend voll ausgelastet ist – der reale Speedup bleibt unter dem theoretischen Maximum.
  2. **Hardware-Overhead:** Jede zusätzliche Pipeline-Stufe benötigt zusätzliche Zwischenspeicher/Register und Steuerlogik. Der Overhead pro Stufe (z. B. Latch-Zeiten) sinkt nicht proportional mit, sodass ab einer gewissen Stufenzahl der Zugewinn durch mehr Parallelität vom Mehraufwand pro Takt aufgefressen wird.

**e) Einfluss der Out-Of-Order-Execution auf den Speedup**

Out-Of-Order-Execution erhöht den Speedup zusätzlich zum reinen Pipelining, indem sie die durch Hazards verursachten Lücken (Stalls) mit unabhängigen, eigentlich späteren Befehlen auffüllt. Dadurch werden CPU-Ressourcen (Bus, Rechenwerk, Steuerwerk) besser ausgelastet, auch wenn im Programmcode direkt aufeinanderfolgende Befehle voneinander abhängen.

**f) Warum sich Tracking für jeden Sprungbefehl nicht lohnt**

Nach dem Pareto-Prinzip verbringt ein Programm den Großteil seiner Laufzeit in wenigen, häufig durchlaufenen (meist inneren) Schleifen bzw. Sprüngen. Die meisten im Programm vorkommenden Sprungbefehle werden dagegen nur selten ausgeführt. Ein Zähler-Eintrag für *jeden* Sprungbefehl im Programm würde erstens sehr viel CPU-internen Speicherplatz benötigen und zweitens für die selten ausgeführten Sprünge kaum Vorhersagenutzen bringen. Es lohnt sich daher nur, wenige, aktuell/aktiv genutzte Sprungadressen in einer kompakten Lookup-Struktur zu verfolgen.

---

### Aufgabe 2: Programmierpraxis

**a) Write-After-Write-Hazard in C**

```c
int r0;

void beispiel(int a, int b, int c, int d)
{
    r0 = a + b;   // B1: erster Schreibzugriff auf r0
    r0 = c * d;   // B2: zweiter Schreibzugriff auf r0
}
```

Hier liegt ein Write-After-Write-Hazard vor, weil beide Befehle in dasselbe Ziel (`r0`) schreiben. Der scheinbare Einwand "B2 überschreibt B1 ohnehin, also ist die Reihenfolge egal" übersieht den eigentlichen Denkfehler: Entscheidend ist **nicht** der Wert an sich, sondern **wann** welcher Schreibzugriff tatsächlich in der Hardware abgeschlossen wird (Write-Back-Zeitpunkt). Wenn z. B. `c * d` (B2) schneller berechnet ist als `a + b` (B1) und die Pipeline die Befehle nicht in Programmreihenfolge zurückschreibt, könnte B1 *nach* B2 abgeschlossen werden. Dann stünde am Ende fälschlich das Ergebnis von B1 in `r0`, obwohl laut Programmsemantik das Ergebnis von B2 (dem letzten Schreibzugriff im Quellcode) gelten muss. Der Hazard erzwingt also, dass die *Reihenfolge* der Schreibvorgänge in der tatsächlichen Ausführung mit der Programmreihenfolge übereinstimmt.

**b) Speedup durch Pipelining messen**

Grundidee: Man vergleicht die Laufzeit eines langen, abhängigen Befehlsstroms (verhindert Pipelining/OoO) mit der Laufzeit eines vergleichbaren, unabhängigen Befehlsstroms (erlaubt Pipelining).

```c
#include <stdio.h>
#include <time.h>

#define N 100000000

int main(void)
{
    volatile long x = 1; // volatile verhindert Wegoptimieren
    struct timespec t1, t2;

    // Variante 1: durchgehende Datenabhängigkeit (Hazard bei jedem Schritt)
    clock_gettime(CLOCK_MONOTONIC, &t1);
    for (long i = 0; i < N; ++i)
        x = x + 1;          // jeder Schritt braucht das Ergebnis des vorigen
    clock_gettime(CLOCK_MONOTONIC, &t2);
    printf("Mit Hazard:    %ld ns, x=%ld\n",
        (t2.tv_sec - t1.tv_sec) * 1000000000L + (t2.tv_nsec - t1.tv_nsec), x);

    // Variante 2: unabhängige Additionen auf getrennte Variablen
    volatile long a = 1, b = 1, c = 1, d = 1;
    clock_gettime(CLOCK_MONOTONIC, &t1);
    for (long i = 0; i < N; ++i) {
        a = a + 1; b = b + 1; c = c + 1; d = d + 1; // gegenseitig unabhängig
    }
    clock_gettime(CLOCK_MONOTONIC, &t2);
    printf("Ohne Hazard:   %ld ns, a=%ld b=%ld c=%ld d=%ld\n",
        (t2.tv_sec - t1.tv_sec) * 1000000000L + (t2.tv_nsec - t1.tv_nsec), a, b, c, d);

    return 0;
}
```

Wichtige Punkte bei der Durchführung:
- `volatile` verhindert, dass der Compiler die Schleife wegoptimiert oder die Reihenfolge selbst verändert.
- Variante 1 erzeugt bei *jedem* Schritt eine Datenabhängigkeit (Read-After-Write auf `x`) – die CPU kann hier kaum pipelinen/parallelisieren.
- Variante 2 verwendet vier unabhängige Akkumulatoren, sodass die CPU die Additionen parallel/pipeline-mäßig verarbeiten kann.
- Messung sowohl im Debug- als auch im Release-Modus durchführen, da der Compiler im Release-Modus selbst umsortiert/vektorisiert.
- Den erzeugten Assemblercode gegenprüfen (z. B. `gcc -S` bzw. Disassembler), um sicherzustellen, dass der Compiler die Abhängigkeit nicht selbst wegoptimiert oder die Datenabhängigkeit anders auflöst als beabsichtigt, und dass die Eingabewerte nicht schon zur Compile-Zeit konstant gefaltet wurden (deshalb `volatile`, ggf. Startwerte erst zur Laufzeit z. B. über `argv`/`rand()` setzen).

**c) Speedup durch Out-Of-Order-Execution messen**

Analoges Vorgehen wie in b), aber die Hazard-Kette muss über den *gesamten* gemessenen Programmabschnitt gehen, damit nicht nur das Pipelining, sondern auch die Out-Of-Order-Execution keine unabhängigen Folgebefehle vorziehen kann:

```c
// Variante mit durchgehender Kette (jeder Befehl hängt vom Ergebnis
// des unmittelbar vorherigen ab -> auch OoO kann hier nichts umsortieren)
for (long i = 0; i < N; ++i)
    x = x * 3 + 1;   // jede Iteration hängt direkt von der vorigen ab

// Variante mit klar getrennten, voneinander unabhängigen Ketten
for (long i = 0; i < N; ++i) {
    a = a * 3 + 1;
    b = b * 3 + 1;
    c = c * 3 + 1;
    d = d * 3 + 1;    // vier unabhängige Ketten -> Out-Of-Order kann sie mischen
}
```

Da im ersten Fall *jeder einzelne* Befehl vom direkten Vorgänger abhängt, gibt es für die Out-Of-Order-Execution keine unabhängigen, vorziehbaren Befehle mehr – die Kette muss strikt sequenziell abgearbeitet werden. Auch hier gelten dieselben Vorsichtsmaßnahmen wie in b) (Debug-/Release-Vergleich, Assembly-Kontrolle, `volatile`, Laufzeit-Erzeugung der Startwerte).

**d) Vom Optimierungskonzept zum Sicherheitsproblem**

Ausgangscode:
```c
const size_t size_ = 128;
char array[size_] = { /* ... */ };

char get_data(size_t index)
{
    if (index >= size_) return '\0';
    return array[index];
}
```

- **Gibt es einen `index`, der undefiniertes Verhalten auslöst?**
  Im Sinne der Sprachsemantik: **Nein.** `index` ist `size_t` (vorzeichenlos), sodass negative Werte ausgeschlossen sind, und die Prüfung `index >= size_` fängt alle zu großen Indizes korrekt ab, bevor auf `array` zugegriffen wird. Die Funktion ist also funktional vollkommen korrekt – genau das macht sie zu einem typischen "Spectre-Gadget": Der Angriffspunkt liegt nicht in einem Sprachfehler, sondern im *nicht-funktionalen* (spekulativen) Verhalten der Hardware.

- **Wie lässt sich die Sprungvorhersage der Prüfung beeinflussen?**
  Indem man `get_data()` viele Male hintereinander mit gültigen, kleinen `index`-Werten aufruft. Die CPU lernt aus diesem Muster, dass die Bedingung `index >= size_` üblicherweise *falsch* ist (der Zugriffspfad `return array[index]` also üblicherweise genommen wird), und sagt dieses Verhalten künftig voraus.

- **Wie bringt man `get_data()` dazu, auf eine beliebige, bekannte Adresse `ptr` zuzugreifen?**
  Man berechnet `index` als Zeigerdifferenz `index = ptr - array` (als `size_t` interpretiert – bei `ptr` außerhalb von `array` ergibt das einen sehr großen, eigentlich ungültigen Wert) und ruft `get_data(index)` unmittelbar nach dem Trainieren der Sprungvorhersage auf. Die CPU sagt spekulativ voraus, dass `index < size_` gilt, und liest spekulativ `array[index]`, was wegen der Zeigerarithmetik tatsächlich `*ptr` entspricht.

- **Warum darf der spekulative Zugriff auf eine geschützte Adresse keine negativen Konsequenzen haben (z. B. Absturz bei Adresse 0)?**
  Weil dieser Zugriff nur im Rahmen einer *möglicherweise falschen* Sprungvorhersage passiert – die tatsächliche, spezifikationskonforme Ausführung des Programms führt diesen Zugriff nach der (korrekten) Prüfung eventuell nie durch. Für `ptr = 0` ergibt sich `index = 0 - (size_t)array` (modulo Adressraumgröße). Würde jeder spekulative, letztlich verworfene Zugriff sofort zum Programmabsturz führen, wäre die gesamte Spekulationstechnik (Pipelining/Sprungvorhersage) praktisch unbrauchbar, da man dann nie "auf Verdacht" auf Speicher zugreifen dürfte.

- **Warum hilft die Rückgabe von `get_data()` nicht direkt weiter?**
  Weil bei einer Fehlschätzung genau diese Rückgabe – der eigentlich gestohlene Wert – *funktional* zurückgenommen wird. Der tatsächliche, korrekte Kontrollfluss durchläuft stattdessen den `if`-Zweig (`return '\0'`); der spekulative Rückgabewert ist für das aufrufende Programm nie sichtbar.

- **Was genau muss die CPU bei einer Fehlschätzung rückgängig machen?**
  Alle *funktionalen* Zustandsänderungen: Registerinhalte, den Befehlszähler, ggf. bereits (spekulativ) durchgeführte Schreibzugriffe und sichtbare Ausgaben. Der eigentliche Speicherzugriff auf `*ptr` selbst (das Lesen an sich) lässt sich dabei aus Sicht der Architektur einfach verwerfen.

- **Welcher Seiteneffekt lässt sich nur schwer/mit großem Aufwand rückgängig machen?**
  Der **Cache-Zustand**: Durch den spekulativen Lesezugriff wird eine Cache-Line geladen (und dabei ggf. eine andere verdrängt). Um dies vollständig rückgängig zu machen, müsste die CPU vor jeder Spekulation den kompletten betroffenen Cache-Zustand sichern und bei Fehlschätzung wiederherstellen – das würde zusätzlichen Speicher- und Rechenaufwand für *jede* Spekulation bedeuten und den durch Spekulation gewonnenen Performance-Vorteil zunichtemachen.

- **Wie nutzt man den Seiteneffekt aus, um Informationen über `array[index]` zu erhalten (Rückgabewert geeignet weiterverrechnen)?**
  Man verwendet den spekulativ gelesenen (später verworfenen) Wert `c = get_data(attack_index)` nicht direkt, sondern führt – noch innerhalb desselben spekulativen Ausführungsfensters – einen weiteren, vom Wert abhängigen Speicherzugriff durch, z. B. `attack_array[c][0]`. Dieser zweite Zugriff hinterlässt eine wertabhängige Cache-Line im Cache und "überlebt" damit die spätere Rückabwicklung der eigentlichen (funktionalen) Rückgabe.

- **Wie lässt sich der Wert von `array[index]` letztlich per Messung ermitteln?**
  Nach dem spekulativen Zugriff werden alle möglichen Werte (z. B. 0–255) von `attack_array[v][0]` einzeln mit einem hochauflösenden Timer durchgemessen. Das Teilarray mit deutlich kürzerer Zugriffszeit liegt bereits im Cache – sein Index `v` entspricht dem gestohlenen Wert von `array[index]`.

**e) Meltdown und Spectre im Vergleich**

*Funktionsweise in eigenen Worten:*
- **Meltdown** nutzt aus, dass viele CPUs bei einem Speicherzugriff die eigentliche Rechteprüfung (Permission Check) erst *nach* der spekulativen Out-Of-Order-Ausführung abgeschlossen wird. Ein Programm liest ohne Berechtigung eine geschützte (z. B. Kernel-) Speicherzelle; obwohl der Zugriff letztlich einen Fehler auslöst, hat die CPU den gelesenen Wert bereits kurzzeitig verwendet, um – spekulativ, aber messbar über den Cache – einen abhängigen Folgezugriff durchzuführen.
- **Spectre** nutzt stattdessen die Sprungvorhersage aus: Ein bedingter, eigentlich schützender Vergleich (z. B. eine Bereichsprüfung) wird gezielt trainiert, sodass die CPU spekulativ den "erlaubten" Pfad nimmt, obwohl die tatsächliche Bedingung dies verbietet. Der so spekulativ gelesene, geschützte Wert wird über einen zweiten, wertabhängigen Zugriff in den Cache übertragen und danach per Zeitmessung ausgelesen.

*Ausgenutzte Schwachstelle / Hardware-Voraussetzungen:*
- Meltdown: verzögerte Rechteprüfung bei spekulativer/Out-Of-Order-Ausführung; betrifft vor allem CPUs, die Zugriffe ausführen, bevor die Berechtigung final geklärt ist (v. a. viele Intel-CPUs sowie einzelne andere Architekturen).
- Spectre: manipulierbare, prozess-/kontextübergreifend geteilte Sprungvorhersage-Strukturen; betrifft praktisch alle modernen CPUs mit spekulativer Ausführung und Branch Prediction (Intel, AMD, ARM u. a.).

*Vorgehen des Angreifers / benötigter Zugriff:*
- Beide Angriffe benötigen lediglich die Möglichkeit, unprivilegierten Code auf dem Zielsystem auszuführen (z. B. als normaler Prozess, als Skript im Browser/JS-Interpreter oder als Gast-VM) – keine speziellen Rechte. Meltdown liest direkt geschützten Speicher aus; Spectre trainiert zunächst gezielt eine Sprungvorhersage und missbraucht sie danach mit präparierten Eingaben.

*Welche Daten lassen sich jeweils ausleiten?*
- Meltdown: beliebiger, in den Adressraum des Prozesses eingeblendeter, aber eigentlich geschützter Speicher – klassischerweise Kernel-Speicher, der (vor Einführung von KPTI) aus Performance-Gründen in jeden Prozess eingeblendet war.
- Spectre: Daten innerhalb derselben oder einer über Sprungvorhersage-Strukturen geteilten Ausführungsumgebung, z. B. Daten anderer Sandboxen/Tabs im selben Prozess, oder – bei Varianten mit geteilter Vorhersage-Hardware – auch Daten anderer Prozesse/VMs.

*Gemeinsamkeiten und Unterschiede:*
- Gemeinsam: Beide nutzen spekulative Ausführung aus, deren *funktionale* Folgen zwar zurückgenommen werden, deren *nicht-funktionale* Nebenwirkungen (Cache-Zustand) aber bestehen bleiben, und lesen diese Nebenwirkungen über einen Timing-Seitenkanal aus.
- Unterschied: Meltdown greift direkt die verzögerte Rechteprüfung bei Out-Of-Order-Execution an und betrifft primär privilegierte Speicherbereiche; Spectre missbraucht die Sprungvorhersage und wirkt allgemeiner auch innerhalb von Software-Grenzen im selben Adressraum (Sandboxen), weshalb es deutlich schwerer vollständig zu beheben ist.

*Warum ist eine Behebung schwierig?*
Die Ursache liegt tief in der Hardware-Architektur (spekulative Ausführung als zentrale Performance-Optimierung seit Jahrzehnten). Ein vollständiges Abschalten der Spekulation würde massive Performance-Einbußen bedeuten. Es gibt daher nur Teillösungen auf verschiedenen Ebenen:
- **Software:** gezielte Schutzbarrieren (z. B. Fence-Befehle), Bounds-Check-Masking, Compiler-Techniken wie Retpoline
- **Hardware:** überarbeitete Spekulationslogik in neueren CPU-Generationen bzw. Microcode-Updates (mit teils spürbarem Performance-Verlust)
- **Betriebssystem:** Page Table Isolation (KPTI) gegen Meltdown, Einschränkung hochauflösender Timer, Prozess-/Sandbox-Isolation gegen Spectre

Da jede Ebene nur einen Teil der Angriffsfläche abdeckt und neue Varianten laufend entdeckt werden, gilt das Problem bis heute nicht als vollständig gelöst.

*Welches Paper beschreibt den in Teilaufgabe d) behandelten Angriff?*
Die in d) beschriebene `get_data()`-Bereichsprüfung, die über eine trainierte Sprungvorhersage umgangen wird, entspricht dem klassischen **Spectre**-Angriff (genauer: der Variante "Bounds Check Bypass") und wird demnach im **spectre.pdf**-Paper beschrieben.

**f) Aktuelle Spectre-Angriffsvariante (Recherche)**

Auch Jahre nach der ursprünglichen Veröffentlichung werden immer wieder neue Spectre-Varianten gefunden, weil sich das grundlegende Problem (spekulative Ausführung + Seitenkanal) nicht ohne massive Performance-Einbußen beheben lässt. Beispiele:

- **Branch Privilege Injection (BPI, CVE‑2024‑45332):** 2024 von Forschenden der ETH Zürich entdeckt. Betroffen sind zahlreiche aktuelle Intel-CPUs. Anstatt die Sprungvorhersage über gültige Eingaben zu trainieren, missbraucht dieser Angriff eine Unstimmigkeit darin, **wann** die CPU eine Vorhersage aus einem niedriger privilegierten (Nutzer-)Kontext für einen höher privilegierten (Kernel-)Kontext übernimmt. Dadurch lässt sich die Vorhersagelogik so beeinflussen, dass der Kernel spekulativ Code an einer vom Angreifer kontrollierten Adresse ausführt und dabei geschützte Daten über den bekannten Cache-Seitenkanal preisgibt – die bisherigen, seit sieben Jahren etablierten Software-Gegenmaßnahmen greifen hier nicht.
- **VMSCAPE (CVE‑2025‑40300, 2025):** Erstmals gelingt es, allein aus einer bösartigen Gast-VM heraus über eine unvollständige Isolation der Sprungvorhersage-Strukturen Geheimnisse des Host-Hypervisors auszulesen – ohne Codeänderungen am Hypervisor, allein durch spekulative "Return-Oriented-Programming"-Gadgets im Zielprozess.
- **TONTOU (2026):** Nutzt ein sehr kleines Zeitfenster zwischen dem Bereinigen einer für die Sprungvorhersage genutzten CPU-Struktur und deren erneuter Nutzung aus, um die Linux-Gegenmaßnahme "Safe RET" gegen Spectre v2 zu umgehen; auf älteren AMD-Prozessoren (Zen 2) konnten die Forschenden damit beliebige Kernel-Speicherbereiche und sogar sensible Systemdateien auslesen.

Gemeinsam ist diesen neueren Varianten, dass sie nicht mehr die "klassische", ursprünglich vorgestellte Bounds-Check-Bypass-Technik nutzen, sondern subtilere Lücken *innerhalb* der bereits existierenden Schutzmechanismen (z. B. zeitliche Lücken beim Umschalten von Kontexten oder unvollständige Isolation der Vorhersage-Hardware zwischen Privilegienstufen) ausnutzen – ein weiteres Indiz dafür, dass Spectre als grundsätzliches Hardware-Designproblem bislang nicht vollständig lösbar ist, solange spekulative Ausführung aus Performance-Gründen aktiv bleibt.