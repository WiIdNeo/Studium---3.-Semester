# Algorithmen und Datenstrukturen – Musterlösung zu Übung 3: Objektorientierte Programmierung

> Alle Codebeispiele sind mit `g++ -std=c++17 -Wall -Wextra` gedacht.
> Hinweis zu Namen: Umlaute in Bezeichnern (`füttern`, `züchten`) sind nicht portabel, daher verwendet die Lösung `fuettern`, `zuechten` usw.

---

## Aufgabe 1: Theorie

### a) `numerics.hpp` / `numerics.cpp` / `main.cpp`

**Was ist das Problem?**

Verletzung der **One-Definition-Rule (ODR)**: Die Struktur `vector` wird in zwei Übersetzungseinheiten *unterschiedlich* definiert.

| Übersetzungseinheit | `PRECISION` | `vector` |
|---|---|---|
| `numerics.cpp` | `double` (Default im Header) | 3 × `double`, `sizeof` = 24 |
| `main.cpp` | `float` (per `#define` vor dem Include) | 3 × `float`, `sizeof` = 12 |

Der Header wirkt in beiden Dateien "gleich", der Präprozessor macht daraus aber zwei verschiedene Typen. Das Programm hat undefiniertes Verhalten (UB), eine Diagnose durch Compiler oder Linker ist laut Standard nicht erforderlich.

**Wie äußert sich das Problem?**

*Allgemein:* Aufrufer und Aufgerufener sind sich über Größe, Ausrichtung und Offsets der Struktur uneinig. Mögliche Folgen sind falsche Werte, überschriebene Nachbarvariablen auf dem Stack, Abstürze (Segfault, Stack-Smashing), oder das Programm läuft scheinbar korrekt und bricht nach einer harmlosen Änderung.

*Vermutlich im Speziellen:*

- `my_vector()` schreibt 3 × `double` mit dem Wert `1234.0` und gibt `1234 1234 1234` aus.
- `main` interpretiert denselben Speicher als 3 × `float`. Die Bytes von `1234.0` als `double` (little endian) sind `00 00 00 00 00 48 93 40`. Als zwei `float` gelesen ergibt das `0x00000000` = **0.0** und `0x40934800` ≈ **4.6025**. Das dritte `float` sind die unteren 4 Bytes des zweiten `double`, also wieder **0.0**.
  Typische Ausgabe in `main`: `0 4.60254 0` statt `1234 1234 1234`.
- Zusätzlich unterscheidet sich oft der Rückgabemechanismus: Auf x86-64 (System V ABI) wird ein 24-Byte-Struct über einen versteckten Speicherzeiger zurückgegeben, ein 12-Byte-Struct aus Floats dagegen in Registern (`xmm0`/`xmm1`). Dann schreibt die Funktion 24 Byte an eine Adresse, die `main` nie bereitgestellt hat (Stack-/Speicherkorruption, Absturz), und `main` liest Register-Restmüll.
- Im Debugger (Speicheransicht von `n`) sieht man genau diese Bytefolge bzw. dass nur 12 statt 24 Byte reserviert sind.

**Warum finden Compiler und Linker das Problem nicht?**

- Der **Compiler** übersetzt jede `.cpp` einzeln. Jede Einheit ist für sich konsistent und korrekt, die andere Einheit sieht er nie.
- Der **Linker** sieht nur Symbole (Namen) in den Objektdateien. Der Name von `my_vector()` (z. B. `_Z9my_vectorv`) enthält weder den Rückgabetyp noch das Layout der Struktur. Beide Objektdateien passen daher namentlich perfekt zusammen. Typdefinitionen stehen nicht in der Objektdatei (allenfalls in Debug-Infos).

**Behebung:** Den Typ nicht per Makro pro Übersetzungseinheit variieren. Stattdessen `PRECISION` einheitlich für das gesamte Projekt über die Compilerflags setzen (`-DPRECISION=float` für alle Dateien), oder den Typ per Template parametrisieren, oder einen festen Typ verwenden. Mit Link-Time-Optimization (GCC: `-flto -Wodr`) lassen sich solche Verstöße teilweise erkennen.

---

### b) Klasse `resource_id`

**Probleme:**

1. **Initialisierungsreihenfolge:** Member werden in *Deklarationsreihenfolge* initialisiert, nicht in der Reihenfolge der Initialisierungsliste. Deklariert ist `full_path` (public, zuerst), dann `base_path_`, dann `file_name_`. `full_path(base_path_ + "/" + file_name_)` greift also auf **noch nicht konstruierte** Member zu, undefiniertes Verhalten (`-Wreorder` warnt nur teilweise).
2. **`base_path_` wird nie initialisiert:** Der Konstruktorparameter `base_path` wird nicht verwendet. `base_path_` ist `const` und wird daher leer default-konstruiert und kann nie mehr gesetzt werden. Selbst bei korrekter Reihenfolge wäre `full_path` = `"/" + file_name_`.
3. Nebenbei: Alle Member sind `const`, die Klasse ist dadurch nicht zuweisbar (hier wohl gewollt).

