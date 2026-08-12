# F# Zero to Hero – Übungsreihe

Jede Aufgabe nennt nur das **Ziel**. Lösung selbst erarbeiten, bei Bedarf in der letzten Referenz-Datei nachschlagen oder fragen. Am Ende jeder Stufe: Idee, die gleiche Aufgabe auch in C und/oder C# zu schreiben, um die Sprachen im Vergleich zu festigen.

---

## Stufe 1 – Grundlagen: Variablen, Ausgabe, einfache Funktionen

**1.1 Hallo Welt**
Schreib ein Programm, das "Hallo Welt" ausgibt.

**1.2 Begrüßung mit Eingabe**
Frag den Namen des Nutzers per Konsoleneingabe ab und gib "Hallo, `<Name>`!" aus.

**1.3 Rechteck-Fläche**
Deklariere zwei `let`-Bindings für Breite und Höhe (feste Werte), berechne die Fläche und gib sie formatiert aus.

**1.4 Mutable Zähler**
Erstelle einen `mutable`-Zähler, erhöhe ihn drei Mal um 1 und gib den Endwert aus. Ziel: den Unterschied zwischen `let` (immutable) und `let mutable` in der Praxis spüren.

**1.5 Einfache Funktion**
Schreib eine Funktion `quadrat`, die eine Zahl quadriert. Teste sie mit mehreren Eingaben.

**1.6 Funktion mit mehreren Parametern**
Schreib eine Funktion `istGroesser`, die zwei Zahlen nimmt und `true`/`false` zurückgibt, je nachdem ob die erste größer ist als die zweite.

---

## Stufe 2 – Kontrollfluss: if/else, Pattern Matching, Schleifen

**2.1 Gerade oder ungerade**
Funktion, die für eine Zahl ausgibt, ob sie gerade oder ungerade ist – einmal mit `if/else`, einmal mit `match`.

**2.2 Notenrechner (match statt switch)**
Schreib eine Funktion, die eine Punktzahl (0–100) entgegennimmt und per `match` mit `when`-Guards eine Note ("Sehr gut", "Gut", "Befriedigend", "Nicht bestanden") zurückgibt.

**2.3 FizzBuzz**
Der Klassiker: Zahlen 1 bis 30 ausgeben, bei Vielfachen von 3 "Fizz", von 5 "Buzz", von beiden "FizzBuzz". Nutze `for`-Schleife und `match` oder `if`.

**2.4 Zähler-Schleife mit while**
Zähle mit einer `while`-Schleife und einem `mutable`-Zähler von 1 bis 10 hoch.

**2.5 Rekursive Fakultät**
Schreib eine Funktion `fakultaet` **rekursiv** (mit `let rec`), keine Schleife. Ziel: Rekursion als F#-typischer Ersatz für Schleifen.

**2.6 Fibonacci rekursiv**
Gleiches Prinzip wie 2.5, aber für die Fibonacci-Folge. Bonus: mach die Funktion tail-rekursiv (mit einem Akkumulator-Parameter) und informier dich, warum das in F# wichtig ist (Stack-Overflow-Vermeidung).

---

## Stufe 3 – Datenstrukturen: Listen, Arrays, Tupel

**3.1 Liste erstellen und durchlaufen**
Erstelle eine Liste von 5 Zahlen, gib jede einzeln mit `for x in liste` aus.

**3.2 Summe einer Liste – rekursiv**
Schreib eine eigene Funktion `summe`, die eine `int list` rekursiv aufsummiert (ohne `List.sum` zu benutzen). Nutze Pattern Matching auf die Liste (`[]` und `head :: tail`).

**3.3 Summe einer Liste – mit Bibliotheksfunktion**
Löse 3.2 nochmal, diesmal mit `List.sum`. Vergleiche die Kürze.

**3.4 Array vs. Liste**
Erstelle dieselben 5 Zahlen einmal als `array` statt `list`. Informier dich: Was ist der praktische Unterschied (Mutability, Performance)?

**3.5 Tupel**
Schreib eine Funktion, die zwei Zahlen nimmt und ein Tupel `(summe, differenz)` zurückgibt. Rufe sie auf und "entpacke" das Tupel in zwei einzelne Bindings.

**3.6 Größte Zahl finden – rekursiv**
Schreib eine rekursive Funktion, die aus einer `int list` die größte Zahl findet (kein `List.max`).

---

## Stufe 4 – Eigene Typen: Records und Discriminated Unions

**4.1 Record definieren**
Definiere einen Record `Buch` mit `Titel: string`, `Autor: string`, `Jahr: int`. Erstelle zwei Instanzen und gib sie formatiert aus.

**4.2 Record kopieren mit Änderung**
Nimm ein `Buch`-Record aus 4.1 und erzeuge mit der `{ x with ... }`-Syntax eine Kopie mit geändertem Jahr.

**4.3 Liste von Records**
Erstelle eine Liste von 3 `Buch`-Records. Nutze `List.filter`, um nur Bücher nach einem bestimmten Jahr zu finden.

**4.4 Discriminated Union – Formen**
Definiere eine Union `Form` mit Fällen `Kreis of float` (Radius), `Rechteck of float * float` (Breite, Höhe), `Dreieck of float * float * float` (drei Seiten). Schreib eine Funktion `flaeche`, die per `match` die Fläche berechnet (Rechteck ist trivial, für Dreieck nutze die Heron-Formel).

**4.5 Option-Typ**
Schreib eine Funktion `sicheresDividieren : float -> float -> float option`, die bei Division durch Null `None` zurückgibt statt eines Fehlers. Werte das Ergebnis mit `match` aus (`Some x` / `None`).

---

## Stufe 5 – Objektorientierung: Klassen, Vererbung, Interfaces

