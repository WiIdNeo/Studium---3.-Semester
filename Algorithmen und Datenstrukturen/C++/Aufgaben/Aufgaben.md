# Algorithmen und Datenstrukturen – Übersicht aller Praxisaufgaben

Geordnet nach Übungsblatt und Aufgabennummer, mit Abhängigkeiten zwischen den Blättern.
Quelle: Übungsblätter 1–6 (Tobias Werner, Leibniz-FH Hannover).

---

## 1. Abhängigkeitskarte (Wer baut auf wem auf?)

```
Ü3 2d rabbit ──► Ü3 2e stall (Häschenkette) ──────────────► Ü6 2a Liste (+ Iterator, Knoten)
                                                                  │
                                                                  ├─► Ü6 2b Einfügen/Löschen in Liste
                                                                  ├─► Ü6 2g fifo_queue
                                                                  └─► Ü6 2h Zeitmessung (Liste)

Ü3 2b int_smart_pointer ─► Ü3 2c (flache Kopie)      (eigenständig, Konzept für Rule of Three)

Ü4 2b string ─► Ü4 2c / 2d (Fehleranalyse an string)
        └─────► Ü5 2b (std::string im vector – Vergleichsfall)

Ü4 3b int_vector ─► Ü4 3c Tests
        │
        └─► Ü5 2a template vector<T> ─► Ü5 2b (std::string) ─► Ü5 2c vector_iterator
                    │                                             ├─► Ü5 2d Iterator-Kategorie
                    │                                             └─► Ü5 2e Einzeiler-Lösung
                    │
                    └─► Ü6 2b Einfügen/Löschen im Array
                        Ü6 2c heapify (+ sift_up, heap-Wrapper, check_heap)
                        Ü6 2d extract_max
                        Ü6 2e heap_sort
                        Ü6 2f binary_search
                        Ü6 2h Zeitmessung (Array, Heap)
```

**Wichtigste Ketten, die man sicher aufbewahren sollte:**

| Kette | Blätter | Endprodukt |
|---|---|---|
| Hase → Stall → Liste | Ü3 → Ü6 | Generische doppelt verkettete Liste |
| `int_vector` → `vector<T>` → Heap-Algorithmen | Ü4 → Ü5 → Ü6 | Template-Array mit Iterator, Heap, Sortierung, Suche |
| `string` | Ü4 (→ Ü5) | Eigene String-Klasse (Aufgabenblatt: „wird noch erweitert“) |

---

## 2. Schnellübersicht (Checkliste)

| Blatt | Aufgabe | Thema | Baut auf | Wird verwendet in |
|---|---|---|---|---|
| Ü1 | 3d | Zeitmessung Konvertierungen (float ↔ string) | – | – |
| Ü1 | 3e | float ↔ string, umkehrbar, alle Werte testen | – | – |
| Ü1 | 3f | (für Profis) menschenlesbar, umkehrbar | 3e | – |
| Ü2 | 4a | Präprozessor-Makro vervollständigen | – | – |
| Ü2 | 5a | Projekt battery / robot / car / main | – | Ü2 5b |
| Ü2 | 5b | Dasselbe ohne eigene Header | 5a | – |
| Ü2 | 8a | Vier Zeiger-Fehler-`main()` | – | – |
| Ü3 | 2a | `window`-Konstruktoren (Deklarationen) | – | – |
| Ü3 | 2b | `int_smart_pointer` (tiefe Kopie) | – | 2c |
| Ü3 | 2c | `int_smart_pointer` mit flacher Kopie | 2b | – |
| Ü3 | 2d | Klasse `rabbit` | – | 2e |
| Ü3 | 2e | `rabbit`-Hände + Klasse `stall` | 2d | **Ü6 2a** |
| Ü4 | 2b | Klasse `string` | – | 2c, 2d, Ü5 2b |
| Ü4 | 3a | Mehrstufiges 3D-Array (Codefragment) | – | – |
| Ü4 | 3b | Klasse `int_vector` | – | 3c, **Ü5 2a** |
| Ü4 | 3c | Tests für `int_vector` | 3b | – |
| Ü5 | 2a | `int_vector` → `template vector<T>` | Ü4 3b | 2b, 2c, Ü6 |
| Ü5 | 2b | `vector<std::string>` ermöglichen | 2a | – |
| Ü5 | 2c | `vector_iterator` | 2a/2b | 2d, 2e |
| Ü5 | 2d | Iterator-Kategorie bestimmen | 2c | – |
| Ü5 | 2e | 2c in einer einzigen Zeile | 2c | – |
| Ü6 | 2a | Häschenkette → generische Liste + Iterator + Knoten | Ü3 2e | 2b, 2g, 2h |
| Ü6 | 2b | Einfügen/Löschen in Array und Liste | Ü4 3b / Ü5 2a, 2a | – |
| Ü6 | 2c | `heapify` (Max-Heap), `sift_up`, `check_heap` | Array | 2d, 2e |
| Ü6 | 2d | `extract_max` | 2c | 2e |
| Ü6 | 2e | `heap_sort` | 2c, 2d | 2f |
| Ü6 | 2f | `binary_search` | 2e (sortiertes Array) | – |
| Ü6 | 2g | `fifo_queue` auf Basis der Liste | 2a | – |
| Ü6 | 2h | Laufzeitmessung Array/Liste/Heap | 2a, 2c | – |