**Korrektur:**

```cpp
#include <string>

class resource_id
{
public:
    resource_id(const std::string& base_path,
                const std::string& file_title,
                const std::string& extension)
        :
        base_path_(base_path),                        // Reihenfolge wie in der Deklaration!
        file_name_(file_title + "." + extension),
        full_path(base_path_ + "/" + file_name_) { }

private:
    const std::string base_path_;
    const std::string file_name_;

public:
    const std::string full_path;                      // nach den Membern deklarieren, von denen er abhängt
};
```

Alternativ: Reihenfolge belassen und `full_path(base_path + "/" + file_title + "." + extension)` direkt aus den Parametern berechnen. Das ist robust gegen Umsortieren.

---

### c) Unabhängige Fälle

| # | Fall | Ergebnis | Begründung |
|---|---|---|---|
| 1 | Header **definiert** `int a(float, float)` (nicht `inline`), Header in mehreren `.cpp` | **Linker-Fehler** (multiple definition) | Jede `.cpp` enthält die Definition; eine nicht-inline-Funktion darf nur einmal im Programm definiert sein (ODR). Formal UB, praktisch Linker-Fehler. Bei nur *einer* einbindenden `.cpp` wäre es korrekt. Lösung: `inline` oder nur deklarieren. |
| 2 | Header definiert `int b()`, `.cpp` bindet ein und definiert `b()` nochmals | **Compiler-Fehler** | Doppelte Definition innerhalb derselben Übersetzungseinheit (redefinition). |
| 3 | Header deklariert `int c(float)`, zwei `.cpp` mit identischer Definition | **Linker-Fehler** (multiple definition) | Auch identische Definitionen einer nicht-inline-Funktion sind über Dateigrenzen unzulässig. |
| 4 | `d.hpp` deklariert `int d(float)`, `d.cpp` definiert sie, inkludiert `d.hpp` aber nie | **korrekt** (kompiliert, linkt, läuft) | Der Linker koppelt über den Symbolnamen. Deklaration und Definition stimmen überein, also passt es. Riskant: Bei abweichender Signatur gäbe es einen Linker-Fehler (andere Parameter) oder sogar UB (nur anderer Rückgabetyp, da dieser nicht im Symbolnamen steckt). Durch das Einbinden des Headers würde der Compiler die Übereinstimmung prüfen. |
| 5 | Klasse `E` im Header, Methoden **außerhalb** der Klasse (nicht inline) in zwei `.cpp` identisch definiert | **Linker-Fehler** (multiple definition) | Wie Fall 3: Membermethoden außerhalb der Klasse sind normale Funktionen und dürfen nur einmal definiert werden. |
| 6 | Klasse `F` im Header, alle Methoden inline in der Klasse, Header in mehreren `.cpp` | **korrekt** | In-class-definierte Methoden sind implizit `inline`. Mehrfache, *identische* Definitionen in verschiedenen Übersetzungseinheiten sind erlaubt, der Linker behält genau eine Kopie. |
| 7 | Mehrere `.cpp` definieren jeweils **unterschiedliche** Klassen `H`, hängen Instanzen an ein globales `std::unique_ptr<H>` | **undefiniertes Verhalten** (evtl. Linker-Fehler) | ODR-Verstoß: verschiedene Klassen gleichen Namens mit externer Bindung. Implizit erzeugte bzw. inline Funktionen (`~H()`, `std::default_delete<H>::operator()`, `unique_ptr<H>`-Instanziierungen) haben in allen Einheiten denselben Symbolnamen und werden vom Linker zu einer Kopie zusammengeführt. Ergebnis: falscher Destruktor, falsche Größe, Heap-Korruption. Ein gleichnamiges globales Objekt wäre zudem entweder ein Linker-Fehler oder dasselbe Objekt. Abhilfe: unterschiedliche Namen, Namespaces oder anonyme Namespaces. |

---

### d) Alles in der Klasse definieren

**1. Naives Argument für mehr Geschwindigkeit**

In der Klasse definierte Methoden sind implizit `inline`. Der Compiler kann den Funktionskörper an der Aufrufstelle einsetzen. Es fallen weg:

