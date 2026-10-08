# Übungsaufgaben C++: dynamischer Speicher und Klassen

Alle Aufgaben im Stil des string-Übungsblatts. Löse sie **auf Papier**, ohne Compiler.

**Regeln für alle Aufgaben**
- Nur `malloc`, `realloc`, `free` (kein `new`/`delete`, keine `std::`-Container, kein `strlen`/`strcpy`/`memcpy`).
- Aufteilung in Header (`.hpp`) und Quelldatei (`.cpp`).
- Dokumentiere im Header die Spezialfälle für den Klassennutzer.
- Schreibe am Ende eine `main` mit Tests für Spezial- und Randfälle.

**Vorgehen (so wie beim string)**
1. Funktionsköpfe aus der Aufgabe abschreiben (Klassengerüst).
2. Fragen: Was muss sich die Klasse merken? (Member-Variablen) Welche Invariante soll immer gelten?
3. Jede Funktion mit Zahlenbeispiel auf Papier durchspielen (Kästchen zeichnen).
4. Checkliste unten abarbeiten.

---

## Aufgabe 1: Dynamisches int-Array (`IntArray`)

Schreibe eine Klasse `IntArray`, die beliebig viele `int`-Werte speichert und bei Bedarf wächst.

- `IntArray::IntArray()`
  Konstruiert ein leeres Array.
  *Wie viele Elemente und wie viel Kapazität hat es? Darf der interne Zeiger `nullptr` sein?*
- `void IntArray::push_back(int value)`
  Hängt einen Wert hinten an.
  *Wann muss `realloc` aufgerufen werden? Warum ist es ungeschickt, bei jedem Anhängen um genau 1 zu vergrößern? Überlege, wie eine Kapazitätsverdopplung funktioniert.*
- `int IntArray::get(int index)`
  Liefert das Element an Position `index`.
  *Was soll bei einem ungültigen Index passieren (negativ, zu groß)? Welchen Rückgabewert wählst du, und wie dokumentierst du es?*
- `int IntArray::size()`
  Anzahl der gespeicherten Elemente. *Ist das dasselbe wie die Kapazität?*
- `int IntArray::find(int value)`
  Index des ersten Vorkommens oder ein Wert für "nicht gefunden". *Warum ist hier der Wert -1 problematisch, wenn man auch negative Zahlen speichern darf?*
- `void IntArray::clear()`
  Entfernt alle Elemente. *Muss der Speicher freigegeben werden, oder reicht es, die Anzahl auf 0 zu setzen? Was sind die Vor- und Nachteile?*
- `IntArray::~IntArray()`
  Gibt den Speicher frei. *Darf `free(nullptr)` aufgerufen werden?*

**Tests:** leeres Array, 1 Element, über die Kapazitätsgrenze hinaus anhängen (z. B. 100 Elemente), `get` mit Index -1, 0, `size()-1`, `size()`, `find` bei Mehrfachvorkommen, `clear` und danach wieder `push_back`.

---

## Aufgabe 2: Stapel (`Stack`)

Schreibe eine Klasse `Stack` für `char`-Werte nach dem Prinzip *Last In, First Out*. Der Stapel hat eine **feste** Kapazität, die dem Konstruktor übergeben wird.

- `Stack::Stack(int capacity)`
  Legt Speicher für `capacity` Zeichen an.
  *Was passiert bei `capacity <= 0`? Was bei einem fehlgeschlagenen `malloc`?*
- `bool Stack::push(char c)`
  Legt `c` oben auf den Stapel. *Was gibst du zurück, wenn der Stapel voll ist? Warum ist ein Rückgabewert hier besser als ein stiller Fehler?*
- `bool Stack::pop(char& out)`
  Entfernt das oberste Element und schreibt es nach `out`. *Warum wird hier eine Referenz benutzt und kein Rückgabewert `char`? Was passiert bei einem leeren Stapel?*
- `bool Stack::empty()` und `bool Stack::full()`
- `int Stack::size()`
- `Stack::~Stack()`

**Anwendung (kleine Zusatzaufgabe):** Schreibe mit dem Stack eine freie Funktion `bool klammernOk(const char* text)`, die prüft, ob alle Klammern `()`, `[]`, `{}` in `text` korrekt geschachtelt sind. Beispiele: `"([]{})"` → true, `"(]"` → false, `"(("` → false.

**Tests:** `pop` auf leerem Stapel, `push` auf vollem Stapel, Reihenfolge der Entnahme (`a`, `b`, `c` → `c`, `b`, `a`), Kapazität 1, Kapazität 0.