---

## 3. Details je Blatt

---

### Übung 1 – Einführung

#### Aufgabe 3d – Kosten der Datenkonvertierung (C)
- `float`-Array mit mehreren Millionen Zufallswerten in [0, 1] füllen.
- **Schleife 1:** alle Einträge in Zeichenfolgen umwandeln, in `char*`-Array speichern.
- **Schleife 2:** alle Zeichenfolgen zurück in `float` wandeln und das `float`-Array überschreiben.
- **Schleife 3 (Vergleich):** abwechselnd addieren/subtrahieren (`arr[1] + arr[2] - arr[3] + ...`).
- Zeit je Schleife messen. Fragen: Welche ist am teuersten? Wie viel teurer ist Konvertierung als Rechnen? (Profis: Wo geht die Zeit verloren → Profiler.)
- Hinweise: Ergebnisse ins Array zurückschreiben (gegen Wegoptimieren); keine `printf`-Ausgaben in der Schleife.

#### Aufgabe 3e – Umkehrbare float → string-Konvertierung (C++)
- Funktion `to_string`: beliebige Bitbelegung eines `float` → Zeichenfolge, **bitgenau umkehrbar**.
- Rückkonvertierung `to_float` implementieren.
- Es muss `to_float(to_string(v)) == v` gelten; **Beweis durch Test aller 2³² Bitmuster**.
- Hinweis: Inhalt muss nicht menschenlesbar sein (Idee: BASE64-artige Kodierung).

#### Aufgabe 3f – (für Profis) Menschenlesbar und umkehrbar
- Wie 3e, aber der String soll eine lesbare Darstellung haben (Dezimal- oder Exponentialschreibweise).
- Sonderwerte (NaN, INF) dürfen als fester Text kodiert werden.

---

### Übung 2 – Grundlagen C und C++

#### Aufgabe 4a – Präprozessor
- Programmfragment **nur an der markierten Stelle** (`#define PRINT_PREPROCESSED /* ??? */`) so ergänzen, dass `"Preprocessed"` ausgegeben wird.

```cpp
#include <iostream>
#define PRINT_PREPROCESSED /* ??? */
int main( PRINT_PREPROCESSED }
```

#### Aufgabe 5a – Mehrdateien-Projekt (Stack only)
Je Modul ein Paar `.hpp`/`.cpp`:
- **battery:** Klasse `battery`, Methode `void power_on()` → gibt `"Starting up"` aus (`iostream`).
- **robot:** Klasse `robot` mit einer Membervariable `battery`; Default-Konstruktor ruft `power_on()` und gibt dann `"Robot ready"` aus.
- **car:** Klasse `car` mit einer Membervariable `battery`; Default-Konstruktor ruft `power_on()` und gibt dann `"Car ready"` aus.
- **main:** freie `main`, erzeugt erst einen `robot`, dann ein `car` – nur auf dem Stack.
- Auf korrekte Header achten: Inclusion Guards, richtige Aufteilung Header/Source, Include-Reihenfolge laut Vorlesung (eigener Header zuerst in der zugehörigen `.cpp`, eigene Header nach Standard-/Fremdheadern).

#### Aufgabe 5b – Ohne eigene Header
- Klassenaufteilung auf `.cpp`-Dateien beibehalten, **keine eigenen Header**.
- Systemheader nutzbar, aber nicht bearbeiten. Header umbenennen und `#include`n ist **keine** zulässige Lösung.

#### Aufgabe 8a – Vier Zeigerfehler
Vier `main()`-Methoden, je mit Nachricht nach dem Schreibzugriff:
1. `int` 1337 an Adresse 0–3 schreiben
2. `int` 1337 an feste Adresse 19522430–…33 schreiben
3. `int` 1337 auf bereits deallokierte **Stack**-Variable
4. `int` 1337 auf bereits deallokierte **Heap**-Variable

Beobachten: Verhalten im Debug-Build (in welcher Zeile unterbricht der Debugger?) und im Release-Build. **Code mit abgeben.**
(Visual Studio: Sicherheitsfeatures unter *Code Generation* ggf. abschalten.)

> **Grenzfälle in Ü2 mit Code-Anteil (eher Theorie):** 4b (Makro-Ausgaben vorhersagen), 6a/6b (Code vereinfachen), 7c/7d (Fehlersuche), 8b/8c (Fehleranalyse). Nicht als eigenständige Programmieraufgaben gelistet.

---

### Übung 3 – Objektorientierte Programmierung

#### Aufgabe 2a – `window`-Konstruktoren (nur Deklarationen)
Geeignet überladene/benannte Methoden für:
- leeres Hauptfenster mit Standardeigenschaften
- Hauptfenster mit Größe in X und Y
- Hauptfenster mit Überschrift
- Fenster innerhalb eines Elternfensters
- Hauptfenster mit beliebig vielen Kindfenstern
- Fenster aus Ressourcendatei (Pfad) laden

