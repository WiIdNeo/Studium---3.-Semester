# Kurzübersicht: Grundlagen C und C++

Die Vorlesung/Übung 2 behandelt fünf große Themenblöcke:

1. **C und C++ im Überblick** – Geschichte, Stärken/Schwächen im Vergleich zu anderen Sprachen.
2. **Compiler-Pipeline** – Jede Übersetzungseinheit (Quellcodedatei) wird einzeln vom **Compiler** zu Maschinencode (Objektdatei) übersetzt; der **Linker** löst anschließend die Verweise zwischen den Objektdateien auf und baut daraus das ausführbare Programm.
3. **Programmaufbau** – Trennung von **Headerdateien** (Schnittstelle: Klassennamen, Signaturen, Member) und **Quellcodedateien** (Implementierung). Der **Präprozessor** fügt `#include`-Inhalte rein textuell ein, bevor überhaupt kompiliert wird. **Inclusion Guards** verhindern Mehrfachdefinitionen durch doppeltes Einbinden.
4. **Werte und Zeiger** – Adress-Operator `&`, Dereferenzierung `*`, mehrstufige Zeiger, Typprüfung, **undefiniertes Verhalten** bei ungültigen Zeigerzugriffen.
5. **Stack und Heap** – Stack: automatische, schnelle, aber begrenzte Speicherverwaltung; Heap: manuelle Verwaltung via `new`/`delete`, Gefahr von Speicherlecks und Use-after-free.

Jetzt zu den Aufgaben, inklusive Rückmeldung zu deinen Notizen:

---

## Aufgabe 1 – Allgemeine Grundlagen

### a) Reflexion deiner Antworten

- **Lokal vs. global** ✅ Richtig.
- **Array vs. Liste** ✅ Im Kern richtig: Array = feste Größe, aber O(1)-Zugriff; Liste (z. B. verkettete Liste) = dynamische Größe, dafür nur sequenzieller Zugriff (O(n)), da man sich von Knoten zu Knoten hangeln muss.
- **Funktion vs. Methode** ✅ Richtig, ggf. ergänzen: Methoden haben stets impliziten Zugriff auf `this`/das Objekt.
- **Instanzvariable vs. Klassenvariable** ⚠️ Leicht ungenau. Besser: Eine **Klassenvariable** (`static`) gehört zur Klasse selbst und existiert nur **einmal**, unabhängig davon, wie viele Objekte erzeugt wurden. Eine **Instanzvariable** gehört zu einem konkreten Objekt – jede Instanz hat ihre **eigene Kopie**.
- **Fehlend:** `return x` vs. `throw x` – `return` beendet die Methode regulär und gibt den Kontrollfluss an den Aufrufer zurück (der Aufrufer erwartet den Rückgabewert). `throw` beendet die Methode **irregulär**: der Kontrollfluss "springt" den Call-Stack hinauf bis zu einem passenden `catch`-Block, überspringt dabei alle Zwischen-Rückgabewerte und -Aufrufer, die die Exception nicht behandeln.

### b) Sprachwahl (nicht beantwortet – hier ein Vorschlag)

| Szenario | Empfehlung | Begründung |
|---|---|---|
| MoneyMatters Highscore-Server | **Java/C#** | Netzwerkdienst mit Sicherheitsanforderungen; verwaltete Sprache mit Speichersicherheit reduziert Angriffsfläche (keine Pufferüberläufe), Team aus Neulingen profitiert von Robustheit & guter Fehlerdiagnose. |
| GrollCollect (Gesundheitskasse) | **C++ oder C#** | Hohe Integrationsanforderungen, knappe Zeit, aber erfahrenes Team und großes Budget – Skalierung & Struktur wichtiger als Robustheit. |
| JCM-Jacuzzi (ATmega, 2 KB RAM) | **C** | Extrem ressourcenbeschränkte Hardware, kein Platz für Laufzeit-Overhead von C++/OOP; C bietet maximale Kontrolle über Speicher & Effizienz. |
| Personal Perfection App (KI lokal auf Handy) | **C++** | Rechenintensive KI muss lokal auf begrenzter Mobil-Hardware laufen – Effizienz und Kontrolle über Speicher sind entscheidend, komplexe Struktur (KI-Logik) spricht für OOP. |
| Flibbers & Snoggles Basisanwendung | **Java/C#** | Plattformübergreifend (Desktop + Mobile), viele externe, fachlich unversierte Entwickler schreiben Importmodule → Robustheit und einfache Erlernbarkeit wichtiger als rohe Geschwindigkeit. |