- Vorbereiten der Parameter nach Aufrufkonvention (Register/Stack)
- `call`-Sprung und `ret` (Rücksprungadresse ablegen und wieder laden)
- Aufbau und Abbau des Stackframes (`push rbp`/`pop rbp`, Register sichern und wiederherstellen)
- Der Sprung selbst (Kontrollflusswechsel)

Zusätzlich kann der Optimierer über die Aufrufgrenze hinweg optimieren (Konstanten weiterreichen, tote Berechnungen entfernen).

**2. Warum es in der Praxis oft langsamer wird (Branch Prediction, Caches)**

*Branch Prediction, kurz:* Moderne CPUs arbeiten in einer tiefen Pipeline und laden Befehle spekulativ vor. Bei bedingten Sprüngen wird das Ergebnis *vorhergesagt* (Sprungrichtung über Verlaufstabellen mit 2-Bit-Zählern bzw. Historien, Sprungziele über den Branch Target Buffer, Rücksprünge über einen Return Stack Buffer). Stimmt die Vorhersage, kostet der Sprung fast nichts. Bei einer Fehlvorhersage muss die Pipeline verworfen werden (rund 10–20 Zyklen). Die Vorhersagetabellen sind klein und werden über die Sprungadresse indiziert.

*Warum konsequentes Inlining schadet:*

- **Code-Aufblähung:** Jeder Aufruf erhält eine eigene Kopie des Funktionskörpers. Das Programm wird größer, der Befehls-Cache (L1i, µop-Cache) wird belastet, es gibt mehr Cache-Misses und mehr iTLB-Misses.
- **Mehr Sprungbefehle:** Jede Kopie enthält eigene bedingte Sprünge, die separat vom Prädiktor gelernt werden müssen. Die Tabellen laufen voll bzw. kollidieren (Aliasing), und selten ausgeführte Kopien sind "kalt" und werden häufiger falsch vorhergesagt. Eine gemeinsame, oft ausgeführte Funktion bleibt dagegen im Cache und ihre Sprünge sind gut trainiert.
- **Der gesparte Aufwand ist klein:** Direkte `call`/`ret`-Paare sind auf modernen CPUs sehr gut vorhersagbar und billig. Der Gewinn durch Wegfall ist gering, der Verlust durch Cache-Effekte kann überwiegen.
- Außerdem: längere Übersetzungszeiten, mehr Header-Abhängigkeiten (jede Änderung erzwingt Neuübersetzung aller Nutzer).

`inline` ist ohnehin nur ein Hinweis, der Compiler entscheidet nach eigenen Heuristiken.

**3. Whole Program Optimization (WPO / LTO)**

Beim Kompilieren wird zunächst nur eine Zwischendarstellung erzeugt. Die eigentliche Optimierung und Codeerzeugung geschieht beim Linken über das **gesamte Programm** hinweg (MSVC `/GL` + `/LTCG`, GCC/Clang `-flto`). Dadurch sind u. a. möglich: Inlining über `.cpp`-Grenzen, Entfernen ungenutzter Funktionen, Zusammenfassen identischer Funktionen, Devirtualisierung.

*Einfluss auf das Vorgehen:* Der Compiler kann auch Methoden inlinen, die in einer `.cpp` definiert sind, und entscheidet nach Kosten-Nutzen-Abschätzung, wann sich Inlining lohnt. Das manuelle Erzwingen durch Definition in der Klasse ist damit überflüssig, und es hat nur die Nachteile (Header-Abhängigkeiten, Übersetzungszeit, ODR-Risiko). Die Standardempfehlung bleibt: Deklaration im Header, Definition in der `.cpp`, Optimierung dem Compiler überlassen.

---

### e) Zwei verschiedene Klassen `battery`

**Warum passiert das?**

Beide Definitionen von `battery` haben externe Bindung und den gleichen Namen, das ist ein **ODR-Verstoß** (verschiedene Definitionen derselben Klasse in mehreren Übersetzungseinheiten, keine Diagnose nötig). Der Konstruktor ist in der Klasse definiert, also implizit `inline`. Der Compiler erzeugt (sofern er nicht inlined) in jeder Objektdatei eine eigene Kopie als *schwaches Symbol* bzw. COMDAT mit identischem Namen, z. B. `_ZN7batteryC1Ev`.

**Was macht der Linker?**

Für schwache/COMDAT-Symbole gilt: Sie müssen laut ODR gleich sein, also behält der Linker **genau eine** Kopie und verwirft die anderen. Er prüft das nicht. Das ist dieselbe Optimierung wie beim Zusammenfassen identischer inline-Funktionen und spart Code und Cache-Platz (vgl. 1d, Punkt 2: Code-Duplikate belasten die Caches). Bei "identischen" Definitionen ist das korrekt, hier sind sie aber verschieden.

