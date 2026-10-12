# Algorithmen und Datenstrukturen – Übung 5: Container (Lösung mit Erklärungen)

> Hinweis: Das Übungsblatt 4 (`int_vector`) liegt mir nicht vor. In Aufgabe 2 gehe ich deshalb von einem typischen `int_vector` aus (Zeiger auf Daten, `size`, `capacity`, Wachstum durch Verdoppeln). Die Ideen lassen sich 1:1 auf Ihren eigenen Code übertragen.

---

## Aufgabe 1: Theorie

### a) Template-Methode außerhalb der Vorlage definieren

**Kleine Korrektur am Beispiel:** In der `.cpp` müsste es `X<A, B, R>::method` heißen (die Klasse hat drei Parameter, nicht zwei). Das ist aber nicht das eigentliche Problem.

**Experiment**

```cpp
// x.hpp
template <typename A, typename B, typename R>
class X { public: R method(A a, B b); };

// x.cpp
#include "x.hpp"
template <typename A, typename B, typename R>
R X<A, B, R>::method(A a, B b) { return (R)(a + b); }

// main.cpp
#include "x.hpp"
int main() { X<int, int, int> x; return x.method(1, 2); }
```

**Was geht schief? Wie äußert es sich?**
Der Compiler läuft fehlerfrei durch, aber der **Linker** bricht ab:

- GCC/Clang: `undefined reference to 'X<int, int, int>::method(int, int)'`
- MSVC: `error LNK2019: Nicht aufgelöstes externes Symbol "public: int __thiscall X<int,int,int>::method(int,int)"`

**Warum?**

1. C++ übersetzt jede `.cpp` **einzeln** zu einer `.obj`-Datei (eine *Übersetzungseinheit*, ÜE). Eine ÜE kennt nur das, was per `#include` hineinkopiert wurde.
2. In `main.cpp` ist nur die **Deklaration** von `X::method` sichtbar. Der Compiler erzeugt den Aufruf, kennt aber den Rumpf nicht. Er kann daher keinen Maschinencode für `X<int,int,int>::method` erzeugen. Er schreibt nur einen Verweis auf ein externes Symbol in die `main.obj`. Das Symbol soll später der Linker auflösen.
3. In `x.cpp` steht die Definition, aber nur als **Vorlage**. Eine Vorlage ist kein Code, sondern ein Bauplan. Maschinencode hängt von den konkreten Typen ab:
   - `int + int` wird zu einer Integer-Add-Instruktion,
   - `float + float` zu einer SSE-Gleitkomma-Addition,
   - `std::string + std::string` zu einem Aufruf von `operator+` mit Speicherverwaltung.

   Ohne konkrete Typen (`A`, `B`, `R`) kann der Compiler nichts erzeugen. In `x.cpp` wird `X` mit keinem Typ verwendet. Also **instanziiert der Compiler nichts**, und `x.obj` enthält kein `method`-Symbol. Das lässt sich mit `dumpbin /symbols x.obj` (MSVC) oder `nm x.o` (GCC) prüfen.
4. Der Linker sucht in allen `.obj`-Dateien ein Symbol `X<int,int,int>::method`. Er findet keins, also gibt es den Fehler.

**Warum löst sich das Problem bei Definition innerhalb der Vorlage (bzw. im Header)?**
Dann gelangt die Definition per `#include` in **jede** ÜE, die `X<...>` verwendet. Beim Übersetzen von `main.cpp` kennt der Compiler den Rumpf und die konkreten Typen. Er kann `X<int,int,int>::method` also in `main.obj` instanziieren und den Maschinencode dort erzeugen. Der Linker hat dann nichts mehr aufzulösen.

*Merksatz:* Der Compiler braucht bei der Instanziierung **Typen und Definition gleichzeitig in derselben ÜE**. Deshalb liegen Template-Definitionen in der Praxis im Header.

**Weitere Lösungswege:** (1) Außerhalb-Definition in einer Datei, die der Header am Ende selbst `#include`t (z. B. `x.inl`/`x.tpp`). (2) *Explizite Instanziierung* in der `x.cpp` mit `template class X<int,int,int>;`. Dann gibt es den Code, aber nur für genau diese Typen.

---

### b) `swap_template`-Beispiel

**Überblick über die drei Dateien**