(Konstruktoren sind auch Methoden – ggf. statische benannte Fabrikmethoden nötig, wenn Signaturen kollidieren.)

#### Aufgabe 2b – `int_smart_pointer` (tiefe Kopie)
- Besitzt immer einen `int` auf dem Heap und merkt sich dessen Adresse.
- `set` / `get`; von außen weder löschbar noch neu anlegbar.
- Konstruktor mit optionalem Anfangswert (sonst 0).
- **Tiefe Kopie:** neue Heap-Allokation, gleicher Wert.
- Destruktor: kein Speicherleck.
- **Jede Operation gibt ihren eigenen Namen auf der Konsole aus.**
- Test:

```cpp
int_smart_pointer a;          std::cout << a.get() << std::endl; // 0
a.set(5);                     std::cout << a.get() << std::endl; // 5
int_smart_pointer b(10);      std::cout << b.get() << std::endl; // 10
int_smart_pointer c(b);       std::cout << c.get() << std::endl; // 10
c.set(20);
std::cout << b.get() << std::endl; // 10
std::cout << c.get() << std::endl; // 20
```

#### Aufgabe 2c – Flache Kopie (Änderung von 2b)
- Kopie verwendet **denselben** `int` wie das Original.
- Frage: Was geht schief? (Fehler muss sich nicht zwingend sichtbar äußern; mit obigem Test prüfen.)

#### Aufgabe 2d – Klasse `rabbit`
- Attribute: Name (`std::string`), Ohrenzahl (Ganzzahl), Alter in Wochen (Ganzzahl), Gewicht in Gramm (Gleitkomma), `essbar` (bool).
- Konstruktor mit Name + Ohrenzahl; Start: 100 g, 0 Wochen.
- `altern()`: Alter +1 Woche.
- `füttern()`: Gewicht + Zufallszahl zwischen 10 und 200.
- `essbar` ist wahr bei Alter **9–12 Wochen** und Gewicht **1500–2000 g**; stets konsistent; von außen nur lesbar.
- `main` zum Testen: mehrere Hasen anlegen, altern lassen, Essbarkeit prüfen.

#### Aufgabe 2e – Häschenkette und `stall`  ⟶ *Grundlage für Ü6 2a*
**Erweiterung `rabbit`:** linke und rechte Hand, jeweils anderer Hase oder keiner.

**Klasse `stall`:**
- Durchgehende Kette; erster Hase hat links keinen Partner, letzter rechts keinen.
- Stall merkt sich **nur den ersten Hasen**.
- `hinzufügen`: legt neuen Hasen an und hängt ihn hinten an (neuer Hase: rechte Hand leer).
- `züchten`: alle Hasen altern und füttern.
- `ernten`: alle Hasen durchgehen; entfernen, wenn essbar **oder** älter als 50 Wochen.
- `inventarisieren`: Daten aller Hasen auf der Konsole ausgeben.

**Test:** Hasen einfügen, abwechselnd züchten und ernten, bis der Stall leer ist; nach jedem Schritt Zustand ausgeben (in der Aufgabe „prüfen“ genannt, gemeint ist vermutlich `inventarisieren`).

---

### Übung 4 – Arrays

#### Aufgabe 2b – Klasse `string`  ⟶ *„wird in nachfolgenden Blättern erweitert“*
Nur `malloc()`, `realloc()`, `free()`; **kein** `strlen`, `strcpy`, `memcpy`; keine Hilfsklassen (`std::vector`, `std::string`, …). `iostream` für Ausgabe erlaubt.

| Methode | Anforderung | Leitfrage |
|---|---|---|
| `string()` | Kopie von `""` | – |
| `string(const char* data)` | Kopie der Zeichenkette | Voraussetzung an `data`? Was bei `nullptr`? |
| `char* data()` | aktuelle Zeichenkette | Kann `nullptr` zurückkommen? |
| `void clear()` | Zeichenkette löschen | `nullptr` vs. `""` – was ist sinnvoll? |
| `void print()` | ausgeben | – |
| `int find(char c)` | Index des Zeichens | Was, wenn nicht gefunden? |
| `void append(const char*)` | anhängen | – |
| `~string()` | Zeichenkette freigeben | Genügt `clear()`? |

- Sinnvolle Aufteilung Header/Source, Klasse dokumentieren (Spezialfälle für Nutzer).
- `main` mit Tests, insbesondere **Spezial- und Randfälle** (`nullptr`-Eingaben, Suche nach `\0`).
- Die Leitfragen müssen nicht explizit beantwortet werden.

#### Aufgabe 2c – Fehlverhalten durch `data()` + `append()`
```cpp
int main() {
    string s("hallo ");
    char* data = s.data();
    s.append("Welt!");
    data[0] = 'H';
    s.print();
}
```
- Erklären, was schiefgeht (Stichwort: `realloc` kann Block verschieben → dangling pointer).
- Als **Kommentar in der Klasse** für Nutzer dokumentieren.