**Wie äußert sich das UB vermutlich?**

Beide Dateien verwenden denselben Konstruktor, der zuerst gelinkte gewinnt. Ausgabe: Es erscheint z. B. beim Anlegen einer `battery` in `sensor.cpp` trotzdem `robot on` (oder umgekehrt in `robot.cpp` `sensor on`), je nach Linkreihenfolge.

**Warum nur unter speziellen Bedingungen?**

- Bei aktivierter Optimierung (`-O2`) wird der triviale Konstruktor meist an der Aufrufstelle **eingesetzt (inlined)**. Dann existiert kein Aufruf des gemeinsamen Symbols und jede Datei verhält sich scheinbar korrekt.
- Der Fehler zeigt sich typischerweise bei `-O0` (kein Inlining, Konstruktor als schwaches Symbol ausgelagert) oder wenn der Compiler nicht inlined. Der Linker muss die Duplikate außerdem tatsächlich zusammenführen (Standardverhalten bei COMDAT/weak; Identical Code Folding, `/OPT:ICF`, `--icf`, verstärkt das).
- Bei größeren Unterschieden (andere Member, andere Größen) wäre das Ergebnis schlimmer (Heap-/Stack-Korruption).

**Abhilfe:** Klassen mit gleichem Namen in getrennten Namespaces oder anonymen Namespaces (`namespace { class battery {...}; }`) definieren, oder eine gemeinsame Definition im Header verwenden.

---

## Aufgabe 2: Praxis

### a) Deklarationen für `window`

Wichtige Überlegungen:

- Konstruktoren dürfen **nur über Anzahl/Typ der Parameter** überladen werden (nicht über Parameternamen oder Rückgabetyp). Eine Überschrift und ein Ressourcenpfad sind beide `std::string`, daher braucht mindestens eine der Varianten einen eigenen Namen. Die Lösung sind benannte statische Erzeugungsmethoden (*Named Constructors*, `create_...`).
- `window(window& parent)` wäre eine gültige **Copy-Konstruktor-Signatur** und würde beim Kopieren mit dem Konstruktor für "Kindfenster" kollidieren. Deshalb hier eine benannte Methode.
- Einparametrige Konstruktoren als `explicit`, um unbeabsichtigte implizite Konvertierungen zu vermeiden.

```cpp
#include <memory>
#include <string>
#include <vector>

class window
{
public:
    // leeres Hauptfenster mit Standardeigenschaften
    window();

    // Hauptfenster mit bestimmter Größe in X- und Y-Richtung
    window(int size_x, int size_y);

    // Hauptfenster mit bestimmter Überschrift
    explicit window(const std::string& title);

    // Hauptfenster mit beliebig vielen Kindfenstern (Besitz geht auf das Hauptfenster über)
    explicit window(std::vector<std::unique_ptr<window>> children);

    // Fenster, das innerhalb eines Elternfensters angezeigt wird
    // (benannt statt Konstruktor: window(window&) wäre eine Copy-Konstruktor-Signatur)
    static std::unique_ptr<window> create_child(window& parent);

    // Fenster mit Eigenschaften und Kindfenstern aus Ressourcendatei
    // (benannt statt Konstruktor: window(const std::string&) ist durch die Überschrift schon belegt)
    static std::unique_ptr<window> load_from_resource_file(const std::string& path);

    // ... weitere Member
};
```

---

### b) `int_smart_pointer` mit tiefem Kopieren

**`int_smart_pointer.hpp`**

```cpp
#ifndef INCLUDED__INT_SMART_POINTER_HPP
#define INCLUDED__INT_SMART_POINTER_HPP

class int_smart_pointer
{
public:
    explicit int_smart_pointer(int initial_value = 0);   // auch Default-Konstruktor
    int_smart_pointer(const int_smart_pointer& other);   // tiefe Kopie
    int_smart_pointer& operator=(const int_smart_pointer& other);
    ~int_smart_pointer();

    int get() const;
    void set(int value);

private:
    int* value_;   // Invariante: zeigt immer auf ein gültiges int auf dem Heap
};

#endif
```

**`int_smart_pointer.cpp`**

