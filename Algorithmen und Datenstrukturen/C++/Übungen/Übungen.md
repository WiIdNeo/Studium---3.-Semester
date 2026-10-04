# C++ lernen: Programmieraufgaben

**Ziel:** C++ mit seinen Eigenheiten und seiner Syntax kennenlernen, indem man Dinge baut, die funktionieren.

**Arbeitsweise:**
- Du implementierst die Aufgabe, ich schaue mit dir drüber, und wir besprechen, wie und ob es besser ginge (Stil, Idiome, Performance, Lesbarkeit).
- Standard: **C++20**, Compiler z. B. `g++ -std=c++20 -Wall -Wextra -O2`.
- Jede Aufgabe hat: *Beschreibung*, *Anforderungen*, *Geübte Konzepte* und *Diskussionsfragen* für unser Gespräch.
- Der Schwierigkeitsgrad steigt an. Du kannst auch Aufgaben überspringen oder umsortieren.

---

## Teil 1: Grundlagen

### Aufgabe 1: Temperaturtabelle

**Beschreibung:** Gib eine Tabelle aus, die Celsius- in Fahrenheit-Werte umrechnet.

**Anforderungen:**
- Bereich von -20 °C bis 40 °C in 5er-Schritten.
- Spalten sauber ausgerichtet, eine Nachkommastelle.
- Die Umrechnung steckt in einer eigenen Funktion.

**Konzepte:** `#include`, `main`, `for`-Schleife, Funktionen, `<iostream>`, `<iomanip>` (`std::setw`, `std::fixed`, `std::setprecision`), `double`

**Diskussion:** `std::cout` vs. `std::format` bzw. `std::print` (C++20/23). `int` oder `double` für die Schleifenvariable?

---

### Aufgabe 2: Zahlen einlesen und auswerten

**Beschreibung:** Das Programm liest beliebig viele Zahlen von der Standardeingabe (bis EOF) und gibt Anzahl, Summe, Mittelwert, Minimum und Maximum aus.

**Anforderungen:**
- Die Zahlen werden in einem `std::vector<double>` gespeichert.
- Bei leerer Eingabe eine sinnvolle Meldung statt Berechnung.
- Die Auswertung steckt in einer Funktion, die einen kleinen `struct` zurückgibt.

**Konzepte:** `std::vector`, `std::cin` in Schleifenbedingung, `struct`, Rückgabe per Wert, `<algorithm>` (`std::minmax_element`), `<numeric>` (`std::accumulate`)

**Diskussion:** Wann `auto`? Warum `const std::vector<double>&` als Parameter? Struct vs. `std::pair`/`std::tuple`?

---

### Aufgabe 3: Primzahlsieb

**Beschreibung:** Implementiere das Sieb des Eratosthenes und gib alle Primzahlen bis `n` aus.

**Anforderungen:**
- `n` kommt von der Kommandozeile (`argc`/`argv`).
- Das Sieb nutzt einen `std::vector<bool>`.
- Ausgabe: Primzahlen, 10 pro Zeile.

**Konzepte:** `argc`/`argv`, `std::stoul`, `std::vector<bool>`, Typen mit fester Breite, `std::size_t`

**Diskussion:** Die Besonderheit von `vector<bool>`. `std::size_t` vs. `int` bei Indizes. Welche Obergrenze für `n` ist sinnvoll?

---

### Aufgabe 4: Wörter zählen

**Beschreibung:** Lies einen Text aus einer Datei und gib die 10 häufigsten Wörter mit ihrer Häufigkeit aus.

**Anforderungen:**
- Dateiname per Kommandozeile.
- Groß-/Kleinschreibung ignorieren, Satzzeichen entfernen.
- Sortierte Ausgabe (absteigend nach Häufigkeit, bei Gleichstand alphabetisch).

**Konzepte:** `std::ifstream`, `std::string`, `std::unordered_map` bzw. `std::map`, `std::sort` mit Lambda, Structured Bindings (`auto [wort, anzahl]`), `std::tolower`/`std::isalpha`

**Diskussion:** `map` vs. `unordered_map`. Bereichs-`for` mit Structured Bindings. Probleme von `std::tolower` mit `char` (Stichwort `unsigned char`) und mit UTF-8.