| Datei | Was steht dort? |
|---|---|
| `swap_template.hpp` | nur *Deklaration* `template<T> T swap(const T&, const T&)` (Rückgabe `T`, **const**-Referenzen) |
| `swap_template_a.cpp` | *Definition* `template<T> void swap(T&, T&)` mit absichtlich kaputtem Rumpf (`a = b; b = 0;`) |
| `swap_template_b.cpp` | *Definition* `template<T> void swap(T&, T&)` mit korrektem Rumpf |

Die Definitionen in a und b haben also **nicht** die Signatur aus dem Header. Sie sind *andere Überladungen* derselben Vorlage `swap`.

**Welche Überladung wird aufgerufen?**
Beim Aufruf `swap(a, b)` mit zwei nicht-konstanten `int`-Lvalues gibt es zwei Kandidaten, jeweils mit `T = int`:

- `swap(const int&, const int&)` aus dem Header (nur deklariert),
- `swap(int&, int&)` aus der eigenen `.cpp` (definiert).

Die Bindung an `int&` ist besser als die an `const int&` (weniger cv-qualifiziert). Es gewinnt also die Überladung der jeweiligen `.cpp`, und die Header-Version wird nie benutzt.

**Frage 1: Welche Werte stehen in a bis d?**

Das Ergebnis hängt vom Build ab. Es ist nämlich ein ODR-Verstoß (siehe unten):

| Szenario | Ausgabe | Erklärung |
|---|---|---|
| Debug (kein Inlining), Linker nimmt Version aus **a** | `2 0` und `4 0` | `a=2, b=0`. Auch `run()` nutzt die kaputte Version: `c=4, d=0` |
| Debug (kein Inlining), Linker nimmt Version aus **b** | `2 1` und `4 3` | beide Aufrufe nutzen die korrekte Version |
| Release (Inlining) | `2 0` und `4 3` | jeder Aufruf wird in seiner ÜE inlined, jede ÜE nutzt ihre eigene Definition |

Welche Version im Debug-Fall gewinnt, ist in der Regel die **zuerst** auf der Linker-Kommandozeile stehende `.obj`. Es ist aber nicht festgelegt. Verlassen kann man sich auf nichts.

**Frage 2: Warum kompiliert das Programm trotz mehrfacher Definition?**

- Jede `.cpp` wird für sich übersetzt. Innerhalb einer ÜE gibt es genau **eine** Definition, also keinen Compilerfehler.
- Beim Instanziieren erzeugt der Compiler `swap<int>(int&, int&)` in **beiden** `.obj`-Dateien, mit **demselben** Symbolnamen (Name Mangling). Instanziierungen von Templates werden als *schwache Symbole* (COMDAT, `selectany`) markiert. Das erlaubt ausdrücklich, dass dasselbe Symbol in mehreren `.obj`-Dateien auftaucht.
- Der Linker nimmt an, dass alle schwachen Duplikate **identisch** sind, behält **eine** beliebige Kopie und verwirft die anderen. Er vergleicht den Inhalt nicht.

Hier sind die Definitionen aber verschieden. Das verletzt die *One Definition Rule* (ODR). Laut Standard ist das *„ill-formed, no diagnostic required"*: Kein Werkzeug muss warnen, das Programm hat undefiniertes Verhalten. Genau das macht den Fehler so gefährlich.

**Frage 3: Was passiert, wenn man eine Definition weglässt?**
Lässt man z. B. die Definition in `b.cpp` weg, sieht der Compiler dort nur die Header-Deklaration `swap(const T&, const T&)`. Der Aufruf in `run()` bindet an sie, und sie hat keinen Rumpf. Es entsteht ein **Linkerfehler** (`undefined reference to swap<int>(int const&, int const&)`). Der Symbolname unterscheidet sich vom `swap(int&, int&)` aus `a.cpp`, es hilft also nicht, dass dort eine Instanz existiert. Dasselbe passiert, wenn man die Definition in `a.cpp` weglässt.

**Frage 4: Schlussfolgerung für Templates**