```cpp
#include "int_smart_pointer.hpp"
#include <iostream>

int_smart_pointer::int_smart_pointer(int initial_value)
    : value_(new int(initial_value))
{
    std::cout << "int_smart_pointer::int_smart_pointer(int)" << std::endl;
}

int_smart_pointer::int_smart_pointer(const int_smart_pointer& other)
    : value_(new int(*other.value_))   // neue Allokation, gleicher Wert
{
    std::cout << "int_smart_pointer::int_smart_pointer(const int_smart_pointer&)" << std::endl;
}

int_smart_pointer& int_smart_pointer::operator=(const int_smart_pointer& other)
{
    std::cout << "int_smart_pointer::operator=" << std::endl;
    if (this != &other)
        *value_ = *other.value_;       // eigene Allokation bleibt bestehen, Wert wird kopiert
    return *this;
}

int_smart_pointer::~int_smart_pointer()
{
    std::cout << "int_smart_pointer::~int_smart_pointer" << std::endl;
    delete value_;                     // kein Speicherleck
}

int int_smart_pointer::get() const
{
    std::cout << "int_smart_pointer::get" << std::endl;
    return *value_;
}

void int_smart_pointer::set(int value)
{
    std::cout << "int_smart_pointer::set" << std::endl;
    *value_ = value;
}
```

Anmerkungen:

- Zeiger `value_` ist `private`, damit von außen niemand `delete`n oder neu zuweisen kann (Klasseninvariante).
- Eine `delete`-Anweisung im Destruktor ist nötig, da der automatisch erzeugte Destruktor nur den Zeiger, nicht den Heap-Speicher freigibt.
- Der Kopierzuweisungsoperator gehört dazu (Regel der Drei): ohne ihn würde `a = b` den Zeiger flach kopieren und einen Doppel-`delete` verursachen.

**Test** (`main.cpp`)

```cpp
#include "int_smart_pointer.hpp"
#include <iostream>

int main()
{
    int_smart_pointer a;
    std::cout << a.get() << std::endl;   // Ausgabe 0
    a.set(5);
    std::cout << a.get() << std::endl;   // Ausgabe 5
    int_smart_pointer b(10);
    std::cout << b.get() << std::endl;   // Ausgabe 10
    int_smart_pointer c(b);
    std::cout << c.get() << std::endl;   // Ausgabe 10
    c.set(20);
    std::cout << b.get() << std::endl;   // Ausgabe 10 (tiefe Kopie: b unverändert)
    std::cout << c.get() << std::endl;   // Ausgabe 20
}
```

Erwartete Ausgabe (die Zeilen mit Zahlen sind die Werte, die anderen die Operationsmeldungen):

```
int_smart_pointer::int_smart_pointer(int)
int_smart_pointer::get
0
int_smart_pointer::set
int_smart_pointer::get
5
int_smart_pointer::int_smart_pointer(int)
int_smart_pointer::get
10
int_smart_pointer::int_smart_pointer(const int_smart_pointer&)
int_smart_pointer::get
10
int_smart_pointer::set
int_smart_pointer::get
10
int_smart_pointer::get
20
int_smart_pointer::~int_smart_pointer     <- c
int_smart_pointer::~int_smart_pointer     <- b
int_smart_pointer::~int_smart_pointer     <- a
```

Destruktoren laufen in umgekehrter Reihenfolge der Konstruktion. Jeder gibt seine eigene Allokation frei, es gibt kein Leck und keinen Doppel-`delete`.

---

### c) Flache Kopie

**Änderung (naiv):**

```cpp
int_smart_pointer::int_smart_pointer(const int_smart_pointer& other)
    : value_(other.value_)             // beide zeigen auf dasselbe int
{
    std::cout << "int_smart_pointer::int_smart_pointer(const int_smart_pointer&)" << std::endl;
}
// Destruktor unverändert: delete value_;
```

**Was geht schief?**

1. **Doppeltes `delete` (double free):** `b` und `c` besitzen denselben Zeiger, beide Destruktoren rufen `delete` darauf auf. Im Test wird zuerst `c`, dann `b` zerstört, die zweite Freigabe ist undefiniertes Verhalten. Mögliche Folgen sind ein Abbruch durch die Laufzeitbibliothek (glibc: `free(): double free detected`), stille Heap-Korruption oder scheinbar korrektes Verhalten (deshalb "muss sich nicht äußern").
2. **Dangling Pointer:** Wird eine Kopie früher zerstört (z. B. `c` in einem inneren Block), zeigen die übrigen Kopien auf freigegebenen Speicher, jeder weitere `get`/`set` ist ein Use-after-free.
3. Die Semantik ändert sich sichtbar: Nach `c.set(20)` liefert auch `b.get()` den Wert 20. Das ist bei flacher Kopie erwartetes Verhalten, aber die Speicherverwaltung ist nun falsch.
4. Der Zuweisungsoperator müsste analog behandelt werden. Kopiert er den Zeiger flach (`value_ = other.value_`), geht die eigene Allokation verloren (Speicherleck), außerdem Doppel-`delete`.

