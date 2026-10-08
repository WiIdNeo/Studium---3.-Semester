Hier sind 8 Aufgaben im gleichen Stil, grob nach Schwierigkeit sortiert. Die Fragen in den Aufzählungen sollst du dir beim Lösen bewusst beantworten, genau wie bei `Stack`.

---

## Aufgabe 1: Freie Funktionen mit Zeigern und Referenzen

Schreibe diese drei Funktionen (keine Klasse):

* `void swap_ints(int& a, int& b)` Vertauscht die Werte. Was passiert, wenn du `int a, int b` ohne Referenz benutzt?
* `bool min_max(const int* arr, int n, int& min, int& max)` Bestimmt Minimum und Maximum eines Arrays. Was gibst du bei `n <= 0` oder `arr == nullptr` zurück? Warum ist `const` bei `arr` sinnvoll?
* `void reverse(char* s, int n)` Dreht die ersten `n` Zeichen in-place um. Warum brauchst du hier keinen Rückgabewert und keinen zweiten Puffer?

---

## Aufgabe 2: Ringpuffer

Schreibe eine Klasse `RingBuffer` für `int`-Werte nach dem Prinzip First In, First Out mit fester Kapazität. Der Speicher wird mit `malloc` angelegt.

* `RingBuffer::RingBuffer(int capacity)` Was passiert bei `capacity <= 0` oder fehlgeschlagenem `malloc`?
* `bool RingBuffer::push(int v)` Hängt hinten an. Was passiert, wenn der Puffer voll ist?
* `bool RingBuffer::pop(int& out)` Entnimmt das *älteste* Element. Wie sorgst du dafür, dass die Indizes am Ende des Arrays wieder bei 0 beginnen (Stichwort Modulo)?
* `bool RingBuffer::empty()`, `bool RingBuffer::full()`, `int RingBuffer::size()`
* `RingBuffer::~RingBuffer()`

Denk darüber nach: Reicht es, `head` und `tail` zu speichern, um "leer" von "voll" zu unterscheiden? Was brauchst du zusätzlich?

---

## Aufgabe 3: Dynamisches Array

Schreibe eine Klasse `IntVector`, die automatisch wächst.

* `IntVector::IntVector()` Startet mit Kapazität 4.
* `bool IntVector::push_back(int v)` Wenn der Platz nicht reicht, verdoppelst du die Kapazität mit `realloc`. Was passiert mit dem alten Zeiger, wenn `realloc` `nullptr` zurückgibt? Warum darfst du das Ergebnis nicht direkt dem Member zuweisen?
* `bool IntVector::get(int index, int& out)` Was passiert bei einem ungültigen Index? Warum ist das besser als `operator[]` ohne Prüfung?
* `bool IntVector::pop_back(int& out)`
* `int IntVector::size()`, `int IntVector::capacity()`
* `IntVector::~IntVector()`

Zusatz: Was passiert bei `IntVector b = a;`? Lösche den Kopierkonstruktor und den Zuweisungsoperator mit `= delete`.

---

## Aufgabe 4: Eigene String-Klasse

Schreibe eine Klasse `MyString`, die ihren eigenen Speicher besitzt.

* `MyString::MyString(const char* s)` Kopiert den C-String. Wie viele Bytes musst du anlegen (Stichwort Nullterminator)? Was passiert bei `s == nullptr`?
* `MyString::MyString(const MyString& other)` Kopierkonstruktor. Warum reicht der vom Compiler erzeugte nicht aus (flache vs. tiefe Kopie)?
* `MyString& MyString::operator=(const MyString& other)` Was passiert bei `a = a;`? Wie schützt du dich davor?
* `int MyString::length() const`
* `bool MyString::append(const char* s)` Wie vergrößerst du den Speicher sicher?
* `const char* MyString::c_str() const` Warum gibst du `const char*` zurück und nicht `char*`?
* `MyString::~MyString()`

Das ist die "Rule of Three" in Reinform.

---

## Aufgabe 5: Einfach verkettete Liste

Schreibe eine Klasse `IntList` mit einer privaten Struktur `struct Node { int value; Node* next; };`

* `IntList::IntList()` Leere Liste.
* `bool IntList::push_front(int v)` Was passiert, wenn `new (std::nothrow)` fehlschlägt?
* `bool IntList::pop_front(int& out)` Wann musst du `delete` aufrufen, und in welcher Reihenfolge, damit du nicht auf freigegebenen Speicher zugreifst?
* `bool IntList::contains(int v) const`
* `bool IntList::remove(int v)` Entfernt das erste Vorkommen. Welche Sonderfälle gibt es (Kopf, Mitte, Ende, nicht gefunden)?
* `int IntList::size() const`
* `IntList::~IntList()` Gibt alle Knoten frei. Warum reicht ein einzelnes `delete head` nicht?

---

## Aufgabe 6: Matrix

Schreibe eine Klasse `Matrix` für `double`-Werte. Die Daten liegen in einem *einzigen* eindimensionalen Array (Zeile für Zeile).

* `Matrix::Matrix(int rows, int cols)` Initialisiert alle Werte mit 0. Was passiert bei `rows <= 0` oder `cols <= 0`? Wie berechnest du die Größe, ohne dass `rows * cols` überläuft?
* `bool Matrix::set(int r, int c, double v)` Wie rechnest du `(r, c)` in einen Index um?
* `bool Matrix::get(int r, int c, double& out) const`
* `bool Matrix::transpose()` Transponiert in-place oder mit neuem Speicher. Warum ist das bei nicht-quadratischen Matrizen schwieriger?
* `Matrix::~Matrix()`

---

## Aufgabe 7: Bitset

Schreibe eine Klasse `BitSet`, die `n` einzelne Bits in einem `unsigned char`-Array speichert.

* `BitSet::BitSet(int nbits)` Wie viele Bytes brauchst du für `nbits` Bits (Aufrunden)?
* `bool BitSet::set(int i)` und `bool BitSet::clear(int i)` Wie bestimmst du Byte und Bitposition? Welche Operatoren brauchst du (`|`, `&`, `~`, `<<`)?
* `bool BitSet::test(int i, bool& out) const`
* `int BitSet::count() const` Wie viele Bits sind gesetzt?
* `BitSet::~BitSet()`

Warum ist ein Rückgabewert `bool` bei `test` problematisch, wenn auch ein Fehlerfall möglich ist?

---

## Aufgabe 8: Klammerprüfung (nutzt deinen Stack)

Schreibe eine freie Funktion `bool balanced(const char* s)`, die mit Hilfe deiner `Stack`-Klasse prüft, ob `()`, `[]` und `{}` korrekt geschachtelt sind.

* Beispiele: `"{[()]}"` → `true`, `"([)]"` → `false`, `"(("` → `false`, `")"` → `false`, `""` → `true`
* Welche Kapazität muss der Stack mindestens haben? (Tipp: `strlen`)
* Was machst du, wenn der Stack bei einer schließenden Klammer leer ist?
* Was prüfst du am Ende, nachdem der String abgearbeitet ist?
* Was machst du, wenn der Stack-Konstruktor fehlschlägt (Kapazität 0 bei leerem String)?

---

**Reihenfolge-Tipp:** Aufgaben 1 und 8 sind gut zum Aufwärmen, 2, 5, 6 und 7 trainieren Speicherverwaltung und Indexlogik, 3 und 4 sind am anspruchsvollsten (`realloc`, Rule of Three).

Wenn du Lösungen hast, schick sie gern rüber, dann gehe ich sie wie bei `Stack` durch.