**5.1 Einfache Klasse**
Definiere eine Klasse `Konto` mit einem Feld `Kontostand` (mutable), einer Methode `Einzahlen(betrag)` und `Abheben(betrag)`. Erstelle eine Instanz, führe ein paar Transaktionen aus, gib den Endstand aus.

**5.2 Vererbung**
Definiere eine Basisklasse `Tier` mit einer virtuellen Methode `MachGeraeusch()`. Leite `Hund` und `Katze` davon ab, überschreibe die Methode jeweils.

**5.3 Interface**
Definiere ein Interface `IBeschreibbar` mit einer Methode `Beschreibung() : string`. Implementiere es in zwei unterschiedlichen Klassen.

**5.4 Klasse mit Konstruktor-Validierung**
Erstelle eine Klasse `Alter`, die im Konstruktor prüft, ob der übergebene Wert ≥ 0 ist, sonst eine Exception wirft (`failwith` oder `invalidArg`).

**Vergleichsaufgabe:** Schreib 5.1 (Konto-Klasse) zusätzlich in C# – vergleiche Syntax für Felder, Konstruktor, Methoden.

---

## Stufe 6 – Funktionale Idiome: Higher-Order-Functions, Pipes, Currying

**6.1 map/filter/fold auf Listen**
Nimm eine Liste von Zahlen 1–20. Nutze `List.filter`, um nur gerade Zahlen zu behalten, dann `List.map`, um jede zu verdoppeln, dann `List.fold`, um sie aufzusummieren.

**6.2 Pipe-Operator**
Löse 6.1 nochmal, aber verkette alles mit dem `|>`-Operator statt verschachtelter Funktionsaufrufe.

**6.3 Eigene Higher-Order-Function**
Schreib eine Funktion `wendeZweimalAn`, die eine Funktion `f` und einen Wert `x` nimmt und `f (f x)` zurückgibt. Teste mit `quadrat` aus 1.5.

**6.4 Currying und partielle Anwendung**
Schreib eine Funktion `multipliziere x y = x * y`. Erzeuge daraus durch partielle Anwendung eine neue Funktion `verdoppeln` (die nur noch einen Parameter braucht). Informier dich, warum das in F# "automatisch" funktioniert (jede Funktion ist curried).

**6.5 Lambda-Ausdrücke**
Löse 6.1 nochmal, aber ersetze `List.filter` und `List.map` durch anonyme Lambda-Funktionen (`fun x -> ...`) direkt inline.

---

## Stufe 7 – Fehlerbehandlung

**7.1 Exceptions**
Schreib eine Funktion, die bei negativer Eingabe eine Exception wirft (`failwith`), und fange sie mit `try/with` im aufrufenden Code ab.

**7.2 Result-Typ**
Schreib eine Funktion `parseAlter : string -> Result<int, string>`, die einen String parst und entweder `Ok wert` oder `Error "Fehlermeldung"` zurückgibt. Werte per `match` aus.

**7.3 Eigene Exception-Typen**
Definiere eine eigene Exception `UngueltigesAlterException of string` und wirf/fange sie gezielt.

---

## Stufe 8 – Module, Generics, Strings

**8.1 Modul**
Packe mehrere deiner Funktionen aus Stufe 1–2 in ein `module Mathe = ...` und rufe sie qualifiziert auf (`Mathe.quadrat 5`).

**8.2 Generische Funktion**
Schreib eine generische Funktion `tausche`, die ein Tupel `(a, b)` beliebigen Typs nimmt und `(b, a)` zurückgibt. Teste mit `int`-Tupel und `string`-Tupel.

**8.3 String-Verarbeitung**
Schreib eine Funktion, die einen Satz (String) nimmt, ihn in Wörter zerlegt (`String.split`), die Anzahl der Wörter zählt und das längste Wort ausgibt.

**8.4 Generischer Container-Typ**
Definiere einen generischen Record `Box<'a> = { Inhalt: 'a }`. Erstelle eine `Box<int>` und eine `Box<string>`.

---

## Stufe 9 – Abschlussprojekt (alles zusammen)

**9.1 Einfache "Bibliotheksverwaltung"**
Kombiniere möglichst viel aus den Stufen oben:
- Record `Buch` (Titel, Autor, Jahr, Verfügbar: bool)
- Liste von Büchern als "Datenbank" (mutable Liste oder Referenzzelle)
- Funktionen zum Ausleihen/Zurückgeben (ändert `Verfügbar`, gibt neue Liste per `List.map` zurück, da Records immutable sind)
- Konsolenmenü mit `match` auf Nutzereingabe (1 = Anzeigen, 2 = Ausleihen, 3 = Beenden), rekursive Schleife wie im Taschenrechner-Beispiel
- Fehlerbehandlung mit `Result` oder `Option`, falls ein Buchtitel nicht gefunden wird

Das ist bewusst offen gehalten – bau es so aus, wie es dir sinnvoll erscheint. Wenn du das komplett durch hast, hast du praktisch jedes Grundkonstrukt angefasst, das du für ein Uni-F#-Modul brauchst.

---

## Hinweis zum Sprachvergleich

Bei den Stufen 1, 2, 5 bietet es sich am meisten an, parallel in **C** (Stufe 1–2: Variablen, Schleifen, Rekursion – kein OOP) und **C#** (Stufe 5: Klassen, Vererbung, Interfaces) mitzuschreiben, da sich dort die Konzepte am direktesten gegenüberstehen. Bei Stufe 4 und 6 (Records, Discriminated Unions, map/filter/fold, Pattern Matching) wirst du merken, dass C und C# keine direkten Äquivalente haben – das sind die Stellen, an denen F# am meisten von den anderen beiden abweicht und am meisten Neues bietet.