**Lösung:** Den gemeinsamen Besitz explizit verwalten, entweder mit eigenem Referenzzähler oder mit `std::shared_ptr<int>`. Die letzte Kopie gibt den Speicher frei:

```cpp
// Header: private Member ersetzen
#include <memory>
// ...
private:
    std::shared_ptr<int> value_;

// Implementierung
int_smart_pointer::int_smart_pointer(int initial_value)
    : value_(std::make_shared<int>(initial_value))
{ std::cout << "int_smart_pointer::int_smart_pointer(int)" << std::endl; }

int_smart_pointer::int_smart_pointer(const int_smart_pointer& other)
    : value_(other.value_)             // flache Kopie, Referenzzähler wird erhöht
{ std::cout << "int_smart_pointer::int_smart_pointer(const int_smart_pointer&)" << std::endl; }

int_smart_pointer::~int_smart_pointer()
{ std::cout << "int_smart_pointer::~int_smart_pointer" << std::endl; }   // Freigabe erfolgt durch shared_ptr

int_smart_pointer& int_smart_pointer::operator=(const int_smart_pointer& other)
{ std::cout << "int_smart_pointer::operator=" << std::endl; value_ = other.value_; return *this; }
```

Im Test gibt `b.get()` nun 20 aus (identisches `int`), und nur der zuletzt zerstörte Besitzer gibt den Speicher frei.

---

### d) Klasse `rabbit`

Entwurfsentscheidungen:

- `name` und `ears` ändern sich nie und haben keine Invariante. Nach der Faustregel der Vorlesung ("Zugriffsspezifizierer nur zum Erhalt von Invarianten") sind sie daher `public const`-Member statt Getter.
- `age_` und `weight_` sind `private`: Sie sollen sich nur über `altern()` bzw. `fuettern()` ändern.
- `essbar` wird **nicht gespeichert, sondern berechnet**. So passt der Wert zwangsläufig immer zu Alter und Gewicht (keine Inkonsistenz möglich), und er ist von außen nur lesbar.
- Grenzen sind inklusiv interpretiert (9 ≤ Alter ≤ 12, 1500 ≤ Gewicht ≤ 2000).
- "Zufällige Zahl zwischen 10 und 200" als `float` aus `std::uniform_real_distribution` (`<random>`).
- Konstruktor mit Initialisierungsliste in Deklarationsreihenfolge.

**`rabbit.hpp`**

```cpp
#ifndef INCLUDED__RABBIT_HPP
#define INCLUDED__RABBIT_HPP

#include <string>

class rabbit
{
public:
    rabbit(const std::string& name, int ears);

    void altern();                 // Alter + 1 Woche
    void fuettern();               // Gewicht + Zufallszahl in [10, 200]

    int alter() const;
    float gewicht() const;
    bool essbar() const;           // nur lesbar, immer konsistent

    const std::string name;        // unveränderlich, keine Invariante nötig
    const int ears;

private:
    int age_;                      // in Wochen
    float weight_;                 // in Gramm
};

#endif
```

**`rabbit.cpp`**

```cpp
#include "rabbit.hpp"
#include <random>

namespace
{
    // Ein Generator für das gesamte Programm, beim ersten Aufruf zufällig initialisiert.
    float random_between(float min, float max)
    {
        static std::mt19937 generator{std::random_device{}()};
        std::uniform_real_distribution<float> distribution(min, max);
        return distribution(generator);
    }
}

rabbit::rabbit(const std::string& name, int ears)
    : name(name), ears(ears), age_(0), weight_(100.0f)
{ }

void rabbit::altern()
{
    ++age_;
}

void rabbit::fuettern()
{
    weight_ += random_between(10.0f, 200.0f);
}

int rabbit::alter() const { return age_; }
float rabbit::gewicht() const { return weight_; }

bool rabbit::essbar() const
{
    return age_ >= 9 && age_ <= 12
        && weight_ >= 1500.0f && weight_ <= 2000.0f;
}
```

**`main.cpp`** (Test)

Wegen der Zufallszahlen ist die Ausgabe nicht deterministisch. Die drei Hasen sind so gewählt, dass sich die Fälle "zu dick", "zu dünn" und "passt" zeigen. Ein Hase wiegt nach `n` Fütterungen im Mittel 100 + 105·n Gramm.