#### Aufgabe 2d – `string` als Wertparameter
```cpp
void print_string(string s) { s.print(); }
```
- Beobachten (Debugger!), was passiert, wenn in `main()` ein `string` übergeben wird, und warum (Stichwort: Compiler-generierter Copy-Konstruktor, Doppelfreigabe).
- Klasse muss **nicht** repariert werden. Release-Optimierung kann das Verhalten verdecken.

> **Aufgabe 2a (Ü4)** ist Analyse/Codevorschlag zu `has_point` (Stichwort: `strlen` in der Schleifenbedingung) und gehört eher zur Theorie.

#### Aufgabe 3a – Mehrstufiges 3D-Array (Codefragment)
- Codefragment (C++), das Speicherblöcke für ein **mehrstufiges** 3D-`bool`-Array (Größe `sx × sy × sz`) allokiert und an einen Zeiger `data` auf dem Stack bindet (`bool*** data`). Kein Initialisieren/Freigeben nötig.
- Dazu auch die Umrechnungsformeln für das **linearisierte** Array: Punkt `p = (px, py, pz)` → Index `i` und zurück `i` → `p`.

#### Aufgabe 3b – Klasse `int_vector`  ⟶ *Grundlage für Ü5 2a und Ü6*
Funktionen:
- Default-Konstruktor (leeres Array), Copy-Konstruktor
- `at` (liefert Alias auf Eintrag), `size`
- `contains` (Integer enthalten?), `find` (Index eines Integers)
- `push_back`, `pop_back`
- `insert` (an Index, Reihenfolge der vorhandenen Elemente bleibt)
- `remove` (an Index, Reihenfolge der übrigen Elemente bleibt)
- `clear`
- Destruktor nach Konventionen
- Code angemessen dokumentieren.

#### Aufgabe 3c – Tests für `int_vector`
- `main`, die Operationen in Folge ausführt, deren Ergebnisarray man vorab kennt; Ergebnis vergleichen.
- Mit weiteren Operationen/Eingaben wiederholen.

---

### Übung 5 – Container

> Theorie-Hinweis aus **Ü5 1a**: Template-Methoden außerhalb der Klasse müssen in jedem Fall für den Linker sichtbar sein → Definitionen gehören in den **Header** (oder innerhalb der Klasse). Hilfreich für 2a.

#### Aufgabe 2a – `int_vector` → `template vector<T>`  *(baut auf Ü4 3b)*
- Nur **minimal nötige** Änderungen am Grundkonzept (weiter `malloc`).
- Ergebnis umbenennen in `vector`.
- `main` zum Testen erweitern.

#### Aufgabe 2b – `std::string` im `vector`
- Prüfen, ob `std::string` einfügbar ist. Falls nicht: warum nicht (Stichwort: `malloc` konstruiert keine Objekte), und korrigieren.
- Weiterhin `malloc` für Speicher; `new` höchstens **zusätzlich** (Stichwort: Placement-new, expliziter Destruktoraufruf).

#### Aufgabe 2c – `vector_iterator`
- `*` und `->` (nach Vorlesung)
- `++` und `--`
- `[offset]` relativ zum aktuellen Eintrag
- `vector::begin()` und `vector::end()` (One-Past-the-End)
- In `main` testen.

#### Aufgabe 2d – Iterator-Kategorie
- Eingeordnet nach Vorlesung (Input/Output/Forward/Bidirectional/Random Access). Begründen anhand der Operationen aus 2c (`[offset]` deutet auf Random Access hin).

#### Aufgabe 2e – 2c in einer einzigen, einfachen Zeile
- Keine Tricks (nicht „alles in eine Zeile schreiben“); richtige Idee gesucht (naheliegend: Zeiger als Iterator, z. B. `using vector_iterator = T*;`).

---

### Übung 6 – Sequentielle Container

> Mit „Array der Vorübungen“ ist euer `vector` (Ü4 3b / Ü5 2a) gemeint, mit „Liste/Häschenkette der Vorübungen“ euer `stall` (Ü3 2e).

#### Aufgabe 2a – Häschenkette → generische Liste  *(baut auf Ü3 2e)*
- Datentyp **zur Compilezeit wählbar** (Template).
- Klassen für **Iterator** und **Listenknoten** ergänzen, falls noch nicht vorhanden.

#### Aufgabe 2b – Einfügen/Löschen
Sofern noch nicht geschehen:
- Einfügen ins **Array** (Ü4 3b `insert`)
- Löschen aus dem **Array** (Ü4 3b `remove`)
- Einfügen in die **Liste**
- Löschen aus der **Liste**

#### Aufgabe 2c – `heapify`
- Funktion `heapify`: nimmt Array (eigener Typ) an und richtet **Max-Heap**-Struktur ein.
- Hilfsfunktion `sift_up` empfohlen; Wrapper-Klasse `heap` (mit eigener, array-unabhängiger Größe) optional hilfreich.
- Test: zufällige Heaps erzeugen; Hilfsfunktion **`check_heap`** prüft, ob jeder innere Knoten die Heap-Eigenschaft erfüllt.