---

## Teil 2: Referenzen, Zeiger, `const`

### Aufgabe 5: Swap und Rotation

**Beschreibung:** Schreibe eigene Funktionen `mein_swap` und `rotiere_links`, die auf Werten bzw. Containern arbeiten.

**Anforderungen:**
- `mein_swap(int&, int&)` tauscht zwei Zahlen.
- `rotiere_links(std::vector<int>&, std::size_t k)` rotiert die Elemente um `k` Positionen nach links, ohne einen zweiten Vektor anzulegen.
- Mache beide Funktionen generisch (Templates) in einer zweiten Version.

**Konzepte:** Referenzen als Parameter, Templates (Funktionstemplates), `std::reverse`, Modulo-Arithmetik

**Diskussion:** Warum ist `std::swap` und `std::rotate` in der Standardbibliothek besser? Was heißt „In-place“?

---

### Aufgabe 6: Const-Korrektheit an einer Matrix-Klasse

**Beschreibung:** Eine einfache Klasse `Matrix` für `double`-Werte mit fester Größe zur Laufzeit.

**Anforderungen:**
- Konstruktor `Matrix(rows, cols)`, Elemente mit 0 initialisiert.
- Elementzugriff über `operator()(row, col)` in einer lesenden (`const`) und einer schreibenden Variante.
- `rows()`, `cols()` als `const`-Memberfunktionen.
- Intern ein einziger `std::vector<double>` (zeilenweise).
- Funktion `Matrix transponiert(const Matrix&)`.
- `operator<<` zum Ausgeben.

**Konzepte:** Klassen, Konstruktoren, Initialisierungsliste, `const`-Memberfunktionen, Operatorüberladung, `friend` oder freie Funktion, `explicit`

**Diskussion:** Warum zwei Überladungen von `operator()`? Flaches Array vs. `vector<vector<double>>`. C++23 `operator[]` mit mehreren Argumenten?

---

### Aufgabe 7: Zeiger lesen können: eine einfach verkettete Liste

**Beschreibung:** Baue eine eigene einfach verkettete Liste für `int` mit Rohzeigern, um zu verstehen, wie Knoten und Zeiger zusammenspielen.

**Anforderungen:**
- Operationen: `push_front`, `push_back`, `size`, `contains`, `reverse` (in-place), Ausgabe.
- Sauberes Aufräumen im Destruktor.
- Kopieren und Verschieben werden **korrekt** unterstützt (Rule of Five).

**Konzepte:** `new`/`delete`, `nullptr`, Zeiger auf Zeiger oder Hilfszeiger, Destruktor, Kopierkonstruktor, Kopierzuweisung, Move-Konstruktor, Move-Zuweisung, `noexcept`, Copy-and-Swap

**Diskussion:** Wie sähe das mit `std::unique_ptr` aus? Warum ist `std::list`/`std::forward_list` meist die bessere Wahl? Was bringt Copy-and-Swap?

---

## Teil 3: RAII und Ressourcenverwaltung

### Aufgabe 8: Datei-Wrapper mit RAII

**Beschreibung:** Eine Klasse `Datei`, die eine C-Datei (`FILE*`) besitzt und im Destruktor schließt.

**Anforderungen:**
- Öffnen im Konstruktor (Pfad, Modus), Fehler beim Öffnen sauber melden (Exception).
- Methoden `zeile_lesen()` und `schreiben(std::string_view)`.
- Nicht kopierbar, aber verschiebbar.

**Konzepte:** RAII, `= delete`, Move-Semantik, `std::string_view`, Exceptions (`std::runtime_error`), `<cstdio>`

**Diskussion:** Warum ist RAII das zentrale Idiom von C++? Wann würdest du doch `std::fstream` nehmen? Alternative: `std::unique_ptr<FILE, Deleter>`.

---

### Aufgabe 9: Ressourcen mit Smart Pointern

**Beschreibung:** Modelliere eine kleine Spielwelt: `Entity` (Basisklasse) mit abgeleiteten Klassen `Spieler`, `Gegner`, `Gegenstand`.