---

## Aufgabe 2 – Compilerpipeline

### a) Reflexion

Deine Antwort ist im Kern richtig, aber der Linker "kompiliert" nichts – er **löst Verweise auf**, ohne selbst zu kompilieren. Präzisere Formulierung:

> Der Compiler übersetzt jede Übersetzungseinheit (Quellcodedatei) unabhängig von den anderen in Maschinencode (Objektdatei). Aufrufe von Funktionen/Variablen aus anderen Einheiten bleiben dabei als offene Referenzen (Symbole) bestehen, deren Existenz nur anhand der Header semantisch geprüft wurde. Der Linker verknüpft anschließend alle Objektdateien zu einem einzigen Programm, indem er diese offenen Referenzen durch die tatsächlichen Adressen der jeweils anderen Objektdatei ersetzt.

### b) Zyklische Abhängigkeit — Korrektur

"Diamond of Doom" trifft die Frage nicht. Die eigentliche Antwort:

**Problem:** Der Compiler übersetzt Übersetzungseinheiten einzeln und nacheinander. Verwenden zwei Einheiten A und B wechselseitig Inhalte voneinander, bräuchte der Compiler beim Übersetzen von A bereits vollständiges Wissen über B – aber B ist zu diesem Zeitpunkt noch gar nicht übersetzt (und umgekehrt). Es entsteht ein Henne-Ei-Problem, das sich nicht direkt auflösen lässt.

**Lösung:** Man trennt Deklaration (Header) von Definition (Quelldatei) und nutzt **Vorwärtsdeklarationen** (`class X;`). Der Compiler braucht beim Übersetzen oft nur die Deklaration (z. B. für Zeiger/Referenzen als Parameter), nicht die vollständige Definition. Die tatsächliche Verknüpfung der Implementierungen erfolgt dann beim Linken, wenn beide Objektdateien bereits vorliegen.

---

## Aufgabe 3 – Headerdateien (nicht beantwortet)

**a) Nutzen von Headerdateien:** Header stellen die *Schnittstelle* einer Übersetzungseinheit bereit, ohne die Implementierung preiszugeben. Andere Dateien können per `#include` die Signaturen (Klassennamen, Member, Methoden) einlesen und so vom Compiler semantisch geprüft werden, ohne dass die komplette Implementierung mitkompiliert werden muss. In den Header gehören: Klassendeklarationen, Membervariablen, Methodensignaturen, Typedefs, Namensräume. In die `.cpp` gehört möglichst viel: die eigentlichen Methodenimplementierungen.

**b) Doppelt vergebener Inclusion-Guard-Name:** Das wird erst sichtbar, wenn **zwei verschiedene Header** (aus unterschiedlichen Projekten/Bibliotheken) zufällig denselben Guard-Namen verwenden **und beide in derselben Übersetzungseinheit eingebunden werden** (direkt oder transitiv). Der Präprozessor hält den Guard-Namen des ersten Headers für gesetzt und überspringt beim zweiten `#include` fälschlich den **gesamten Inhalt des anderen Headers** – dessen Klassen/Funktionen sind dann schlicht unbekannt. Das äußert sich meist in kryptischen "unbekannter Bezeichner"-Fehlern an Stellen, die scheinbar nichts mit Includes zu tun haben. Schwer zu diagnostizieren, weil der fehlerhafte Header selbst syntaktisch fehlerfrei ist – man muss erst erkennen, dass er *gar nicht erst eingebunden* wurde.

**c) Include-Reihenfolge (eigene Header zuletzt):** Wenn eigene Header **vor** den Standard-/Drittbibliotheks-Headern eingebunden werden, könnten eigene Header versehentlich von Fehlern in ihrer eigenen Vorwärtsdeklaration/Definition "profitieren" (bzw. Fehler verschleiern), weil noch nicht klar ist, ob ein Symbol aus einem Standardheader stammt oder zufällig schon vorher deklariert wurde. Am Beispiel: `vector.hpp` deklariert fälschlich `namespace std { class vector; }`. Bindet man `vector.hpp` **vor** `<vector>` ein, kollidiert die eigene (falsche) Deklaration mit der echten STL-Deklaration aus `<vector>` → Compilerfehler (widersprüchliche Deklaration von `std::vector`). Bindet man Standardheader zuerst ein, würde ein solcher Fehler viel eher (und klarer) auffallen, weil die eigene fehlerhafte Datei gegen eine bereits bekannte, korrekte Definition geprüft wird.

