# Zusätzliche Übungsaufgaben: Objektorientierte Programmierung in C++

Die Aufgaben sind im Stil von Übung 3 (Aufgabe 2, Praxis) gehalten und bauen grob aufeinander auf. Teile jede Klasse in `.hpp` und `.cpp` auf, benutze Include-Guards, `const`-Korrektheit und Initialisierungslisten. Kompiliere mit `g++ -std=c++17 -Wall -Wextra -Wpedantic`.

Mit **(*)** markierte Aufgaben sind schwieriger.

---

## Aufgabe 1: Konstruktoren und Kapselung

Schreibe eine Klasse `bank_account`.

- Ein Konto hat eine Kontonummer (`std::string`), einen Inhaber (`std::string`) und einen Kontostand in Cent (`long long`).
- Man kann ein Konto mit Nummer und Inhaber anlegen (Kontostand 0) oder zusätzlich mit einem Startguthaben.
- `einzahlen(betrag)` erhöht den Kontostand, `abheben(betrag)` verringert ihn.
- Der Kontostand darf nie negativ werden. `abheben` gibt `true` zurück, wenn es geklappt hat, sonst `false` und der Stand bleibt unverändert. Negative Beträge werden abgelehnt.
- Der Kontostand lässt sich von außen nur lesen, nicht setzen.
- `ueberweisen(ziel, betrag)` bucht von diesem Konto auf ein anderes Konto um.

**Test:** Lege zwei Konten an, überweise Beträge hin und her und versuche, mehr abzuheben als vorhanden ist. Gib nach jedem Schritt beide Kontostände aus.

---

## Aufgabe 2: Rule of Three

Erstelle eine Klasse `int_array` mit folgenden Eigenschaften:

- Sie verwaltet ein dynamisch angelegtes `int`-Array mit einer beim Anlegen angegebenen Größe. Alle Elemente starten mit 0.
- `get(i)` und `set(i, wert)` greifen auf Elemente zu. Bei ungültigem Index wird eine `std::out_of_range`-Exception geworfen.
- `size()` gibt die Anzahl der Elemente zurück.
- Kopieren ist **tief**.
- Kein Speicherleck beim Löschen.
- Jeder Konstruktor, der Destruktor und jede Zuweisung gibt den eigenen Namen auf der Konsole aus.

Implementiere Destruktor, Kopierkonstruktor und Kopierzuweisungsoperator.

**Fragen:**

1. Was passiert bei `a = a;`, wenn man die Selbstzuweisung nicht abfängt?
2. Was passiert, wenn der Kopierzuweisungsoperator zuerst den alten Speicher löscht und das anschließende `new` eine Exception wirft?
3. Wie sieht die Lösung mit dem Copy-and-Swap-Idiom aus?

**Test:**

```cpp
int_array a(5);
a.set(2, 42);
int_array b(a);        // Kopierkonstruktor
int_array c(3);
c = a;                 // Kopierzuweisung
b.set(2, 7);
std::cout << a.get(2) << " " << b.get(2) << " " << c.get(2) << '\n';  // 42 7 42
a = a;                 // darf nichts kaputt machen
```

---

## Aufgabe 3 (*): Rule of Five

Erweitere `int_array` um **Move-Konstruktor** und **Move-Zuweisung**.

- Nach dem Verschieben muss das Quellobjekt in einem gültigen, löschbaren Zustand sein (zum Beispiel Größe 0, Zeiger `nullptr`).
- Markiere beide mit `noexcept`.
- Schreibe eine Funktion `int_array make_array(int n)`, die ein Array erzeugt und zurückgibt, und beobachte anhand der Konsolenausgaben, welche Konstruktoren aufgerufen werden. Probiere auch `std::move` explizit aus.

**Fragen:**

1. Warum ist `noexcept` bei Move-Operationen wichtig, wenn man das Objekt später in einem `std::vector` ablegt?
2. Was ist die *Rule of Zero* und wie könnte man `int_array` mit `std::vector<int>` oder `std::unique_ptr<int[]>` so schreiben, dass man keine der fünf Methoden selbst braucht?

---

## Aufgabe 4: Einfach verkettete Liste

Schreibe eine Klasse `int_list` für eine einfach verkettete Liste. Die Knoten sind eine eigene Struktur `node` mit einem `int` und einem Zeiger auf den Nachfolger. Die Liste merkt sich nur den Zeiger auf den ersten Knoten (`head`).

- `push_front(wert)` fügt vorne ein, `push_back(wert)` hinten.
- `pop_front()` entfernt den ersten Knoten.
- `remove(wert)` entfernt den ersten Knoten mit diesem Wert und gibt zurück, ob einer gefunden wurde.
- `contains(wert)`, `size()` und `print()`.
- `reverse()` dreht die Liste **in place** um. Es werden keine neuen Knoten angelegt, nur die Zeiger umgehängt.
- Kein Speicherleck, Kopieren ist tief.