---

## Aufgabe 3: Kopieren absichern (Rule of Three für `string`)

Nimm deine fertige `string`-Klasse. Aktuell würde `string b = a;` nur den Zeiger kopieren.

a) **Zeige das Problem.** Spiele auf Papier durch, was bei folgendem Code passiert, wenn man nichts ergänzt:

```cpp
{
    string a("Hallo");
    string b = a;
}
```

*Wohin zeigen `a.text` und `b.text`? Was passiert am Ende des Blocks?*

b) Schreibe den **Kopierkonstruktor** `string::string(const string& other)`, der eine tiefe Kopie anlegt.
*Warum muss der Parameter eine Referenz sein? Was würde bei Übergabe per Wert passieren?*

c) Schreibe den **Zuweisungsoperator** `string& string::operator=(const string& other)`.
*Was muss mit dem alten Speicher von `this` geschehen? Was passiert bei der Selbstzuweisung `a = a;`, und wie fängst du sie ab? Warum ist die Reihenfolge "erst freigeben, dann kopieren" gefährlich?*

d) Beantworte schriftlich: Warum sollte man bei einer Klasse mit eigenem Destruktor fast immer auch Kopierkonstruktor und Zuweisungsoperator schreiben?

**Tests:** Kopie eines normalen Strings, Kopie eines leeren Strings, Änderung der Kopie (darf das Original nicht verändern), `a = b`, `a = a`, Kette `a = b = c`.

---

## Aufgabe 4: C-String-Funktionen selbst schreiben

Schreibe die folgenden **freien Funktionen** (keine Klasse) mit `const char*` und `char*`. Verboten sind alle Funktionen aus `<cstring>`.

- `std::size_t laenge(const char* s)`
  *Was liefert die Funktion bei `nullptr`?*
- `int vergleiche(const char* a, const char* b)`
  Liefert 0 bei Gleichheit, einen negativen Wert, wenn `a` lexikographisch vor `b` steht, sonst einen positiven. *Wie vergleichst du `"ab"` mit `"abc"`? Wie gehst du mit `nullptr` um?*
- `char* kopie(const char* s)`
  Legt mit `malloc` eine Kopie an und gibt sie zurück. *Wer ist für das `free` verantwortlich? Wie dokumentierst du das?*
- `char* verbinde(const char* a, const char* b)`
  Neuer String mit `a` gefolgt von `b`. *Wie viele Byte brauchst du? Was passiert, wenn eines der beiden `nullptr` ist?*
- `char* umkehren(const char* s)`
  Neuer String mit umgekehrter Zeichenfolge (`"abc"` → `"cba"`).
- `int zaehle(const char* s, char c)`
  Wie oft kommt `c` vor? *Was ist das Ergebnis für `c == '\0'`?*

**Tests:** leerer String, `nullptr`, ein Zeichen, gleiche Strings, Strings mit Präfix (`"ab"`/`"abc"`), Rückgabewerte von `kopie`/`verbinde`/`umkehren` jeweils mit `free` aufräumen.

---

## Aufgabe 5: Ringpuffer (`RingBuffer`)

Ein Ringpuffer speichert höchstens `capacity` Werte. Wenn er voll ist, wird beim Einfügen der **älteste** Wert überschrieben. Typisch für Sensordaten und Logs.

- `RingBuffer::RingBuffer(int capacity)`
  Legt den Speicher an. *Welche Member brauchst du außer dem Zeiger? Tipp: Position zum Schreiben, Position zum Lesen, Anzahl.*
- `void RingBuffer::push(int value)`
  Fügt einen Wert ein, überschreibt bei vollem Puffer den ältesten. *Wie kommst du mit dem Operator `%` immer wieder auf Index 0 zurück?*
- `bool RingBuffer::pop(int& out)`
  Entnimmt den ältesten Wert. *Was passiert, wenn der Puffer leer ist?*
- `int RingBuffer::size()`, `bool RingBuffer::empty()`, `bool RingBuffer::full()`
- `int RingBuffer::at(int i)`
  Der `i`-te Wert, gezählt ab dem **ältesten**. *Wie rechnest du den logischen Index `i` in den echten Index im Array um?*
- `RingBuffer::~RingBuffer()`

**Tests:** Kapazität 3 mit 5 Werten füllen (`1,2,3,4,5` → übrig bleiben `3,4,5`), `pop` bis leer, `pop` auf leerem Puffer, `push` nach vollständigem Leeren, Kapazität 1.

---

## Checkliste zum Abhaken (nach jeder Aufgabe)