1. Eine Template-Definition muss in **jeder ÜE sichtbar** sein, die sie instanziiert, also in den Header.
2. Es darf zu jedem Template (gleicher Name und gleiche Signatur) nur **eine einzige** Definition geben. Der Linker schützt uns bei Templates nicht vor widersprüchlichen Definitionen, im Gegensatz zu normalen Funktionen.
3. Eine Deklaration im Header ohne Definition ist bei Templates fast immer ein Fehler (siehe Aufgabe a).
4. Will man eine Hilfsvorlage nur lokal benutzen, gehört sie in einen unbenannten Namespace oder wird `static` (internal linkage). Dann gibt es keine Kollision.

---

### c) Vorlage `X` in vielen `.cpp`-Dateien mit denselben Typparametern

**Problem:** Wegen der Erkenntnisse aus a) und b) instanziiert jede ÜE `X<int>` selbst. Der identische Maschinencode landet also in jeder `.obj`-Datei:

- Der Compiler übersetzt dasselbe immer wieder (längere Compilezeiten, auch weil jede ÜE den Header neu parst).
- Die `.obj`-Dateien werden größer, der Linker muss mehr Daten verarbeiten.
- Die Duplikate müssen später wieder entfernt werden.

**Wie kann die Compilerpipeline damit umgehen?**

1. **Schwache Symbole / COMDAT-Folding (Standardlösung):** Jede ÜE erzeugt die Instanz wie bisher. Die Instanzen werden als schwach markiert, und der Linker behält genau eine Kopie und wirft den Rest weg (siehe b). Das kostet Compilezeit, ist aber die einfachste und wichtigste Technik.
2. **Explizite Instanziierung (manuell, C++11):** In einer einzigen `.cpp` schreibt man `template class X<int>;`, in den Headern `extern template class X<int>;`. Letzteres sagt: „Die Instanz existiert woanders, erzeuge sie hier nicht." So wird sie nur einmal übersetzt.
3. **Template-Repository / Instantiation-Cache (ältere Compiler, z. B. GCC `-frepo`):** Der Compiler merkt sich, welche Instanzen schon existieren, und erzeugt jede nur einmal.
4. **Precompiled Headers und C++20-Module:** Der Header wird nicht in jeder ÜE neu geparst, das spart zumindest den Parse-Aufwand.

---

### d) `std::list`-Iterator läuft über `end()` hinaus

```cpp
std::list<int> l({1, 2, 3});
std::list<int>::iterator it(l.begin());
it++; it++; it++; it++; it++;
// std::cout << *it;
it--; it--; it--;
std::cout << *it;
```

**Verhalten: undefiniertes Verhalten (UB).** `end()` darf nicht inkrementiert werden. Dasselbe gilt für das Dekrementieren von `begin()` und das Dereferenzieren von `end()`. Gültig ist nur der Bereich `[begin, end]`.

**Was passiert praktisch?**

*Release-Build:* Die gängigen Implementierungen (libstdc++, MSVC) speichern `std::list` als *zirkuläre doppelt verkettete Liste mit einem Sentinel-Knoten*. `end()` zeigt auf diesen Sentinel, dessen `next` auf das erste Element zeigt. Der Iterator zählt dann einfach weiter:

```
Start:        begin → 1
1. it++       → 2
2. it++       → 3
3. it++       → end (Sentinel)
4. it++       → 1   (UB, "wrap-around")
5. it++       → 2   (UB)
3x it--       → 1 → Sentinel → 3
Ausgabe:      3
```

Das Programm gibt also **3** aus. Es sieht „richtig" aus, ist aber nur Zufall der Implementierung.

*Zeile 4 (`*it` nach 5×`++`):* Im Release-Build zeigt `it` zufällig auf das Element `2`. Es wird also **2** ausgegeben, ohne Absturz. Bei einer anderen Anzahl von Inkrementen läge der Iterator auf dem Sentinel, und `*it` würde Speicher lesen, der keinen gültigen `int` enthält (Datenmüll, im ungünstigen Fall Absturz).