**Test:** Füge Werte vorne und hinten ein, entferne den ersten, einen mittleren, den letzten und einen nicht vorhandenen Wert. Rufe `reverse()` auf. Prüfe mit `valgrind --leak-check=full` oder `-fsanitize=address`, dass nichts verloren geht.

**Frage:** Warum ist `push_back` hier O(n)? Welche Änderung an der Klasse macht es O(1)?

---

## Aufgabe 5: Doppelt verkettete Liste mit Iterator (*)

Verallgemeinere die Liste aus Aufgabe 4 zu einer Template-Klasse `list<T>` mit doppelter Verkettung (Zeiger `prev` und `next`, Zeiger auf `head` und `tail`).

- `push_front`, `push_back`, `pop_front`, `pop_back`, `size`, `empty`.
- `insert_after(iterator, wert)` und `erase(iterator)`.
- Eine verschachtelte Klasse `iterator` mit `operator*`, `operator++`, `operator!=` bzw. `operator==`. Dazu `begin()` und `end()`.

**Ziel:** Folgende Schleife soll funktionieren:

```cpp
list<std::string> l;
l.push_back("a");
l.push_back("b");
for (const auto& s : l) {
    std::cout << s << '\n';
}
```

**Hinweis:** Template-Klassen müssen komplett im Header stehen (oder die Definitionen in einer `.tpp`-Datei, die am Ende des Headers eingebunden wird). Überlege, warum das so ist.

---

## Aufgabe 6: Stack und Queue auf Basis der Liste

Baue auf deiner Liste aus Aufgabe 4 oder 5 auf.

a) `stack` mit `push`, `pop`, `top`, `empty`. Löse damit: Prüfe, ob in einem String alle Klammern `()[]{}` korrekt geschachtelt sind.

b) `queue` mit `enqueue`, `dequeue`, `front`, `empty`. Simuliere damit eine Warteschlange an einer Kasse: Kunden kommen zufällig an (`std::mt19937`), jeder braucht eine zufällige Bedienzeit. Gib die durchschnittliche Wartezeit aus.

c) **Komposition oder Vererbung?** Schreibe `stack` einmal so, dass es eine Liste als privates Member **enthält**, und einmal so, dass es von der Liste **erbt**. Diskutiere, warum die Komposition hier die bessere Wahl ist (Stichwort: Schnittstelle, die man nicht nach außen geben will).

---

## Aufgabe 7: Vererbung und Polymorphie

Erstelle eine Klassenhierarchie für Formen.

- Abstrakte Basisklasse `shape` mit den rein virtuellen Methoden `area() const`, `perimeter() const` und `print() const`.
- Abgeleitete Klassen `circle`, `rectangle` und `triangle` (über drei Seitenlängen, mit Prüfung der Dreiecksungleichung im Konstruktor).
- Die Basisklasse bekommt einen **virtuellen Destruktor**.
- Lege in `main` einen `std::vector<std::unique_ptr<shape>>` mit gemischten Formen an. Gib alle aus, berechne die Gesamtfläche und finde die Form mit dem größten Umfang.

**Fragen:**

1. Was passiert beim Löschen über einen `shape*`, wenn der Destruktor **nicht** virtuell ist?
2. Was ist *Slicing* und wie lässt es sich in dieser Aufgabe provozieren (`std::vector<shape>` statt Zeiger)?
3. Wozu dient das Schlüsselwort `override` und welchen Fehler fängt es ab?
4. Wie funktioniert der Aufruf einer virtuellen Methode intern (vtable)? Passt das zur Branch-Prediction-Diskussion aus Aufgabe 1d?

---

## Aufgabe 8: Operatoren überladen

Schreibe eine Klasse `fraction` für Brüche.

- Zähler und Nenner als `int`. Der Bruch wird nach jeder Operation gekürzt (`std::gcd`), das Vorzeichen steht immer im Zähler. Nenner 0 ist verboten (Exception).
- `+`, `-`, `*`, `/` als Operatoren, dazu `+=`, `-=`, `*=`, `/=`.
- Vergleichsoperatoren `==`, `<`, und was daraus folgt (in C++20: `operator<=>`).
- `operator<<` zur Ausgabe, zum Beispiel `3/4`.
- Implizite Konvertierung von `int` zu `fraction`, sodass `fraction(1,2) + 3` funktioniert.

**Fragen:**

1. Warum implementiert man `operator+` meist als freie Funktion und `operator+=` als Member?
2. Warum muss `operator<<` eine freie Funktion sein?
3. Wann ist `explicit` am Konstruktor sinnvoll, und was geht damit bei `fraction(1,2) + 3` verloren?

---

## Aufgabe 9: Smart Pointer selbst bauen

Gehe zurück zu `int_smart_pointer` aus Übung 3 und verallgemeinere:

a) `unique_ptr`-Nachbau `my_unique<T>`: Kopieren verboten (`= delete`), Verschieben erlaubt. `get()`, `operator*`, `operator->`, `release()`, `reset()`.