#### Aufgabe 2d – `extract_max`
- Parameter: als Heap aufgebautes Array; Wurzel entfernen, Heap-Struktur erhalten.
- Aktuelle Heap-Größe in **separater Variable** halten (Array nicht verkleinern, nur den Heap).
- Test in `main`.

#### Aufgabe 2e – `heap_sort`
- Array nach dem Verfahren der Vorlesung sortieren (Ü6 1i: absteigend; die Praxisaufgabe nennt keine Richtung).
- Test in `main`.

#### Aufgabe 2f – `binary_search`
- Auf **sortiertem** Array prüfen, ob ein Wert enthalten ist (Verfahren der Vorlesung).

#### Aufgabe 2g – `fifo_queue`
- Queue-Funktionalität **ohne eigene Container-Implementierung**; stattdessen die eigene **Listenklasse** nutzen (Komposition).

#### Aufgabe 2h – Laufzeitmessung Suche
Suche messen in:
- unsortiertem **Array**
- unsortierter **Liste**
- unsortiertem **Heap**

Bedingungen: hinreichend und **gleich große** Datenstrukturen, **zufälliger, aber gleicher** Inhalt. Frage: Lassen sich die Laufzeitergebnisse aus der Vorlesung bestätigen?

---

## 4. Wiederverwendungs-Checkliste („Was muss ich aufbewahren?“)

| Artefakt | Entsteht in | Wird gebraucht in |
|---|---|---|
| `rabbit`, `stall` (Kette per Zeiger) | Ü3 2d/2e | Ü6 2a (Umbau zur Liste) |
| `string` (malloc/realloc/free) | Ü4 2b | Ü4 2c/2d, Ü5 2b (als Testtyp, `std::string` im `vector`) |
| `int_vector` | Ü4 3b | Ü5 2a (→ Template) |
| `vector<T>` + `vector_iterator` | Ü5 2a–2c | Ü6 2b, 2c, 2d, 2e, 2f, 2h |
| generische Liste + Iterator + Knoten | Ü6 2a | Ü6 2b, 2g, 2h |
| `sift_up`, `heapify`, `check_heap`, `heap` | Ü6 2c | Ü6 2d, 2e, 2h |
| `extract_max` | Ü6 2d | Ü6 2e |
| sortiertes Array (via `heap_sort`) | Ü6 2e | Ü6 2f |

**Hinweis:** Konkrete Details, die später wichtig werden:
1. `vector` muss mit `malloc` arbeiten und trotzdem Klassentypen (`std::string`) korrekt unterstützen (Ü5 2b).
2. Der Heap in Ü6 arbeitet auf dem **selbstgeschriebenen Array** mit separater Heap-Größe.
3. Die Liste aus Ü6 2a ersetzt die händische Hasenkette; Iterator und Knoten sind eigene Klassen.

# Algorithmen und Datenstrukturen – Praxisaufgaben (Originaltext, nach Zusammengehörigkeit)

Die Aufgabentexte sind unverändert aus den Übungsblättern übernommen (nur Seitenköpfe entfernt). Es stehen nur Implementierungsaufgaben darin, keine Theoriefragen.

Quellen: **Ü3** = Objektorientierte Programmierung, **Ü4** = Arrays, **Ü5** = Container, **Ü6** = Sequentielle Container.

---

# Strang A: Hase → Stall → Liste → Queue

## Ü3, Aufgabe 2d

d) Schreiben Sie eine Klasse rabbit für niedliche Häschen. Ein rabbit hat folgende Eigenschaften:
• einen Namen, gespeichert als std::string
• eine Ganzzahl für die Anzahl an Ohren, die der Hase hat
• ein Alter in Wochen als Ganzzahl
• ein Gewicht in Gramm als Gleitkommazahl
• einen Wahrheitswert, ob der Hase aktuell essbar ist
• Ein rabbit lässt sich mit gegebenem Namen und gegebener Ohrenzahl anlegen. Anfänglich wiegt der Hase 100 Gramm und er ist 0 Wochen alt.
• Es gibt eine Funktion altern(), die das Alter des Hasen um 1 Woche erhöht.
• Es gibt eine Funktion füttern(), welche das Gewicht des Hasen um eine zufällige Zahl zwischen 10 und 200 erhöht.
• Der Wahrheitswert essbar ist wahr, wenn das Alter zwischen 9 und 12 Wochen und das Gewicht zwischen 1500 und 2000 Gramm liegt. Der Wert soll ständig mit dem Alter und dem Gewicht des Hasen zusammenpassen. Man kann den Wert von außen abfragen, aber nicht verändern.

Schreiben Sie eine main-Funktion, um Ihre Hasenklasse zu testen. Legen Sie ein paar Hasen mit Beispieldaten an, lassen Sie diese altern, und prüfen Sie, ob die Hasen korrekt essbar werden.

## Ü3, Aufgabe 2e

e) Erweitern Sie zunächst die rabbit-Klasse so, dass Hasen sich an der Hand halten können (vgl. ausgeschnittene Häschenkette): Zum Händchenhalten hat jeder Hase eine rechte und eine linke Hand, wobei an der rechten wie an der linken Hand jeweils ein anderer Hase oder kein Hase hängen kann.