*Debug-Build:* Die Standardbibliotheken enthalten **Iterator-Debugging** (MSVC: `_ITERATOR_DEBUG_LEVEL`, libstdc++: `-D_GLIBCXX_DEBUG`). Der 4. Aufruf von `it++` schlägt dann mit einer Assertion fehl (*„list iterator not incrementable"*), und zu Zeile 4 kommt man gar nicht erst.

**Warum prüft die Release-Version nicht?** C++ folgt dem Prinzip *„you don't pay for what you don't use"*. Jede Prüfung kostet Laufzeit in der innersten Schleife. Der Programmierer ist dafür verantwortlich, nur gültige Iteratoren zu verwenden.

---

### e) Ändert sich das Verhalten bei `std::vector`?

**Formal nein.** Die Dokumentation (cppreference) legt für `vector` ebenfalls fest: Inkrementieren von `end()` und Dereferenzieren von `end()` sind undefiniertes Verhalten. Auch der Zeigerwert `begin()+5` bei nur 3 Elementen ist schon UB (erlaubt ist maximal one-past-the-end).

**Praktisch gibt es Unterschiede:**

- Ein `vector<int>::iterator` ist im Release-Build im Kern ein Zeiger. `++` addiert `sizeof(int)`, und es gibt **kein** Wrap-around. Nach 5×`++` steht der Iterator bei `begin()+5`, nach 3×`--` bei `begin()+2`. `*it` liefert hier ebenfalls **3**.
- **Zeile 4** verhält sich aber anders: `*it` liest `begin()[5]`, also Speicher hinter dem Puffer (Heap-Datenmüll, im ungünstigen Fall ein Zugriffsfehler). Bei der Liste liest man dagegen ein gültiges Element, weil die Liste im Kreis läuft.
- Debug-Build: Auch hier greifen die Prüfungen (Assertion bei `++` über `end()`).

Die Aufgabe will zeigen: **Compiler und Verstand helfen nicht, nur die Doku.** Ob UB „funktioniert", sagt nichts über die Korrektheit.

---

### f) Der `erase`-Fehler

```cpp
std::list<int> a({3, 5, 7, 9, 11});
std::list<int> b({2, 4, 6, 7, 13});
auto x(std::find(a.begin(), a.end(), 7));   // x gehört zu a!
b.erase(x);                                  // erase auf b
```

**Das Problem:** `x` ist ein Iterator in **a**, wird aber an `b.erase()` übergeben. Das ist UB. Wahrscheinlich wollte der Programmierer `std::find(b.begin(), b.end(), 7)` schreiben (Tippfehler/Copy-Paste). Zusätzlich wäre `x == a.end()` möglich, falls 7 nicht vorkäme.

**Wie äußert es sich im Release-Build?**
Eine zeitoptimale Implementierung von `list::erase` entfernt den Knoten in **O(1)**:

```cpp
node->prev->next = node->next;
node->next->prev = node->prev;
--size_;           // Zähler des Containers, auf dem erase aufgerufen wurde (b)
delete node;
```

Es wird **nicht geprüft**, ob der Knoten überhaupt zu `b` gehört. Das wäre nur in O(n) möglich und würde den Vorteil der Liste zunichte machen. Die Folgen sind:

- Der Knoten `7` wird aus der Kette von **a** ausgehängt und freigegeben. Die Nachbarn `5` und `9` sind korrekt neu verlinkt, `a` sieht also beim Durchlaufen wie `3 5 9 11` aus.
- `a.size()` ist weiterhin 5, aber es gibt nur noch 4 Knoten. Dafür ist `b.size()` plötzlich 4, obwohl alle 5 Knoten noch dran hängen und die `7` aus `b` **nicht** gelöscht wurde.
- Es gibt keinen Absturz und keine Ausnahme. Das Programm läuft scheinbar normal weiter.

**Warum ist das schwer zu finden?**

- Der Fehler tritt an einer anderen Stelle auf, als er sich zeigt (falsche Größen, falsche Inhalte, später doppelte Freigabe oder Absturz beim Zerstören).
- Es gibt keinen Compilerfehler: `list<int>::iterator` ist für beide Listen derselbe Typ. Der Typ allein verrät die Zugehörigkeit zum Container nicht.
- Im Release-Build gibt es keinerlei Prüfung, nur im Debug-Build (Iterator-Debugging prüft die Zugehörigkeit).
- Das Verhalten ist reproduzierbar „fast richtig" und hängt von der Implementierung ab.

**Konsequenz:** Iteratoren immer nur mit dem Container verwenden, aus dem sie stammen. Debug-Builds mit Iterator-Prüfung testen und Sanitizer verwenden.

---

## Aufgabe 2: Praxis

### a) `int_vector` → Vorlage `vector<T>` (minimale Änderungen)

**Vorgehen:** Überall, wo `int` der *Elementtyp* ist, wird `T` eingesetzt. Aus `class int_vector` wird `template <typename T> class vector`. Weiterhin wird mit `malloc`/`realloc` gearbeitet. **Alle Methoden müssen im Header stehen** (siehe Aufgabe 1a).

```cpp
// vector.hpp  (Stufe a: nur für "einfache" Typen wie int, double, ...)
#pragma once
#include <cstddef>
#include <cstdlib>
#include <cstring>
#include <new>

template <typename T>
class vector
{
    T*          data_;
    std::size_t size_;
    std::size_t capacity_;

public:
    vector() : data_(nullptr), size_(0), capacity_(0) {}

    vector(const vector& o) : data_(nullptr), size_(0), capacity_(0)
    {
        reserve(o.size_);
        if (o.size_) std::memcpy(data_, o.data_, o.size_ * sizeof(T));
        size_ = o.size_;
    }

    ~vector() { std::free(data_); }

    vector& operator=(const vector& o)
    {
        if (this != &o) { vector tmp(o); swap(tmp); }
        return *this;
    }

    void swap(vector& o) noexcept
    {
        std::swap(data_, o.data_);
        std::swap(size_, o.size_);
        std::swap(capacity_, o.capacity_);
    }

    void reserve(std::size_t n);                  // wird unten außerhalb definiert
    void push_back(const T& v)
    {
        if (size_ == capacity_) reserve(capacity_ ? capacity_ * 2 : 4);
        data_[size_++] = v;                       // Zuweisung auf rohen Speicher!
    }

    T&          operator[](std::size_t i)       { return data_[i]; }
    const T&    operator[](std::size_t i) const { return data_[i]; }
    std::size_t size() const     { return size_; }
    std::size_t capacity() const { return capacity_; }
};

// Definition AUSSERHALB der Klasse: template-Zeile und <T> nicht vergessen,
// und es muss weiterhin im HEADER stehen!
template <typename T>
void vector<T>::reserve(std::size_t n)
{
    if (n <= capacity_) return;
    T* p = static_cast<T*>(std::realloc(data_, n * sizeof(T)));
    if (!p) throw std::bad_alloc();
    data_ = p;
    capacity_ = n;
}
```

Wichtige Änderungen gegenüber `int_vector`:

- `int` → `T` (Zeiger, Parameter, Rückgabetypen),
- `sizeof(int)` → `sizeof(T)`,
- die Klasse wird zur Vorlage, Methodendefinitionen wandern in den Header (außerhalb mit `template <typename T>` und `vector<T>::`).

**Einfacher Test** (zunächst nur mit `int`; mit `std::string` knallt es, siehe b):

```cpp
vector<int> v;
for (int i = 0; i < 10; ++i) v.push_back(i * i);
for (std::size_t i = 0; i < v.size(); ++i) std::cout << v[i] << ' ';
```

---

### b) Funktioniert `vector<std::string>`?

**Nein, die Version aus a) ist für `std::string` fehlerhaft** (sie kompiliert, stürzt aber ab oder verhält sich unvorhersehbar).