**Anforderungen:**
- Die Welt (`class Welt`) besitzt alle Entitäten über `std::unique_ptr<Entity>` in einem `std::vector`.
- Virtuelle Methode `update(double dt)` und `beschreibe() const`.
- Ein `Gegner` hält eine **nicht besitzende** Referenz auf sein Ziel (`Entity*` oder `std::weak_ptr`), je nach deiner Designentscheidung.
- Funktion `std::unique_ptr<Entity> erzeuge(std::string_view typ)` als einfache Factory.

**Konzepte:** Vererbung, `virtual`, `override`, virtueller Destruktor, `std::unique_ptr`, `std::make_unique`, `std::move`, Factory-Muster

**Diskussion:** Besitz vs. Beobachtung. `shared_ptr` nur bei echtem geteilten Besitz. Alternative zu Vererbung: `std::variant` (siehe Teil 5).

---

### Aufgabe 10: Scope-Guard

**Beschreibung:** Baue eine kleine Hilfsklasse `ScopeExit`, die beim Verlassen des Gültigkeitsbereichs eine übergebene Funktion aufruft.

**Anforderungen:**
- Funktioniert mit Lambdas.
- Methode `abbrechen()` (dismiss), damit die Aktion nicht ausgeführt wird.
- Nicht kopierbar.
- Demo: Ein Programm, das eine Ressource öffnet und sie über `ScopeExit` wieder freigibt.

**Konzepte:** Klassentemplates, Template-Argumentableitung (CTAD), Lambdas, `std::function` vs. Template-Parameter, Destruktoren

**Diskussion:** Warum ein Template statt `std::function`? Was kostet `std::function`?

---

## Teil 4: Templates und generische Programmierung

### Aufgabe 11: Eigener `Stack<T>`

**Beschreibung:** Ein generischer Stack mit dynamischem Speicher, ohne `std::vector` als Basis.

**Anforderungen:**
- `push`, `pop`, `top`, `empty`, `size`, Kapazitätswachstum (verdoppeln).
- Funktioniert für Typen wie `int`, `std::string` und für nur verschiebbare Typen (`std::unique_ptr<int>`).
- `emplace`, das ein Objekt direkt im Speicher konstruiert.
- Rule of Five.

**Konzepte:** Klassentemplates, `std::allocator` bzw. Placement-new, perfekte Weiterleitung (`std::forward`), variadische Templates, `std::move_if_noexcept`

**Diskussion:** Lohnt sich Handarbeit gegenüber `std::stack`? Rolle von `noexcept` beim Umkopieren während des Wachsens.

---

### Aufgabe 12: Generische Algorithmen

**Beschreibung:** Implementiere eigene Versionen einiger Standardalgorithmen, die mit beliebigen Iteratoren arbeiten.

**Anforderungen:**
- `meine_find_if(first, last, pred)`
- `meine_transform(first, last, out, f)`
- `meine_accumulate(first, last, init, op)`
- Alle als Funktionstemplates; teste mit `std::vector`, `std::list` und C-Arrays.
- Zweite Version mit **Concepts** (`std::input_iterator`, `std::predicate`, ...).

**Konzepte:** Iterator-Kategorien, Funktionstemplates, Concepts und `requires` (C++20), Lambdas als Prädikate

**Diskussion:** Was bringen Concepts gegenüber „blankem“ `typename`? Wie lesbar sind Template-Signaturen?

---

### Aufgabe 13: Compile-Zeit-Berechnungen

**Beschreibung:** Berechne Werte zur Übersetzungszeit.

**Anforderungen:**
- `constexpr`-Funktion für Fakultät und Fibonacci.
- `constexpr`-Funktion, die ein `std::array<bool, N>` mit einem Primzahlsieb füllt.
- `static_assert` prüft einige Werte.
- Ein `consteval`-Beispiel (z. B. Berechnung einer Lookup-Tabelle für Sinuswerte).

**Konzepte:** `constexpr`, `consteval`, `static_assert`, `std::array`, Nicht-Typ-Template-Parameter

**Diskussion:** Wann lohnt sich Compile-Zeit-Rechnung? Unterschied `constexpr` vs. `const`.

---

## Teil 5: Moderne Standardbibliothek

### Aufgabe 14: Einfacher Befehlsparser

**Beschreibung:** Ein Programm liest Zeilen wie `add 3 4`, `neg 5`, `help`, `quit` und führt sie aus.

