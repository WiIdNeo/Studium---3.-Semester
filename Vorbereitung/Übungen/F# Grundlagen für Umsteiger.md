# F# Basics – Referenz für Umsteiger

## Variablen (Bindings)

F# nennt das nicht "Variable", sondern **Binding** – standardmäßig **immutable** (unveränderlich), anders als in C#.

```fsharp
let x = 5              // Typ wird inferiert als int
let name = "Max"        // string
let pi = 3.14           // float

// Explizite Typannotation (optional, aber erlaubt):
let y: int = 10
let z: float = 2.5

// x <- 6               // FEHLER: x ist immutable, das geht nicht

// Für veränderliche Werte brauchst du "mutable":
let mutable counter = 0
counter <- 1            // Zuweisung mit <-, nicht mit =
counter <- counter + 1
```

Wichtig: `=` ist in F# **kein** Zuweisungsoperator wie in C#, sondern Teil der Bindung selbst. Änderung eines mutable-Werts geschieht mit `<-`.

---

## Funktionen

```fsharp
// Grundform: let name parameter1 parameter2 = ausdruck
let add x y = x + y

// Aufruf: keine Klammern/Kommas nötig
let result = add 3 4    // 7

// Mit expliziten Typen:
let addTyped (x: int) (y: int) : int = x + y

// Mehrzeilige Funktion (Einrückung ist bedeutungstragend, wie bei Python)
let describe age =
    if age < 18 then
        "minderjährig"
    else
        "erwachsen"

// Funktion ohne Parameter braucht "()" (unit) als Platzhalter
let sayHello () =
    printfn "Hallo!"

sayHello ()
```

Der letzte Ausdruck im Funktionskörper ist automatisch der Rückgabewert – kein `return` nötig (es gibt zwar `return`, aber nur in speziellen Kontexten wie computation expressions).

---

## Klassen

F# ist funktional-first, aber Klassen (OOP) sind vollständig unterstützt:

```fsharp
type Person(name: string, age: int) =
    // Felder
    member this.Name = name
    member this.Age = age

    // Methode
    member this.Greet() =
        printfn "Hallo, ich bin %s und %d Jahre alt" this.Name this.Age

    // Methode mit mutable internem Zustand
    member val Score = 0 with get, set
```

Der Konstruktor steht direkt hinter dem Typnamen (`Person(name: string, age: int)`) – es gibt keinen separaten Konstruktor-Block wie in C#.

### Instanz erstellen

```fsharp
let p = Person("Anna", 30)
p.Greet()                  // "Hallo, ich bin Anna und 30 Jahre alt"
p.Score <- 42               // setzt den veränderlichen Wert
printfn "%d" p.Score
```

### Alternative: Records (oft die bessere Wahl statt Klassen)

Für reine Datencontainer sind **Records** idiomatischer als Klassen – immutable, mit automatischem Vergleich und Kopierfunktion:

```fsharp
type PersonRecord = { Name: string; Age: int }

let p2 = { Name = "Tom"; Age = 25 }
printfn "%s ist %d" p2.Name p2.Age

// "Ändern" erzeugt eine Kopie mit neuem Wert (Original bleibt unverändert):
let older = { p2 with Age = 26 }
```

---

## Switch-Case → Pattern Matching (`match`)

F# hat kein `switch`, sondern **`match`** – deutlich mächtiger, da es nicht nur Werte, sondern auch Strukturen/Typen matchen kann:

```fsharp
let describeNumber n =
    match n with
    | 0 -> "null"
    | 1 -> "eins"
    | x when x < 0 -> "negativ"     // Bedingung mit "when"
    | _ -> "irgendeine andere Zahl"  // "_" = default/else

printfn "%s" (describeNumber 0)
printfn "%s" (describeNumber -5)
```

Wie in deinem Python-Taschenrechner-Beispiel, nur ohne `break` (kein Fallthrough in F#):

```fsharp
let calculate op a b =
    match op with
    | "+" -> a + b
    | "-" -> a - b
    | "*" -> a * b
    | "/" -> a / b
    | _ -> failwith "Unbekannter Operator"
```

`match` funktioniert auch mit Typen (z.B. Discriminated Unions) und Tupeln – das ist eines der stärksten Features von F#, aber für den Einstieg reicht die Grundform oben.

---

## Ausgaben

```fsharp
printfn "Hallo Welt"                    // einfacher String, Zeilenumbruch am Ende
printfn "Name: %s, Alter: %d" name age  // formatiert, wie printf in C
printfn "Pi ist ungefähr %f" 3.14159
printf "Ohne Zeilenumbruch"             // ohne "n" -> kein \n am Ende
```

Wichtige Format-Platzhalter:
- `%s` → string
- `%d` → int
- `%f` → float
- `%b` → bool
- `%A` → beliebiger Typ (druckt automatisch eine sinnvolle Darstellung, super für Debugging von Records/Listen)

```fsharp
printfn "%A" [1; 2; 3]     // [1; 2; 3]
```

---

## Eingaben

```fsharp
printf "Gib deinen Namen ein: "
let name = System.Console.ReadLine()
printfn "Hallo, %s!" name

// Eingabe in Zahl umwandeln:
printf "Gib eine Zahl ein: "
let input = System.Console.ReadLine()

match System.Int32.TryParse(input) with
| true, value -> printfn "Du hast %d eingegeben" value
| false, _ -> printfn "Das war keine gültige Zahl"
```

`TryParse` gibt ein Tupel `(bool, wert)` zurück – kein Exception-Handling nötig, das ist der idiomatische F#-Weg, Konvertierungsfehler abzufangen (ähnlich deinem `try/except`-Ansatz in Python, nur ohne Exception).

---

## Mini-Beispiel: Dein Taschenrechner in F#

```fsharp
let rec loop () =
    printf "Erste Zahl (oder 'q' zum Beenden): "
    let input1 = System.Console.ReadLine()

    if input1 = "q" then
        ()
    else
        match System.Double.TryParse(input1) with
        | false, _ ->
            printfn "Ungültige Eingabe, nochmal von vorn"
            loop ()
        | true, num1 ->
            printf "Operator (+, -, *, /): "
            let op = System.Console.ReadLine()

            printf "Zweite Zahl: "
            let input2 = System.Console.ReadLine()

            match System.Double.TryParse(input2) with
            | false, _ ->
                printfn "Ungültige Eingabe, nochmal von vorn"
                loop ()
            | true, num2 ->
                let result =
                    match op with
                    | "+" -> Some (num1 + num2)
                    | "-" -> Some (num1 - num2)
                    | "*" -> Some (num1 * num2)
                    | "/" when num2 <> 0.0 -> Some (num1 / num2)
                    | "/" -> printfn "Division durch Null!"; None
                    | _ -> printfn "Unbekannter Operator"; None

                match result with
                | Some r -> printfn "%f %s %f = %f" num1 op num2 r
                | None -> ()

                loop ()

loop ()
```

Beachte `let rec` – für rekursive Funktionen (wie hier die Schleife) brauchst du das Schlüsselwort `rec`, sonst kennt die Funktion sich selbst nicht.