Schreiben Sie weiterhin eine Klasse stall, für einen Ort an dem Ihre Hasen glücklich leben können:
• Im Stall halten sich die Hasen in einer durchgehenden Kette an der Hand. Es gibt also einen ersten Hasen, der keinen Hasen an seiner linken Hand hat, und einen letzten Hasen, der keinen Hasen an seiner rechten Hand hat. Alle anderen Hasen haben einen Partner an der linken und der rechten Hand.
• Der Stall selbst merkt sich nur den ersten Hasen in der Kette.
• Der Stall hat eine Funktion hinzufügen, die einen neuen Hasen anlegt und an die bestehende Häschenkette hinten anhängt. Das heißt also, dass der (vormals) letzte Hase einen neuen Partner für seine rechte Hand bekommt. Der neu angelegte Hase hat eine leere rechte Hand.
• Der Stall hat eine Funktion züchten, die alle Hasen altern lässt und füttert.
• Der Stall hat eine Funktion ernten. Diese Funktion geht alle Hasen durch. Wenn ein Hase essbar ist, wird der Hase aus dem Stall entfernt. Wenn ein Hase älter als 50 Wochen ist, wird der Hase ebenfalls entfernt.
• Es gibt eine Funktion inventarisieren. Diese Funktion geht alle Hasen im Stall durch und gibt deren Daten auf der Kommandozeile aus.

Testen Sie Ihren stall wie folgt: Fügen Sie ein paar Hasen in den Stall ein. Züchten und ernten Sie die Hasen abwechselnd, bis der Stall leer ist. Geben Sie nach jedem Schritt per prüfen den Zustand des Stalls aus.

## Ü6, Aufgabe 2a

a) Wandeln Sie Ihre Häschenkette aus den Vorübungen in eine Liste um, die Daten von einem zur Compilezeit wählbaren Typen vorhält. Ergänzen Sie, so noch nicht geschehen, Klassen für einen Iterator und für einen Listenknoten.

## Ü6, Aufgabe 2g

g) Schreiben Sie eine Klasse fifo_queue. Diese soll die Funktionalität einer Queue zur Verfügung stellen, ohne dabei eine eigene Container-Implementierung zu enthalten. Nutzen Sie stattdessen Ihre eigene Listenklasse aus den Vorübungen.

---

# Strang B: int_vector → vector\<T\> → Iterator → Heap → Sortieren → Suchen

## Ü4, Aufgabe 3b

b) Schreiben Sie eine Klasse int_vector für ein Array aus int-Zahlen.

Die Klasse soll folgende Funktionen bieten:
• Default-Konstruktor für ein leeres Array
• Copy-Konstruktor für ein bestehendes Array
• Funktion at, welche ein Alias für einen Eintrag an einem bestimmten Index zurückliefert
• Funktion size, welche die Größe des Arrays zurückgibt
• Funktion contains, die prüft, ob ein gegebener Integer im Array enthalten ist
• Funktion find, die zurückgibt, an welchem Index ein Integer im Array is
• Funktion push_back zum Einfügen eines ints am Ende des Arrays
• Funktion pop_back zum Entfernen eines ints am Ende des Arrays
• Funktion insert zum Einfügen eines ints an einem gegebenen Index, wobei die Reihenfolge der bestehenden Elemente erhalten bleibt (nicht deren Indizes, logischerweise)
• Funktion remove zum Löschen eines ints an einem gegebenen Index, wobei die Reihenfolge der verbleibenden Elemente erhalten bleibt (nicht deren Indizes, logischerweise)
• Funktion clear, die alle Einträge löscht
• Destruktor nach Konventionen

Dokumentieren Sie Ihren Code, wie Ihnen das angemessen erscheint. Achten Sie darauf, dass die Mischung aus Code und Kommentaren gut lesbar und verständlich ausfällt.

## Ü4, Aufgabe 3c

c) Schreiben Sie eine main-Methode, um Ihren int_vector ausgiebig zu testen. Führen Sie einige Operationen in Folge aus, so dass Sie das Ergebnisarray bereits kennen. Prüfen Sie, ob das Ergebnis von Ihrem Code ebenfalls ermittelt wird. Wiederholen Sie das für ein paar weitere Operationen bzw. Eingaben für die Funktionen.

## Ü5, Aufgabe 2a

a) Stellen Sie Ihren int_vector aus dem vorherigen Übungsblatt zu einer template um, so dass der int_vector Einträge von beliebigen Typen T enthalten kann. Sie sollen dazu nur minimal nötige Änderungen am Grundkonzept der Klasse vornemen (z. B. weiter mit malloc Speicher allokieren). Benennen Sie das Ergebnis aber als Vorlage vector statt int_vector.

Erweitern Sie Ihre main, um den vector zu testen.

Hinweis: Die Teilaufgabe zur Implementierung von Template-Methoden von oben ist für diese Aufgabe vermutlich hilfreich!

## Ü5, Aufgabe 2b