**d) Eigener Header immer zuerst in der zugehörigen `.cpp`:** Damit wird sichergestellt, dass der Header **für sich allein** vollständig kompilierbar ist (alle von ihm benötigten Typen sind bereits in ihm selbst per Include vorhanden) und nicht heimlich von Includes profitiert, die zufällig vorher in der `.cpp` standen. Im Beispiel: `output.hpp` verwendet `std::string`, includet aber selbst kein `<string>`. In `output.cpp` funktioniert das nur, weil dort zuvor `#include <string>` steht. Ein späterer Entwickler, der `main.cpp` schreibt und nur `#include "output.hpp"` einbindet (ohne vorher `<string>`), bekommt einen Compilerfehler – der Header war nie wirklich eigenständig funktionsfähig. Würde man in `output.cpp` den eigenen Header zuerst einbinden, wäre dieser Fehler sofort beim Kompilieren von `output.cpp` selbst aufgefallen.

**e) Warum der Compiler doppelte textuelle Einbindung nicht automatisch verbietet:** Weil mehrfaches Einbinden **derselben Datei mit unterschiedlichem Kontext** ein legitimes, absichtliches Sprachmittel ist (z. B. X-Macro-Technik). Beispiel:

```cpp
// colors.def  (kein vollständiger Header, keine Guards!)
COLOR(Red)
COLOR(Green)
COLOR(Blue)
```
```cpp
enum class Color {
#define COLOR(name) name,
#include "colors.def"
#undef COLOR
};

const char* to_string(Color c) {
    switch (c) {
#define COLOR(name) case Color::name: return #name;
#include "colors.def"
#undef COLOR
    }
    return "";
}
```
`colors.def` wird hier bewusst zweimal eingebunden, jedes Mal mit anderer `COLOR`-Makrodefinition – ein generisches Verbot mehrfacher Einbindung würde dieses Muster zerstören.

---

## Aufgabe 4 – Präprozessor

### a) Korrektur deiner Lösung

Deine Version ändert die Signatur von `main` und nutzt `printf` – das ist nicht das, was verlangt war (nur an der markierten Stelle, also nur in der `#define`-Zeile, ergänzen). Die Originalvorlage:

```cpp
#include <iostream>
#define PRINT_PREPROCESSED /* ??? */
int main( PRINT_PREPROCESSED }
```

Der Trick: Der Präprozessor ersetzt rein **textuell**, auch über Klammer-/Blockgrenzen hinweg. Löst man `PRINT_PREPROCESSED` zu `) { std::cout << "Preprocessed";` auf:

```cpp
#define PRINT_PREPROCESSED ) { std::cout << "Preprocessed";
```

ergibt sich nach der Ersetzung:

```cpp
int main( ) { std::cout << "Preprocessed"; }
```

— ein vollständiges, korrektes Programm, obwohl im Quelltext selbst weder `)`, `{` noch der eigentliche Ausgabebefehl sichtbar waren.

### b) MULT-Makro – Korrektur/Ergänzung

Deine Notiz hat nur **5 statt 6** Werte (Zeile 7 fehlt) und die Reihenfolge stimmt dadurch nicht mehr mit dem Code überein. `#define MULT(a, b) a * b` ersetzt rein textuell, **ohne Klammern um die Parameter** – das ist die Kernfalle:

| Zeile | Aufruf | Expansion | Ergebnis |
|---|---|---|---|
| 5 | `MULT(2, 3)` | `2 * 3` | `6` |
| 6 | `MULT(2.f, 3.f)` | `2.f * 3.f` | `6` |
| 7 | `MULT(1 + 4, 5 + 3)` | `1 + 4 * 5 + 3` | `24` (Punkt-vor-Strich: `1+20+3`) |
| 8 | `MULT((1 + 4), (5 + 3))` | `(1 + 4) * (5 + 3)` | `40` |
| 9 | `MULT("1" << 4, 5 << "2")` | `"1" << 4 * 5 << "2"` | **Compilerfehler**: `*` bindet stärker als `<<`, `"1" << 20` ist für `const char*` nicht definiert |
| 10 | `MULT(MULT(2, 3), 4)` | inneres Makro wird zuerst expandiert → `2 * 3 * 4` | `24` |