**Warum?**

1. **Keine Konstruktion.** `malloc` liefert **rohen Speicher**, es wird kein Konstruktor aufgerufen. `data_[size_++] = v;` ist eine *Zuweisung* auf ein Objekt, das noch gar nicht existiert. `std::string::operator=` interpretiert den Datenmüll als gültigen String (Zeiger, Länge, Kapazität) und gibt womöglich fremden Speicher frei. Das ist UB.
2. **Kein Destruktor.** `free` gibt zwar den Puffer frei, die Strings darin werden aber nie zerstört. Deren eigener Heap-Speicher leckt.
3. **Bitweises Kopieren (`memcpy`/`realloc`) ist für Strings nicht erlaubt.** `std::string` ist nicht *trivially copyable*. Bei der *Small String Optimization* (SSO) zeigt ein interner Zeiger auf den Puffer *innerhalb des Objekts selbst*. Nach dem Umkopieren zeigt er noch auf die alte Adresse (dangling). Bei langen Strings würden Kopie und Original denselben Heap-Block besitzen (doppeltes `delete`).

**Korrektur mit geeigneten Mitteln** (weiterhin `malloc`, dazu *placement new* aus der Vorlesung):

| Stelle | Vorher | Nachher |
|---|---|---|
| Element einfügen | `data_[i] = v;` | `new (data_ + i) T(v);` (placement new, ruft den Copy-Konstruktor auf) |
| Element entfernen | nichts | `data_[i].~T();` (expliziter Destruktoraufruf) |
| Wachsen | `realloc` | neuer `malloc`-Block, Elemente per `new (neu + i) T(std::move(alt[i]))` umziehen, alte zerstören, `free` |
| Kopieren | `memcpy` | Element für Element kopierkonstruieren |
| Destruktor | `free` | erst alle Elemente zerstören, dann `free` |