```cpp
#include "rabbit.hpp"
#include <iostream>

// Lässt einen Hasen 14 Wochen altern und füttert ihn dabei; gibt jede Woche den Zustand aus.
// Solange das Gewicht unter umstell_gewicht liegt, wird futter_anfangs-mal pro Woche gefüttert,
// danach futter_spaeter-mal.
void simuliere(rabbit& hase, int futter_anfangs, int futter_spaeter, float umstell_gewicht)
{
    std::cout << "--- " << hase.name << " (" << hase.ears << " Ohren) ---\n";
    for (int woche = 1; woche <= 14; ++woche)
    {
        hase.altern();
        int anzahl = hase.gewicht() < umstell_gewicht ? futter_anfangs : futter_spaeter;
        for (int i = 0; i < anzahl; ++i)
            hase.fuettern();

        std::cout << "Alter " << hase.alter() << " Wochen, "
                  << hase.gewicht() << " g, essbar: "
                  << (hase.essbar() ? "ja" : "nein") << '\n';
    }
}

int main()
{
    rabbit dick("Fettel", 2);      // 3x pro Woche: zu schwer, sobald das Alter passt
    rabbit duenn("Zwirn", 2);      // 1x pro Woche: bleibt zu leicht
    rabbit normal("Hoppel", 2);    // erst 2x pro Woche, ab ca. 1300 g nur noch 1x: wird ca. mit 9-11 Wochen essbar

    simuliere(dick, 3, 3, 0.0f);
    simuliere(duenn, 1, 1, 0.0f);
    simuliere(normal, 2, 1, 1300.0f);
}
```

Erwartung: `Fettel` ist nie essbar (mit 9 Wochen schon rund 2900 g), `Zwirn` nie (mit 12 Wochen nur rund 1400 g), `Hoppel` typischerweise in einigen Wochen zwischen 9 und 12 (genauer Zeitraum je nach Zufall).

---

### e) Häschenkette und `stall`

Entwurfsentscheidungen:

- Jeder Hase hat zwei Zeiger `left_` und `right_` (`nullptr` = kein Partner), private, damit die Kette nicht von außen zerstört werden kann. Die **Invariante** ist: `a->right_ == b` genau dann, wenn `b->left_ == a`.
- `stall` ist `friend` von `rabbit` (Friending aus der Vorlesung): Nur der Stall darf die Ketten-Zeiger verändern, die öffentliche Schnittstelle bleibt schmal.
- Der Stall speichert nur `first_`. Er **besitzt** alle Hasen und löscht sie im Destruktor (Regel der Drei: Kopieren wird gesperrt). Auch `rabbit` wird nicht kopierbar gemacht, weil eine Kopie die Nachbarzeiger mitkopieren würde.
- Der Destruktor löscht iterativ (nicht rekursiv), damit lange Ketten keinen Stack-Überlauf verursachen.
- Die Aufgabe nennt die Ausgabefunktion einmal `inventarisieren` und im Test `prüfen`. Hier wird durchgehend `inventarisieren` verwendet.
- Hinweis: Bei genau einer Fütterung pro Woche (Mittelwert 105 g) erreicht ein Hase mit 9–12 Wochen nur etwa 1050–1360 g und wird **praktisch nie essbar**, sondern nur nach über 50 Wochen ausgesondert. Damit auch das Ernten essbarer Hasen zu sehen ist, hat `zuechten` einen optionalen Parameter `fuetterungen` (Standard 1 wie in der Aufgabe). Der Test verwendet 2.

**`rabbit.hpp`** (Erweiterung gegenüber d)

```cpp
#ifndef INCLUDED__RABBIT_HPP
#define INCLUDED__RABBIT_HPP

#include <string>

class rabbit
{
    friend class stall;            // nur der Stall darf die Kette verändern

public:
    rabbit(const std::string& name, int ears);

    rabbit(const rabbit&) = delete;             // Kopie würde Nachbarzeiger duplizieren
    rabbit& operator=(const rabbit&) = delete;

    void altern();
    void fuettern();

    int alter() const;
    float gewicht() const;
    bool essbar() const;

    const std::string name;
    const int ears;

private:
    int age_;
    float weight_;
    rabbit* left_;                 // Hase an der linken Hand oder nullptr
    rabbit* right_;                // Hase an der rechten Hand oder nullptr
};

#endif
```

**`rabbit.cpp`**: gegenüber d) ändert sich nur der Konstruktor:

```cpp
rabbit::rabbit(const std::string& name, int ears)
    : name(name), ears(ears), age_(0), weight_(100.0f), left_(nullptr), right_(nullptr)
{ }
```

**`stall.hpp`**