Vollständige, korrigierte Ausgabe: `6, 6, 24, 40, Error, 24`. Dein Fehlerfall (Zeile 9) war richtig erkannt – nur der Eintrag für Zeile 7 fehlte in deiner Liste.

### c) Kritik der Makroprogrammierung (nicht beantwortet)

Makros arbeiten **rein textuell vor der eigentlichen Kompilierung**, ohne jede Kenntnis von C++-Syntax, Typen oder Gültigkeitsbereichen:

- **Keine Typprüfung:** Ein Makro-Parameter kann alles sein; Fehler zeigen sich erst nach der Expansion, mit für den Entwickler kryptischen Fehlermeldungen (die auf den expandierten, nicht den geschriebenen Code verweisen).
- **Operatorpräzedenz-Fallen:** Wie in 4b gezeigt, führt fehlende Klammerung leicht zu falschen Berechnungen.
- **Mehrfachauswertung von Argumenten:** Ein Ausdruck mit Nebeneffekten (`MULT(i++, 2)`) wird mehrfach ausgewertet – Bugs, die schwer zu finden sind.
- **Keine Geltungsbereiche/Namensräume:** Makros sind global und können überall kollidieren; `#undef` ist die einzige "Löschung".
- **Schlecht debugbar:** Debugger springen historisch nicht in Makros hinein, man sieht nur den expandierten (oft unlesbaren) Code.
- ⇒ In modernem C++ ersetzen **Templates**, `constexpr`-Funktionen und `inline`-Funktionen die meisten sinnvollen Anwendungsfälle von Makros, da sie typsicher sind und im Debugger normal behandelt werden.

---

## Aufgabe 5 – Mehrere Abhängigkeiten (nicht beantwortet)

### a) Mit eigenen Headern

```cpp
// battery.hpp
#if !defined(INCLUDED__ADS__BATTERY_HPP)
#define INCLUDED__ADS__BATTERY_HPP
class battery {
public:
    void power_on();
};
#endif
```
```cpp
// battery.cpp
#include "battery.hpp"
#include <iostream>
void battery::power_on() { std::cout << "Starting up" << std::endl; }
```
```cpp
// robot.hpp
#if !defined(INCLUDED__ADS__ROBOT_HPP)
#define INCLUDED__ADS__ROBOT_HPP
#include "battery.hpp"
class robot {
public:
    robot();
private:
    battery b_;
};
#endif
```
```cpp
// robot.cpp
#include "robot.hpp"
#include <iostream>
robot::robot() {
    b_.power_on();
    std::cout << "Robot ready" << std::endl;
}
```
```cpp
// car.hpp / car.cpp – analog zu robot
#if !defined(INCLUDED__ADS__CAR_HPP)
#define INCLUDED__ADS__CAR_HPP
#include "battery.hpp"
class car {
public:
    car();
private:
    battery b_;
};
#endif
```
```cpp
#include "car.hpp"
#include <iostream>
car::car() {
    b_.power_on();
    std::cout << "Car ready" << std::endl;
}
```
```cpp
// main.cpp
#include "robot.hpp"
#include "car.hpp"
int main() {
    robot r;
    car c;
}
```

### b) Ohne eigene Header

Ohne Header kann `main.cpp` die Klassen `robot`/`car` nicht per `#include` kennenlernen. Die einzige saubere Möglichkeit: die **vollständige Klassendefinition** direkt in der jeweiligen `.cpp` belassen, und `main.cpp` benötigt dann selbst eine Vorwärtsdeklaration bzw. muss die Klassen direkt kennen – de facto lässt sich das nur lösen, indem man die Klassen **nicht in main.cpp verwendet**, sondern eine freie Funktion pro Klasse exportiert (`void run_robot(); void run_car();`) und diese **manuell in `main.cpp` deklariert** (ohne Header), z. B.:

```cpp
// robot.cpp (komplett – Klasse + Funktion in einer Datei, kein Header)
#include <iostream>
class battery_r { public: void power_on() { std::cout << "Starting up" << std::endl; } };
class robot { public: robot() { b_.power_on(); std::cout << "Robot ready" << std::endl; } private: battery_r b_; };
void run_robot() { robot r; }
```

```cpp
// main.cpp – Deklarationen von Hand, ohne Header
void run_robot(); // manuell dupliziert statt per #include
void run_car();
int main() { run_robot(); run_car(); }
```

Das zeigt gut, **warum** man Header überhaupt braucht: Ohne sie müsste man Deklarationen von Hand synchron halten – fehleranfällig und nicht wartbar. Genau diese Redundanz automatisiert der Header.