b) (*) `shared_ptr`-Nachbau `my_shared<T>`: Alle Kopien teilen sich dasselbe Objekt und einen gemeinsamen **Referenzzähler** auf dem Heap. Das Objekt wird gelöscht, wenn der letzte `my_shared` verschwindet. `use_count()` gibt den aktuellen Zähler zurück.

c) Provoziere mit `my_shared` einen **Zyklus** (zwei Objekte zeigen mit `my_shared` aufeinander). Was passiert beim Beenden? Wie löst `std::weak_ptr` das Problem?

**Zusammenhang:** Vergleiche das mit der flachen Kopie aus Übung 3, Aufgabe 2c. Der Referenzzähler ist genau die Antwort auf das dort entstehende Problem.

---

## Aufgabe 10 (*): Hasenstall mit Smart Pointern

Schreibe den Hasenstall aus Übung 3, Aufgabe 2e neu, **ohne** ein einziges `new` und `delete`.

- Die Rechte Hand ist ein `std::unique_ptr<rabbit>` (der Besitzer), die linke Hand ein normaler Rohzeiger `rabbit*` (nur Beobachter, kein Besitz).
- Der Stall hält `std::unique_ptr<rabbit> first`.

**Fragen:**

1. Warum darf die linke Hand kein `unique_ptr` sein?
2. Der Destruktor der Kette löscht rekursiv: Jeder Hase löscht seinen rechten Nachbarn. Was passiert bei sehr langen Ketten (Stack Overflow)? Wie vermeidest du das mit einem eigenen Destruktor des Stalls, der die Kette iterativ abbaut?
3. Wie änderst du `ernten`, damit ein Hase aus der Mitte entfernt werden kann, ohne dass der Besitz verloren geht? Tipp: `std::move` und Umhängen der Besitzer-Zeiger.

---

## Aufgabe 11: Header, Linker und ODR

Du bekommst folgendes Projekt:

```cpp
// util.hpp
int square(int x) { return x * x; }

// a.cpp
#include "util.hpp"
// ...

// b.cpp
#include "util.hpp"
// ...
```

a) Was meldet der Linker? Gib mindestens drei verschiedene Lösungen an (`inline`, Definition in `.cpp`, `static`) und diskutiere die Unterschiede.

b) Was ändert sich, wenn `square` stattdessen eine **Klassenmethode** ist, die in der Klassendefinition im Header steht? Und wenn sie außerhalb der Klasse im Header definiert wird?

c) Warum funktioniert folgender Code bei einem Header **ohne** Include-Guard nicht, obwohl jede Datei den Header scheinbar nur einmal einbindet?

```cpp
// main.cpp
#include "a.hpp"   // bindet intern shape.hpp ein
#include "b.hpp"   // bindet intern ebenfalls shape.hpp ein
```

d) Untersuche mit `nm -C datei.o` (Linux/Mac) oder `dumpbin /symbols` (Windows), welche Symbole in den Objektdateien liegen und welche als `W` (weak) oder `T` markiert sind. Erkläre den Unterschied zwischen starken und schwachen Symbolen.

---

## Aufgabe 12: Mini-Projekt – Bibliothek

Kombiniere die Techniken in einem kleinen Projekt mit mehreren Dateien.

- Klasse `book` (Titel, Autor, ISBN, ausgeliehen ja/nein).
- Klasse `member` (Name, Mitgliedsnummer, Liste der ausgeliehenen Bücher).
- Klasse `library` verwaltet Bücher und Mitglieder. Sie besitzt die Bücher (`std::vector<std::unique_ptr<book>>`), Mitglieder halten nur nicht besitzende Zeiger.
- Funktionen: `book_hinzufuegen`, `mitglied_anlegen`, `ausleihen(isbn, mitglied)`, `zurueckgeben(isbn)`, `suchen(autor)`, `inventarisieren`.
- Regeln: Maximal 3 Bücher pro Mitglied, ein Buch ist nur einmal gleichzeitig ausleihbar.
- Fehlerfälle werden durch Exceptions oder Rückgabewerte sauber gemeldet.

**Test:** Schreibe eine `main`, die ein Szenario durchspielt, einschließlich aller Fehlerfälle, und nach jedem Schritt den Zustand ausgibt.

---

## Tipps zum Üben

- Kompiliere immer mit `-Wall -Wextra -fsanitize=address,undefined`. Das findet Speicherfehler, die sonst nur manchmal auffallen.
- Schreibe zuerst den Test (`main`), dann die Klasse. So überlegst du dir die Schnittstelle, bevor du Details festlegst.
- Gib in Konstruktoren, Destruktoren und Zuweisungen testweise etwas aus, um zu sehen, wann Kopien und Verschiebungen wirklich passieren.
- Zeichne Zeigerstrukturen (Listen, Ketten) auf Papier, bevor du sie codest, besonders bei Einfügen und Löschen.