**Anforderungen:**
- Jedes Kommando wird als eigener Typ modelliert; das Ergebnis des Parsens ist ein `std::variant<Add, Neg, Help, Quit>`.
- Ausführung mit `std::visit` und einem Overload-Set aus Lambdas.
- Das Parsen gibt `std::optional<Befehl>` zurück (leer bei unbekanntem Befehl).
- Zeilen werden mit `std::string_view` zerlegt, ohne unnötige Kopien.

**Konzepte:** `std::variant`, `std::visit`, `std::optional`, `std::string_view`, `std::from_chars`, `overloaded`-Hilfsstruktur

**Diskussion:** `variant` + `visit` vs. Vererbung + virtuelle Funktionen. Wann ist `optional` besser als Exceptions?

---

### Aufgabe 15: Inventarverwaltung

**Beschreibung:** Eine kleine Verwaltung für Artikel (Name, Preis, Menge) mit Suche und Sortierung.

**Anforderungen:**
- Speicherung in `std::vector<Artikel>`.
- Funktionen: hinzufügen, nach Name suchen, nach Preis sortieren, Gesamtwert berechnen, Artikel unter einem Mindestbestand filtern.
- Umsetzung mit Standardalgorithmen (`std::ranges::sort`, `std::ranges::find_if`, `std::views::filter`, `std::views::transform`).
- `Artikel` bekommt einen `operator<=>` (Spaceship) für Vergleiche.

**Konzepte:** `<ranges>`, Views und Pipes (`|`), Projektionen, `operator<=>` mit `= default`, Aggregatinitialisierung, Designated Initializers

**Diskussion:** Ranges vs. klassische Iterator-Paare. Lesbarkeit und Lebensdauerfragen bei Views.

---

### Aufgabe 16: Formatierte Ausgabe

**Beschreibung:** Schreibe einen kleinen Bericht-Generator, der eine Tabelle aus Datensätzen formatiert ausgibt.

**Anforderungen:**
- Nutze `std::format` (bzw. `std::print` mit C++23, falls dein Compiler es kann).
- Spaltenbreiten werden aus den Daten berechnet.
- Eigener `std::formatter` für einen selbst definierten Typ (z. B. `Punkt` → `(1.5, 2.0)`).

**Konzepte:** `std::format`, Formatspezifikationen, Spezialisierung von `std::formatter`, Templates

**Diskussion:** `printf` vs. `iostream` vs. `std::format`. Typsicherheit und Performance.

---

## Teil 6: Funktionale Elemente und Lambdas

### Aufgabe 17: Ereignissystem

**Beschreibung:** Ein `EventBus`, bei dem sich beliebige Funktionen für benannte Ereignisse registrieren können.

**Anforderungen:**
- `abonniere(name, callback)` gibt einen Handle zurück, mit dem man sich wieder abmelden kann.
- `sende(name, daten)` ruft alle registrierten Callbacks auf.
- Callbacks können Lambdas (auch mit Captures), freie Funktionen oder Memberfunktionen sein.

**Konzepte:** `std::function`, Lambda-Captures (`[=]`, `[&]`, `[this]`, Init-Captures), `std::unordered_map`, `std::bind_front`

**Diskussion:** Lebensdauer von Captures. Kosten von `std::function`. Alternativen (Templates, `std::move_only_function` ab C++23).

---

### Aufgabe 18: Memoisierung

**Beschreibung:** Eine Funktion `memoize`, die eine beliebige reine Funktion `int -> long long` umhüllt und Ergebnisse zwischenspeichert.

**Anforderungen:**
- Rückgabe ist ein aufrufbares Objekt (Lambda oder Funktor mit Zustand).
- Demo mit rekursiver Fibonacci-Berechnung und Zeitmessung (`<chrono>`) mit und ohne Cache.
- Zweite Variante: verallgemeinert auf beliebige Argumenttypen mit `std::tuple` und variadischen Templates.

**Konzepte:** Lambdas mit Zustand (`mutable`), generische Lambdas (`auto`-Parameter), `<chrono>`, variadische Templates, Hash für Tupel

**Diskussion:** Wie rekursiv ruft sich ein Lambda selbst auf (Deducing `this` in C++23)? Thread-Sicherheit des Caches?