---

## Aufgabe 6 – Schöner Code (nicht beantwortet)

### a)

```cpp
// Beispiel 1
bool robot_ready() { return battery_loaded() && os_started(); }

// Beispiel 2
bool is_obstacle_close() { return obstacle_detected() && distance < 3.0; }

// Beispiel 3
string rotate_direction = (obstacle_pos < robot_pos) ? "left" : "right";
```

Vorteil bei Beispiel 3: Der Ternäroperator erlaubt eine **`const`-Initialisierung in einem Schritt** statt einer nachträglichen Zuweisung – dadurch kann `rotate_direction` als `const` deklariert werden, was Bugs durch spätere versehentliche Änderung verhindert und dem Compiler mehr Optimierungsspielraum gibt.

### b)

```cpp
bool initialize() {
    return power_available() && (power_on(), true)
        && terminal_connected() && (show_logon_prompt(), true)
        && check_user_credentials() && (show_welcome_user_message(), true);
}
```

Sauberer (üblicher) ohne Komma-Operator, rein mit `&&`-Kurzschlussauswertung – jede Bedingung wird nur ausgewertet, wenn die vorherige `true` war, exakt wie in der ursprünglichen verschachtelten `if`-Struktur:

```cpp
bool initialize() {
    return power_available()
        && power_on()          // Achtung: power_on() muss dafür bool zurückgeben oder in ,-Ausdruck eingebettet werden
        && terminal_connected()
        && show_logon_prompt()
        && check_user_credentials()
        && show_welcome_user_message();
}
```
Falls `power_on()`, `show_logon_prompt()`, `show_welcome_user_message()` `void` sind, ist die Komma-Operator-Variante oben die korrekte, ohne Hilfsfunktionen/-variablen.

---

## Aufgabe 7 – Stack, Heap, Zeiger (nicht beantwortet)

### a)
- `value`, `value_ptr` → **eingebaut** (float bzw. Zeiger auf eingebaut — Zeiger selbst gelten als eingebauter Typ)
- `s`, `s_ptr` → **zusammengesetzt** (`std::string` ist eine Klasse) bzw. Zeiger darauf (Zeiger selbst wieder eingebaut)
- `r`, `r_ptr` → **zusammengesetzt** (`robot`) bzw. Zeiger (eingebaut)
- `r.speed` → eingebaut (`float`), `r.position` → zusammengesetzt (`point3f`), `r.position.x` → eingebaut (`float`)

### b)
| Ausdruck | Speicherort |
|---|---|
| `ra` | Stack |
| `ra.speed` | Stack |
| `ra.s` | Stack (der Zeiger selbst) |
| `ra.s->scanning_range` | Heap (Ziel des Zeigers) |
| `rb` | Stack (Zeigervariable) |
| `*rb` | Heap |
| `rb->speed` | Heap |
| `rb->s->scanning_range` | Heap |
| `rc` | Stack |
| `*rc` | Stack (zeigt auf `ra`) |
| `rb->partner_ptr` | Heap (Member von `*rb`) |
| `*(rb->partner_ptr)` | Stack (zeigt auf `ra`) |

### c)

```
Speicher auf dem Stack           Speicher auf dem Heap
Variable   allok.  freigeg.      allok.        freigeg.
a          3       12            3             –  (nie!)
b          4       12            8 (jede Iter.) 11 (nur letzte)
w          5       12            –             –
```

**Drei Probleme:**
1. `*a` (heap) wird nie mit `delete` freigegeben → garantiertes Speicherleck.
2. Jede Schleifeniteration überschreibt `b` mit einer neuen Heap-Adresse, ohne die vorherige zu löschen → Speicherleck pro Iteration (außer der letzten).
3. Ist `w.exit()` bereits zu Programmstart `true` (siehe Hinweis), läuft die Schleife **nie** – `b` bleibt uninitialisiert, und `delete b;` in Zeile 11 löscht einen **wilden Zeiger** → undefiniertes Verhalten.

### d)
Problem: `teeth` wird per `new int(32)` auf dem Heap angelegt, aber nie mit `delete` freigegeben – Speicherleck, da `pumpkin` keinen Destruktor hat. Lösung nur in `main()` möglich (ohne die Struktur zu ändern): manuelles Freigeben direkt nach Gebrauch:

```cpp
int main(int argc, char** argv) {
    pumpkin p;
    delete p.teeth;
}
```