**Vollständige korrigierte Version inklusive Iterator (Aufgabe c und die Variante aus e im Kommentar):**

```cpp
// vector.hpp
#pragma once
#include <cstddef>
#include <cstdlib>
#include <new>
#include <utility>

// ---------- Aufgabe 2c: eigener Iterator ----------
template <typename T>
class vector_iterator
{
    T* p_;

public:
    explicit vector_iterator(T* p = nullptr) : p_(p) {}   // auch default-konstruierbar

    T& operator*()  const { return *p_; }
    T* operator->() const { return p_; }

    vector_iterator& operator++()    { ++p_; return *this; }
    vector_iterator  operator++(int) { vector_iterator t(*this); ++p_; return t; }
    vector_iterator& operator--()    { --p_; return *this; }
    vector_iterator  operator--(int) { vector_iterator t(*this); --p_; return t; }

    // Zugriff relativ zum aktuellen Eintrag (nicht relativ zum Vektoranfang!)
    T& operator[](std::ptrdiff_t offset) const { return p_[offset]; }

    bool operator==(const vector_iterator& o) const { return p_ == o.p_; }
    bool operator!=(const vector_iterator& o) const { return p_ != o.p_; }
};

// ---------- Aufgabe 2a + 2b: vector ----------
template <typename T>
class vector
{
    T*          data_;
    std::size_t size_;
    std::size_t capacity_;

public:
    using value_type     = T;
    using iterator       = vector_iterator<T>;
    using const_iterator = vector_iterator<const T>;

    vector() noexcept : data_(nullptr), size_(0), capacity_(0) {}

    vector(const vector& o) : vector()            // delegiert: Objekt gilt dann als konstruiert
    {
        reserve(o.size_);
        for (std::size_t i = 0; i < o.size_; ++i)
            push_back(o.data_[i]);                // jedes Element wird kopierkonstruiert
    }

    vector(vector&& o) noexcept
        : data_(o.data_), size_(o.size_), capacity_(o.capacity_)
    { o.data_ = nullptr; o.size_ = o.capacity_ = 0; }

    vector& operator=(vector o) noexcept          // copy-and-swap (deckt Copy und Move ab)
    { swap(o); return *this; }

    ~vector() { clear(); std::free(data_); }

    void swap(vector& o) noexcept
    {
        std::swap(data_, o.data_);
        std::swap(size_, o.size_);
        std::swap(capacity_, o.capacity_);
    }

    void reserve(std::size_t n)
    {
        if (n <= capacity_) return;
        T* neu = static_cast<T*>(std::malloc(n * sizeof(T)));
        if (!neu) throw std::bad_alloc();
        for (std::size_t i = 0; i < size_; ++i)
        {
            new (neu + i) T(std::move(data_[i]));  // im neuen Block konstruieren ...
            data_[i].~T();                         // ... und das alte Objekt zerstören
        }
        std::free(data_);
        data_ = neu;
        capacity_ = n;
    }

    void push_back(const T& v)
    {
        T tmp(v);   // Kopie VOR reserve(): v könnte ein Element dieses Vektors sein,
                    // das beim Umkopieren ungültig würde (Referenz-Invalidierung!)
        if (size_ == capacity_) reserve(capacity_ ? capacity_ * 2 : 4);
        new (data_ + size_) T(std::move(tmp));     // placement new
        ++size_;
    }

    void pop_back() { data_[--size_].~T(); }       // expliziter Destruktoraufruf

    void clear() { while (size_) pop_back(); }

    T&          operator[](std::size_t i)       { return data_[i]; }
    const T&    operator[](std::size_t i) const { return data_[i]; }
    std::size_t size() const     { return size_; }
    std::size_t capacity() const { return capacity_; }
    bool        empty() const    { return size_ == 0; }

    // ---------- Aufgabe 2c: begin/end ----------
    iterator       begin()       { return iterator(data_); }
    iterator       end()         { return iterator(data_ + size_); }  // one-past-the-end
    const_iterator begin() const { return const_iterator(data_); }
    const_iterator end()   const { return const_iterator(data_ + size_); }
};
```