b) Prüfen Sie, ob Sie in Ihren selbst-geschriebenen vector auch std::strings einfügen können. Falls nein: Warum funktioniert es nicht? Korrigieren Sie Ihren vector mit geeigneten Mitteln nach, bleiben Sie aber weiterhin bei der Verwaltung von Speicher mittels malloc. Sie dürfen new höchstens zusätzlich verwenden.

## Ü5, Aufgabe 2c

c) Erweitern Sie Ihren vector um einen vector_iterator. Diese Klasse soll folgende Funktionen bieten:
• Zugriff auf einen aktuellen Eintrag mittels * sowie -> nach Vorlesung.
• Weiterzählen und Zurückzählen mit ++ und --.
• Zugriff auf einen Array-Eintrag mittels [offset], wobei offset relativ zum aktuellen Eintrag des Iterators gewertet wird.
• Abfrage von Iteratoren zum Anfang des vectors per begin() und für One-Past-End des vectors mittels end().

Prüfen Sie in der main, ob der vector_iterator funktioniert.

## Ü5, Aufgabe 2e

e) Lösen Sie die Teilaufgabe 2c) in einer einzigen, einfachen Codezeile.

Hinweis: Hier braucht man die richtige Idee. Tricks (z. B. einfach allen Code in eine einzige Zeile zu schreiben) sind nicht zulässig.

## Ü6, Aufgabe 2c

c) Schreiben Sie eine Funktion heapify. Diese Funktion soll ein Array von Ihrem selbstgeschriebenen Arraytypen aus den Vorgängerübungen annehmen und auf diesem Array eine Heapstruktur für einen Max-Heap einrichten.

Es mag helfen, für die heapify-Funktion eine Hilfsfunktion sift_up zu erstellen. Es könnte ebenfalls hilfreich sein, eine Klasse heap als Wrapper für das Array aus den Vorübungen zu programmieren (also mit eigener, array-unabhängiger Größe).

Testen Sie Ihre Funktion heapify mit einer geeigneten main. Erstellen Sie zufällige Heaps und prüfen Sie mit einer weiteren Hilfsfunktion, check_heap, ob jeder Eintrag in inneren Knoten in den Ergebnisheaps die Heap-Eigenschaft erfüllt.

## Ü6, Aufgabe 2d

d) Schreiben Sie eine Funktion extract_max. Diese Funktion soll als Parameter ein als Heap aufgebautes Array annehmen und aus dem Array die Wurzel entfernen, wobei die Heapstruktur erhalten bleibt. Halten Sie die aktuelle Größe des Heaps in einer gesonderten Variablen (d. h. machen Sie bei extract_max nicht das Array kleiner, sondern nur den Heap).

Testen Sie Ihren Code in einer geeigneten main-Funktion.

## Ü6, Aufgabe 2e

e) Schreiben Sie eine Funktion heap_sort, welche ein gegebenes Array mit dem Verfahren aus der Vorlesung sortiert.

Testen Sie Ihren Code in einer geeigneten main-Funktion.

## Ü6, Aufgabe 2f

f) Schreiben Sie eine Funktion binary_search, welche auf einem sortierten Array mit dem Verfahren aus der Vorlesung prüft, ob ein bestimmter Wert enthalten ist.

---

# Strang C: Zusammenführung Array + Liste (Ü6)

Diese zwei Aufgaben betreffen sowohl Strang A (Liste) als auch Strang B (Array, Heap).

## Ü6, Aufgabe 2b

b) Schreiben Sie, sofern noch nicht geschehen:
• eine Funktion zum Einfügen in das Array der Vorübungen
• eine Funktion zum Löschen aus dem Array der Vorübungen
• eine Funktion zum Einfügen in die Liste der Vorübungen
• eine Funktion zum Löschen in der Liste der Vorübungen

## Ü6, Aufgabe 2h

h) Messen Sie, wie lange auf Ihrem Rechner das Suchen...
• ... in einem unsortierten Array,
• ... in einer unsortierten Liste und
• ... in einem unsortierten Heap
braucht. Achten Sie darauf, die Datenstrukturen hinreichend (aber gleich) groß und mit zufälligem (aber gleichem) Inhalt zu wählen. Können Sie die Laufzeitergebnisse aus der Vorlesung bestätigen?

---

# Strang D: string-Klasse

## Ü4, Aufgabe 2b

b) Schreiben Sie eine Klasse string mit nachfolgenden Funktionen.
• string::string()
Konstruktion eines Strings mit einer Kopie der festen Zeichenkette "".
• string::string(const char* data)
Konstruktion aus einem data-Zeiger auf eine Zeichenkette. Internes Speichern einer Kopie der eingehenden Zeichenkette.
Welche Voraussetzung muss die Zeichenkette data erfüllen, damit dieser Konstruktor funktioniert? Was passiert, wenn data ein nullptr ist?
• char* string::data()
Abfrage der aktuell gespeicherten Zeichenkette.
Kann diese Funktion nullptr zurückgeben?
• void string::clear()
Löschen der gespeicherten Zeichenkette.
Überlegen Sie in diesem Zusammenhang, was der Unterschied zwischen nullptr-Daten und einem leeren String "" ist. Welche dieser beiden Varianten ist als Ergebnis der clear()-Methode sinnvoll?
• void string::print()
Ausgeben der aktuellen Zeichenkette.
• int string::find(char c)
Finden eines Zeichens c in der aktuellen Zeichenkette. Rückgabewert sollte der Index des Zeichens im String sein.
Was passiert, wenn das Zeichen nicht gefunden wird?
• void string::append(const char* data)
Anhängen einer weiteren Zeichenkette an den bestehenden String.
• string::~string()
Destruktor. Löschen der gespeicherten Zeichenkette.
Genügt hier ein Aufruf der Memberfunktion clear()?