---

## Aufgabe 8 – Fehler mit Zeigern (nicht beantwortet)

### a) Vier Fälle

```cpp
// Fall 1: Adresse 0
int main() {
    int* p = nullptr;
    *p = 1337;
    std::cout << "geschrieben" << std::endl;
}
```
```cpp
// Fall 2: feste Adresse
int main() {
    int* p = reinterpret_cast<int*>(19522430);
    *p = 1337;
    std::cout << "geschrieben" << std::endl;
}
```
```cpp
// Fall 3: deallokierte Stack-Variable
int* get_ptr() { int local = 0; return &local; }
int main() {
    int* p = get_ptr();
    *p = 1337;
    std::cout << "geschrieben" << std::endl;
}
```
```cpp
// Fall 4: deallokierte Heap-Variable
int main() {
    int* p = new int(0);
    delete p;
    *p = 1337;
    std::cout << "geschrieben" << std::endl;
}
```

**Debug-Build:** Fall 1 und 2 stürzen zuverlässig **direkt in der Schreibzeile** ab (Hardware-Schutzverletzung, Access Violation/Segfault – nicht mit Adresse 0/19522430 gemappte Seite). Fall 3 und 4 stürzen im Debug-Build oft **nicht** sofort ab – der Speicher ist physisch noch vorhanden, nur logisch ungültig; manche Debug-CRTs (z. B. MSVC Debug-Heap) füllen freigegebenen Speicher mit Erkennungsmustern, wodurch spätere Prüfungen (z. B. bei der nächsten Allokation) einen Fehler melden können, aber nicht unbedingt in derselben Zeile.

**Release-Build:** Fall 1 und 2 verhalten sich identisch zu Debug (hardwarebasierter Schutz ist build-unabhängig). Fall 3 und 4 laufen im Release meist **ohne jede Fehlermeldung** durch, da die Debug-Sicherheitsprüfungen (Guard-Bytes, Pattern-Fill) entfernt sind – das Programm "funktioniert scheinbar", die Korruption zeigt sich erst später, an ganz anderer Stelle.

### b) Vier Codebeispiele

**Beispiel 1** — Compilezeitfehler in Zeile 5: `p0 = &p1;` — `p0` ist `int*`, `&p1` aber `int**` (Typ passt nicht).

**Beispiel 2** — Kein Fehler. Ausgabe: `Ergebnis: 5` (über `pp` wird `p` auf `&i` umgebogen, `*p` liest dann `i`).

**Beispiel 3** — Laufzeitfehler in **Zeile 7** (`std::cout << *p;`): `delete p` setzt `p` **nicht** automatisch auf `nullptr` (daher ist die Bedingung in Zeile 4 `false`, "True in Z4" wird nicht ausgegeben). Erst danach wird `p` in Zeile 5 manuell auf `nullptr` gesetzt; Zeile 7 dereferenziert diesen Null-Zeiger → undefiniertes Verhalten/Absturz.

**Beispiel 4** — Laufzeitfehler in **Zeile 3**: `delete &f;` löscht die **Adresse der lokalen Zeigervariablen `f` selbst** (Stack-Adresse), nicht das mit `new` angelegte Heap-Ziel. Da diese Adresse nie mit `new` erzeugt wurde, ist das undefiniertes Verhalten (typischerweise Absturz); zusätzlich bleibt der eigentliche Heap-Speicher als Leck zurück.

### c) Strict Pointer Aliasing

Strict Aliasing besagt, dass der Compiler annehmen darf, dass Zeiger unterschiedlichen, nicht verwandten Typs (hier `float*` und `int*`) **niemals** dieselbe Speicherstelle referenzieren. Auf Basis dieser Annahme darf der Optimierer Lesezugriffe über `ptr_i` zwischenspeichern/cachen und muss nicht neu einlesen, nur weil zwischenzeitlich über `ptr_f` geschrieben wurde. Im Beispiel wird `f` über `ptr_f` verändert, aber der zweite Zugriff über `ptr_i` liest möglicherweise trotzdem denselben (veralteten) Wert wie beim ersten Mal – weil der Compiler laut Sprachstandard davon ausgehen durfte, dass sich über `ptr_i` nichts geändert haben kann. Das Ergebnis ist **undefiniertes Verhalten**: je nach Optimierungsstufe kann der zweite Ausgabewert korrekt oder veraltet sein, was den beobachteten Effekt erklärt.