- [ ] `public:` vor den Funktionen, `;` hinter der Klasse
- [ ] `ClassName::` vor jedem Namen in der `.cpp`
- [ ] Include-Guard im Header, eigene Header mit `"..."`
- [ ] Jedes `malloc` hat genau ein passendes `free`
- [ ] `realloc` immer über eine temporäre Variable
- [ ] Größe berechnet: `+ 1` für `'\0'` bei Strings
- [ ] Länge bedeutet überall dasselbe (ohne `'\0'`)
- [ ] `==` statt `=` in Bedingungen
- [ ] Vor jedem Dereferenzieren: kann der Zeiger `nullptr` sein?
- [ ] Schleifengrenzen geprüft (`<` oder `<=`?)
- [ ] Indizes mit Zahlenbeispiel nachgezählt
- [ ] Destruktor nicht selbst aufgerufen
- [ ] Kopieren ist geregelt (verboten oder implementiert)
- [ ] Alle Randfälle in `main` getestet

---

## Lösungshinweise (erst nach dem eigenen Versuch lesen)

**Aufgabe 1**
- Leeres Array: `data = nullptr`, `size = 0`, `capacity = 0` ist erlaubt, weil `realloc(nullptr, n)` wie `malloc(n)` arbeitet und `free(nullptr)` harmlos ist.
- Wachstum: Wenn `size == capacity`, neue Kapazität `capacity == 0 ? 4 : capacity * 2`. Dadurch ist das Anhängen im Durchschnitt billig.
- `find`: `-1` ist mehrdeutig nur bei `get`, nicht bei `find` (ein Index ist nie negativ). Bei `get` ist der Rückgabewert dagegen ein Problem, weil `-1` ein gültiger gespeicherter Wert sein kann. Besser: `bool get(int index, int& out)`.
- `clear`: Anzahl auf 0 setzen reicht und ist schneller, der Speicher bleibt für spätere Nutzung reserviert.

**Aufgabe 2**
- `pop(char& out)`: Mit der Referenz kann die Funktion gleichzeitig "geklappt/nicht geklappt" (Rückgabewert) und den Wert (Parameter) liefern. Ein reiner `char`-Rückgabewert hätte keinen freien Wert für "leer".
- Klammerprüfung: Öffnende Klammer → `push`. Schließende Klammer → `pop` und prüfen, ob sie passt (bei leerem Stapel: false). Am Ende muss der Stapel leer sein. Kapazität = Länge des Textes reicht.

**Aufgabe 3**
- Ohne Ergänzung zeigen beide Zeiger auf denselben Block, und am Blockende geben beide Destruktoren ihn frei: **Double Free**.
- Kopierkonstruktor: Länge übernehmen, neuen Block holen, Zeichen kopieren. Parameter per Referenz, weil sonst zum Übergeben bereits eine Kopie nötig wäre, also Endlosrekursion.
- Zuweisung: Zuerst `if (this == &other) return *this;`. Dann neuen Block mit der Kopie anlegen, **danach** den alten freigeben und umhängen. Am Ende `return *this;`. Bei der Selbstzuweisung ohne Prüfung würde man den Block freigeben, aus dem man gleich kopieren will.
- Regel (Rule of Three): Braucht eine Klasse einen eigenen Destruktor, verwaltet sie eine Ressource, und dann ist die Standardkopie (Zeiger kopieren) falsch.

**Aufgabe 4**
- `vergleiche`: Schleife, solange beide Zeichen gleich und nicht `'\0'` sind. Rückgabe: Differenz der ersten ungleichen Zeichen (als `unsigned char`). Bei `"ab"` gegen `"abc"` steht links `'\0'` gegen `'c'`, also negativ.
- `verbinde`: Länge `la + lb + 1` Byte. Ein `nullptr` zählt als `""`.
- `umkehren`: Ziel an Index `i` bekommt `s[n - 1 - i]`, danach `'\0'` an Index `n`.
- `zaehle` mit `'\0'`: Gibt 0 zurück, da das Terminierungszeichen nicht zum Inhalt gehört (konsistent mit `find` im string).

**Aufgabe 5**
- Member: `data`, `capacity`, `head` (Leseposition), `count`. Die Schreibposition ist `(head + count) % capacity`.
- `push`: Ist `count == capacity`, überschreibe an `head` und setze `head = (head + 1) % capacity`, sonst `count++`.
- `pop`: Wert bei `head` lesen, `head = (head + 1) % capacity`, `count--`.
- `at(i)`: echter Index ist `(head + i) % capacity`.