---

## Teil 7: Nebenläufigkeit

### Aufgabe 19: Parallele Summe

**Beschreibung:** Summiere einen großen `std::vector<double>` parallel mit mehreren Threads.

**Anforderungen:**
- Aufteilung in Blöcke, ein Thread pro Block, Ergebnisse werden zusammengeführt.
- Variante A mit `std::thread` und Ergebnisarray, Variante B mit `std::async`/`std::future`.
- Zeitmessung gegen `std::accumulate` und `std::reduce(std::execution::par, ...)`.

**Konzepte:** `std::thread`, `join`, `std::async`, `std::future`, `std::hardware_concurrency`, `<execution>`

**Diskussion:** Ab welcher Datenmenge lohnt sich Parallelisierung? Wie viele Threads sind sinnvoll? Falsches Teilen von Cachelines (False Sharing).

---

### Aufgabe 20: Thread-sichere Warteschlange

**Beschreibung:** Eine Producer-Consumer-Anwendung mit einer eigenen Queue.

**Anforderungen:**
- Klasse `SyncQueue<T>` mit `push` und blockierendem `pop`.
- Mehrere Producer erzeugen Zahlen, mehrere Consumer verarbeiten sie.
- Sauberes Beenden: Die Queue kann geschlossen werden, Consumer beenden sich danach von selbst.
- Nutze `std::jthread` und `std::stop_token`.

**Konzepte:** `std::mutex`, `std::lock_guard`/`std::unique_lock`, `std::condition_variable`, `std::jthread`, `std::stop_token`, RAII für Locks

**Diskussion:** Wie wird die Queue erweitert (maximale Größe, Timeout)? Lock-freie Alternativen und warum man sie meist meidet.

---

## Teil 8: Abschlussprojekte

Wähle eines (oder mehrere) aus, wenn du dich sicher fühlst.

### Projekt A: Mini-JSON-Parser

**Beschreibung:** Parse JSON-Text in eine Baumstruktur und gib ihn wieder aus.

**Anforderungen:**
- Wertetyp mit `std::variant<std::nullptr_t, bool, double, std::string, Array, Object>`.
- Rekursiver Abstiegsparser auf `std::string_view`.
- Fehlerbehandlung über `std::expected` (C++23) oder eigenen Ergebnistyp.
- Ausgabe mit schöner Einrückung.

**Diskussion:** Rekursive Typen mit `variant`. Besitz der Strings (`string_view` vs. `string`). Testen der Funktionalität.

---

### Projekt B: Textadventure-Engine

**Beschreibung:** Räume, Gegenstände und einfache Befehle (`gehe nord`, `nimm schlüssel`, `benutze schlüssel`), die Welt wird aus einer Textdatei geladen.

**Anforderungen:**
- Saubere Klassenhierarchie oder `variant`-Design, deine Wahl, wir diskutieren sie.
- Einlesen der Weltbeschreibung aus Datei.
- Spielstand speichern und laden.

**Diskussion:** Datengetriebenes Design. Wie testet man so etwas?

---

### Projekt C: Bildfilter für PGM/PPM

**Beschreibung:** Lies ein Graustufenbild im PGM-Format (ASCII), wende Filter an (Invertieren, Weichzeichnen, Kantenerkennung) und schreibe das Ergebnis.

**Anforderungen:**
- Klasse `Bild` mit flachem Speicher und Zugriff über `operator()`.
- Filter als austauschbare Funktionsobjekte.
- Parallele Verarbeitung von Zeilen mit `std::for_each(std::execution::par, ...)`.

**Diskussion:** Speicherlayout und Cache-Freundlichkeit. `std::span` für Zeilenansichten.

---

## Hinweise zum Vorgehen

1. Beginne mit Aufgabe 1 und schicke mir deinen Code, sobald er läuft.
2. Beschreibe kurz, wo du unsicher warst oder was du anders hättest lösen können.
3. Wir schauen gemeinsam auf: Korrektheit, Idiomatik („wie würde man das in modernem C++ schreiben?“), Lesbarkeit und Alternativen.
4. Wenn dir eine Aufgabe zu leicht oder zu schwer ist, sag Bescheid, dann passe ich die Reihenfolge oder Tiefe an.