Anmerkungen:

- Die Strategie „neuer Block + umziehen + alten zerstören" ersetzt `realloc`, denn `realloc` kopiert bitweise.
- Perfekt ausnahmesicher ist `reserve` noch nicht (wirft ein Move-Konstruktor mittendrin, leckt der neue Block). Mit `std::move_if_noexcept` und einem Aufräumblock ließe sich das verbessern, das geht über die Aufgabe hinaus.
- `new` darf laut Aufgabe ergänzend verwendet werden. Hier kommt es nur als *placement new* vor, der Speicher selbst kommt weiter von `malloc`.

---

### c) Test des `vector_iterator`

```cpp
// main.cpp
#include "vector.hpp"
#include <iostream>
#include <string>

int main()
{
    // int-Vektor, wächst mehrfach (4 -> 8 -> 16)
    vector<int> vi;
    for (int i = 0; i < 10; ++i) vi.push_back(i * i);

    std::cout << "vorwaerts:  ";
    for (vector<int>::iterator it(vi.begin()); it != vi.end(); ++it)
        std::cout << *it << ' ';

    std::cout << "\nrueckwaerts: ";
    for (vector<int>::iterator it(vi.end()); it != vi.begin(); )
        std::cout << *--it << ' ';

    vector<int>::iterator m(vi.begin());
    ++m; ++m;                                    // zeigt auf vi[2] == 4
    std::cout << "\nm[0]=" << m[0] << " m[3]=" << m[3] << " m[-1]=" << m[-1] << '\n';
    //          4               25 (vi[5])          1 (vi[1])

    // std::string: testet Konstruktion, Umkopieren, Destruktoren
    vector<std::string> vs;
    vs.push_back("kurz");
    vs.push_back(std::string(40, 'x'));          // länger als SSO-Puffer -> Heap
    vs.push_back("drei"); vs.push_back("vier");
    vs.push_back("fuenf");                       // erzwingt Wachstum
    vs.push_back(vs[0]);                         // Alias auf eigenes Element: push_back ist sicher

    for (vector<std::string>::iterator it(vs.begin()); it != vs.end(); ++it)
        std::cout << it->size() << ":" << *it << "  ";
    std::cout << '\n';

    vector<std::string> kopie(vs);               // Copy-Konstruktor
    std::cout << "kopie.size()=" << kopie.size() << '\n';

    const vector<int>& cv = vi;                  // const-Iteratoren
    for (auto it = cv.begin(); it != cv.end(); ++it) std::cout << *it << ' ';
    std::cout << '\n';
}
```

*Tipp:* Mit Address-Sanitizer (`-fsanitize=address`) bzw. Valgrind prüfen, dass es weder Lecks noch Zugriffsfehler gibt.

---

### d) Welche Iterator-Kategorie ist das?

Anforderungen aus der Vorlesung, abgeglichen mit `vector_iterator`:

| Kategorie / Konzept | Gefordert | Erfüllt? |
|---|---|---|
| Basis: Copy-konstruierbar, zuweisbar, zerstörbar, `++` | ja | ✔ |
| Input: `==`, `!=`, `*`, `->` (lesend) | ja | ✔ |
| Output: `*`, `->` (schreibend, nicht-const `T&`) | optional | ✔ (für nicht-const `T`) |
| Forward: default-konstruierbar, Mehrfach-Durchlauf | ja | ✔ (Default-Argument `p = nullptr`) |
| Bidirektional: `--` | ja | ✔ |
| Random-Access: `+`, `-`, `+=`, `-=`, Abstand `it - it`, `<`, `<=`, `>`, `>=` | ja | ✘ (nicht implementiert) |
| Zugriff `[offset]` | gehört zu Random-Access | ✔ (zusätzlich) |
| Contiguous-Memory (Array-Eigenschaft) | nur bei Random-Access | ✘ formal nicht |