```cpp
#ifndef INCLUDED__STALL_HPP
#define INCLUDED__STALL_HPP

#include "rabbit.hpp"
#include <string>

class stall
{
public:
    stall();
    ~stall();

    stall(const stall&) = delete;               // Stall besitzt die Hasen
    stall& operator=(const stall&) = delete;

    void hinzufuegen(const std::string& name, int ears);   // neuen Hasen hinten anhängen
    void zuechten(int fuetterungen = 1);                   // alle altern und füttern
    void ernten();                                         // essbare und alte Hasen entfernen
    void inventarisieren() const;                          // Daten aller Hasen ausgeben
    bool leer() const;

private:
    rabbit* first_;                // einziger Einstieg in die Kette
};

#endif
```

**`stall.cpp`**

```cpp
#include "stall.hpp"
#include <iostream>

stall::stall()
    : first_(nullptr)
{ }

stall::~stall()
{
    rabbit* current = first_;
    while (current)                // iterativ löschen, Nachfolger vorher merken
    {
        rabbit* next = current->right_;
        delete current;
        current = next;
    }
}

void stall::hinzufuegen(const std::string& name, int ears)
{
    rabbit* neu = new rabbit(name, ears);   // right_ ist nach dem Konstruktor nullptr

    if (!first_)                            // leerer Stall: neuer Hase ist der erste
    {
        first_ = neu;
        return;
    }

    rabbit* last = first_;                  // letzten Hasen suchen
    while (last->right_)
        last = last->right_;

    last->right_ = neu;                     // bisher letzter Hase bekommt Partner rechts ...
    neu->left_ = last;                      // ... und der neue Hase einen links
}

void stall::zuechten(int fuetterungen)
{
    for (rabbit* r = first_; r; r = r->right_)
    {
        r->altern();
        for (int i = 0; i < fuetterungen; ++i)
            r->fuettern();
    }
}

void stall::ernten()
{
    rabbit* current = first_;
    while (current)
    {
        rabbit* next = current->right_;     // vor dem möglichen delete merken!

        if (current->essbar() || current->alter() > 50)
        {
            // Kette schließen: Nachbarn miteinander verbinden
            if (current->left_)
                current->left_->right_ = current->right_;
            else
                first_ = current->right_;   // erster Hase entfernt: neuer Einstieg

            if (current->right_)
                current->right_->left_ = current->left_;

            delete current;
        }
        current = next;
    }
}

void stall::inventarisieren() const
{
    std::cout << "Stall:";
    if (!first_)
        std::cout << " leer";
    std::cout << '\n';

    for (const rabbit* r = first_; r; r = r->right_)
    {
        std::cout << "  " << r->name
                  << ", Ohren: " << r->ears
                  << ", Alter: " << r->alter() << " Wochen"
                  << ", Gewicht: " << r->gewicht() << " g"
                  << ", essbar: " << (r->essbar() ? "ja" : "nein") << '\n';
    }
}

bool stall::leer() const
{
    return first_ == nullptr;
}
```

**`main.cpp`** (Test)

```cpp
#include "stall.hpp"
#include <iostream>

int main()
{
    stall s;
    s.hinzufuegen("Hoppel", 2);
    s.hinzufuegen("Mümmel", 2);
    s.hinzufuegen("Schlappohr", 2);
    s.hinzufuegen("Stummel", 1);
    s.hinzufuegen("Flauschi", 2);

    std::cout << "== Anfangszustand ==\n";
    s.inventarisieren();

    int runde = 0;
    while (!s.leer())                       // terminiert spätestens nach 51 Runden (Alter > 50)
    {
        ++runde;

        std::cout << "\n== Runde " << runde << ": züchten ==\n";
        s.zuechten(2);                      // 2 Fütterungen pro Woche, siehe Hinweis oben
        s.inventarisieren();

        std::cout << "\n== Runde " << runde << ": ernten ==\n";
        s.ernten();
        s.inventarisieren();
    }
}
```

Zu beachten:

- In `ernten()` muss der Nachfolger **vor** dem `delete` gemerkt werden, sonst wird nach dem Löschen auf freigegebenen Speicher zugegriffen.
- Drei Fälle beim Entfernen: erster Hase (Einstieg `first_` neu setzen), mittlerer Hase (beide Nachbarn verbinden), letzter Hase (linker Nachbar bekommt leere rechte Hand).
- Bei 2 Fütterungen pro Woche wiegt ein Hase mit 9 Wochen im Mittel rund 1990 g (Streuung ca. ±230 g). Ungefähr die Hälfte der Hasen wird also mit 9 Wochen essbar und beim nächsten `ernten()` entfernt, die übrigen werden zu schwer und erst nach über 50 Wochen ausgesondert. Die genaue Verteilung hängt vom Zufall ab.
- Es gibt kein Speicherleck: Alle Hasen werden entweder in `ernten()` oder im Destruktor des Stalls gelöscht (prüfbar mit `valgrind` oder `-fsanitize=address`).