Verwenden Sie intern nur malloc(), realloc() und free(), um die string-Zeichen zu verwalten. Nutzen Sie kein strlen, kein strcpy und kein memcpy. Ebenfalls nicht erlaubt ist die Verwendung von Hilfsklassen (z. B. std::vector, std::string, …) zum internen Speichern der Zeichenkette. Für die Ausgabe darf aber die Standard-Bibliothek iostream verwendet werden.

Achten Sie auf eine passende Aufteilung in Header- und Quelldatei. Dokumentieren Sie Ihre Klasse. Relevant sind für den Klassennutzer interessante Spezialfälle.

Testen Sie alle Funktionen Ihrer string-Klasse in einer main-Methode. Testwürdig sind insbesondere Spezial- und Randfälle (z. B. nullptr-Eingaben, Suche nach dem Zeichen \0).

Hinweise:
• Die Fragen bei den einzelnen Punkten der Implementierung sollen Sie beim Programmieren anleiten. Sie müssen diese Fragen nicht explizit beantworten.
• Die string-Klasse wird in den nachfolgenden Übungsblättern noch erweitert. Es empfiehlt sich daher, den Code gut aufzubereiten und sicher abzulegen.

---

# Strang E: int_smart_pointer

## Ü3, Aufgabe 2b

b) Erstellen Sie eine Klasse int_smart_pointer mit folgenden Eigenschaften:
• Jeder int_smart_pointer hat immer einen zugeordneten int als Allokation auf dem Heap liegen.
• Der int_smart_pointer merkt sich intern, wo der int auf dem Heap liegt.
• Von außerhalb des int_smart_pointer lässt sich der int mit Methoden set und get auslesen und verändern, aber weder löschen noch neu anlegen.
• Man kann beim Anlegen einer Instanz von int_smart_pointer den Anfangswert des ints vorgeben, sonst wird als Wert 0 genommen.
• Wenn man einen int_smart_pointer kopiert, ist das Kopieren tief: der neue int_smart_pointer hat automatisch eine neue Heap-Allokation, der darin gespeicherte int bekommt den selben Wert wie der Quell-int.
• Wenn ein int_smart_pointer gelöscht wird, gibt es kein Speicherleck.
• Alle Operationen auf int_smart_pointer schreiben auf die Kommandozeile, dass die jeweilige Operation gerade läuft (d. h. die Methoden geben den jeweils eigenen Namen aus).

Prüfen Sie an folgenden Codezeilen, ob int_smart_pointer korrekt funktioniert:

```cpp
int_smart_pointer a;
std::cout << a.get() << std::endl; // Ausgabe 0
a.set(5);
std::cout << a.get() << std::endl; // Ausgabe 5
int_smart_pointer b(10);
std::cout << b.get() << std::endl; // Ausgabe 10
int_smart_pointer c(b);
std::cout << c.get() << std::endl; // Ausgabe 10
c.set(20);
std::cout << b.get() << std::endl; // Ausgabe 10
std::cout << c.get() << std::endl; // Ausgabe 20
```

## Ü3, Aufgabe 2c

c) Passen Sie den Code der vorigen Aufgabe an: Wenn man den int_smart_pointer kopiert, soll die Kopie flach erfolgen, also den selben (d. h. identischen) int wie das Original verwenden. Was geht jetzt schief? Prüfen Sie ggf. mit den obigen Codezeilen, beachten Sie aber, dass sich der Fehler nicht unbedingt äußern muss.

---

# Strang F: window-Deklarationen (eigenständig)

## Ü3, Aufgabe 2a

a) In einer GUI kann ein Fensterelement der Klasse window auf Basis verschiedener Ausgangsdaten erzeugt werden. Geben Sie geeignete Deklarationen für (sinnvoll überladene und benannte) Methoden an, die das Hauptfenster aus den gegebenen Daten erzeugen. Beachten Sie, dass Konstruktoren auch Methoden sind.
• ein leeres Hauptfenster mit Standardeigenschaften
• ein Hauptfenster mit einer bestimmten Größe in X- und Y-Richtung
• ein Hauptfenster mit einer bestimmten Überschrift
• ein Fenster, das innerhalb eines Elternfensters angezeigt wird
• ein Hauptfenster, das beliebig viele gegebene Kindfenster besitzt
• ein Fenster, dessen Eigenschaften und Kindfenster aus einer Ressourcendatei mit angegebenem Pfad geladen werden