**Einordnung:** Es ist ein **bidirektionaler Iterator** (mit Schreibzugriff, also auch Output-Iterator), der zusätzlich `operator[]` anbietet. Das `[]` ist etwas ungewöhnlich, weil es sonst erst bei Random-Access vorkommt. Zu einem *Random-Access-Iterator* fehlen die Arithmetik (`+`, `-`, `+=`, `-=`), die Abstandsberechnung und die Vergleichsoperatoren `<`, `<=`, `>`, `>=` (bzw. `<=>`). Da der `vector` ein Array mit gleich großen, aufeinanderfolgenden Einträgen ist, ließe sich der Iterator mit wenigen Zeilen zu einem *Random-Access-* bzw. *Contiguous-Memory-Iterator* ausbauen. Jeder dieser Operatoren ist nur eine Zeigeroperation auf `p_`.

---

### e) Aufgabe 2c in einer einzigen, einfachen Zeile

**Die richtige Idee:** Ein *normaler C-Zeiger* ist bereits ein vollwertiger Iterator! `*`, `->`, `++`, `--`, `[offset]` (relativ zum Zeiger), `==` und `!=` kann er alles schon. Man muss ihn nur *umbenennen*. Die ganze Klasse `vector_iterator` ersetzt eine Zeile:

```cpp
template <typename T> using vector_iterator = T*;
```

(Alternativ innerhalb der Klasse `vector`: `typedef T* iterator;` bzw. `using iterator = T*;`.)

Die restlichen Zeilen im `vector` bleiben gleich, denn `begin()` und `end()` liefern jetzt einfach die Zeiger:

```cpp
iterator begin() { return data_; }
iterator end()   { return data_ + size_; }
```

**Einordnung:** Ein Zeiger auf ein Array-Element ist ein **Contiguous-Memory-Iterator** (also auch Random-Access). Er unterstützt zusätzlich `+`, `-`, `+=`, `-=`, `it - it` und alle Vergleiche. Damit ist er sogar *mächtiger* als unsere handgeschriebene Klasse. (Der Standard selbst nutzt bei `std::vector` je nach Compiler eine dünne Hülle um einen Zeiger.)

**Nachteile des nackten Zeigers:**

- Der Iterator ist nicht vom normalen Zeiger zu unterscheiden. Das kann bei Überladungen verwirren.
- Es gibt keine Möglichkeit für Debug-Prüfungen (z. B. auf Gültigkeit oder Containerzugehörigkeit, vgl. 1d und 1f). Das ist ein Grund, warum Standardbibliotheken manchmal doch eine Klasse verwenden.

---

## Kurzzusammenfassung der Kernaussagen

| Aufgabe | Kernaussage |
|---|---|
| 1a | Templates werden pro ÜE mit konkreten Typen instanziiert. Die Definition muss deshalb im Header stehen, sonst gibt es einen *Linkerfehler*. |
| 1b | Mehrere unterschiedliche Template-Definitionen sind ein ODR-Verstoß, den der Linker nicht meldet. Das Ergebnis hängt von Linkreihenfolge und Optimierung ab. |
| 1c | Duplikate entschärft man durch schwache Symbole (COMDAT) oder explizite Instanziierung (`extern template`). |
| 1d/1e | Über `end()` hinaus zu iterieren ist UB. Es kann „funktionieren", ist aber nicht portabel. Debug-Builds prüfen, Release-Builds nicht. |
| 1f | Ein Iterator darf nur mit seinem eigenen Container benutzt werden. `list::erase` prüft das aus Effizienzgründen nicht. |
| 2a | `int` → `T`, Methoden im Header. |
| 2b | Rohen `malloc`-Speicher bevölkert man mit placement new und räumt ihn mit explizitem `~T()` ab. Statt `realloc`/`memcpy` wird umkonstruiert. |
| 2c/d | `vector_iterator` ist ein bidirektionaler Iterator mit `[]`, Random-Access fehlt formal. |
| 2e | `template <typename T> using vector_iterator = T*;` – ein Zeiger ist schon ein Contiguous-Memory-Iterator. |