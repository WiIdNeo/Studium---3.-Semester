# CRC (Cyclic Redundancy Check) verstehen und üben

## Teil 1: Die Grundidee

Beim Übertragen können Bits kippen. Der Sender hängt deshalb an die Nachricht eine kurze **Prüfsumme** an (den CRC). Der Empfänger rechnet nach und erkennt so Übertragungsfehler.

Das Verfahren in einem Satz: **Sender und Empfänger einigen sich auf ein Generatorpolynom G. Der Sender macht die Nachricht so, dass sie "restlos durch G teilbar" ist. Bleibt beim Empfänger ein Rest, ist etwas schiefgegangen.**

Geteilt wird dabei nicht "normal", sondern **modulo 2**. Das heißt:

- Es gibt keinen Übertrag.
- Subtrahieren und Addieren sind dasselbe und entsprechen **XOR**.

| a | b | a XOR b |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

(Gleiche Bits ergeben 0, verschiedene ergeben 1.)

### Das Generatorpolynom als Bitfolge

Jeder Koeffizient des Polynoms wird zu einem Bit. Fehlende Potenzen sind 0.

```text
G(x) = x³ + x + 1
        x³  x²  x¹  x⁰
        1   0   1   1    →  1011
```

Wichtig: Ein Polynom vom **Grad n** ergibt **n + 1 Bits**, der CRC hat **n Bits**, und du hängst **n Nullen** an.

| Polynom | Bitfolge | Grad | Nullen anhängen | CRC-Länge |
|---|---|---|---|---|
| x³ + x + 1 | 1011 | 3 | 3 | 3 Bit |
| x³ + x² + 1 | 1101 | 3 | 3 | 3 Bit |
| x⁴ + x + 1 | 10011 | 4 | 4 | 4 Bit |
| x⁵ + x² + 1 | 100101 | 5 | 5 | 5 Bit |

> Genau hier haben in der Klausur mehrere Leute Punkte verloren (4 statt 3 Nullen oder gar keine). Rechne immer: **Anzahl Nullen = Bits von G − 1.**

---

## Teil 2: Das Rezept (Sender)

1. **G als Bitfolge** aufschreiben (n + 1 Bits, Grad n).
2. An die Nachricht **n Nullen anhängen**.
3. **Modulo-2-Division** durchführen (siehe unten). Der **Rest** hat n Bits.
4. **Übertragen wird: Originalnachricht + Rest.** (Nicht die Nachricht mit den Nullen!)

### Die Division mit der "Fenster-Methode"

Du arbeitest immer mit einem Fenster von **n + 1 Bits** (so lang wie G):

1. Nimm die ersten n + 1 Bits als Fenster.
2. Ist das **vorderste Bit 1** → Fenster **XOR G**. Ist es **0** → nichts tun (XOR mit 0000).
3. Das vorderste Bit fällt weg (es ist immer 0). Übrig bleibt ein **Rest mit n Bits**.
4. **Hole das nächste Bit** der Nachricht rechts an den Rest. Das ist dein neues Fenster.
5. Wiederhole ab Schritt 2, bis alle Bits verbraucht sind.

Der Rest nach dem letzten Bit ist der **CRC**.

**Typischer Fehler:** Beim Herunterholen ein Bit vergessen oder doppelt nehmen. Hake in der Nachricht jedes Bit ab, das du verbraucht hast.

---

## Teil 3: Ausführliches Beispiel

**Aufgabe:** Die Nachricht `1101011` soll mit dem Generatorpolynom `x³ + x + 1` gesendet werden.

### Schritt 1: G als Bits

x³ + x + 1 → **1011** (Grad 3 → 3 Nullen, CRC hat 3 Bit).

### Schritt 2: Nullen anhängen

```text
Nachricht:      1101011
+ 3 Nullen:     1101011 000   →   1101011000   (10 Bit)
```

### Schritt 3: Division

Die Bits der erweiterten Nachricht sind durchnummeriert: `1 1 0 1 0 1 1 0 0 0` (Bit 1 bis 10).

| Schritt | Fenster (Rest + neues Bit) | vorderstes Bit | Rechnung | Neuer Rest |
|---|---|---|---|---|
| 1 | `1101` (Bit 1–4) | 1 | 1101 XOR 1011 = 0110 | **110** |
| 2 | `110` + Bit 5 (0) = `1100` | 1 | 1100 XOR 1011 = 0111 | **111** |
| 3 | `111` + Bit 6 (1) = `1111` | 1 | 1111 XOR 1011 = 0100 | **100** |
| 4 | `100` + Bit 7 (1) = `1001` | 1 | 1001 XOR 1011 = 0010 | **010** |
| 5 | `010` + Bit 8 (0) = `0100` | 0 | nichts (nur schieben) | **100** |
| 6 | `100` + Bit 9 (0) = `1000` | 1 | 1000 XOR 1011 = 0011 | **011** |
| 7 | `011` + Bit 10 (0) = `0110` | 0 | nichts (nur schieben) | **110** |

Alle 10 Bits sind verbraucht. **Der Rest ist `110`**, das ist der CRC.

### Schritt 4: Übertragene Nachricht

```text
Originalnachricht:  1101011
CRC:                       110
Gesendet:           1101011110
```

### Probe beim Empfänger

Der Empfänger teilt die **empfangene Nachricht** (ohne Nullen) durch dasselbe G:

| Schritt | Fenster | vorderstes Bit | Rechnung | Neuer Rest |
|---|---|---|---|---|
| 1 | `1101` | 1 | 1101 XOR 1011 = 0110 | 110 |
| 2 | `1100` | 1 | 1100 XOR 1011 = 0111 | 111 |
| 3 | `1111` | 1 | 1111 XOR 1011 = 0100 | 100 |
| 4 | `1001` | 1 | 1001 XOR 1011 = 0010 | 010 |
| 5 | `0101` (Bit 8 ist jetzt 1) | 0 | nichts | 101 |
| 6 | `1011` (Bit 9 ist 1) | 1 | 1011 XOR 1011 = 0000 | 000 |
| 7 | `0000` (Bit 10 ist 0) | 0 | nichts | **000** |

**Rest 000 → kein Fehler erkannt.** Würde unterwegs ein Bit kippen, bliebe (fast immer) ein Rest ≠ 0, und der Empfänger verwirft den Frame.

### Warum funktioniert das?

Beim Senden hast du den Rest R der Nachricht (mit Nullen) berechnet. Anhängen von R bedeutet: Nachricht mit Nullen **XOR R**. Weil XOR hier Addieren und Subtrahieren zugleich ist, wird der Rest dadurch genau "weggerechnet". Das Ergebnis ist ohne Rest durch G teilbar.

---

## Teil 4: Die Klausuraufgabe nachgerechnet

Zur Kontrolle deiner Klausur (Aufgabe 8): Nachricht `101010111101`, G = `1011`.

Mit 3 Nullen: `101010111101000` (15 Bit).

- Start: `1010` XOR `1011` = `0001` → Rest **001**
- Dann je ein neues Bit (Bit 5 bis 15): Reste **011, 110, 110, 110, 110, 110, 111, 100, 011, 110, 111**

Der Rest ist **111**, übertragen wird **101010111101111**.

Vergleiche das mit deiner Rechnung: Du hattest die richtigen Startwerte, aber ab der Stelle mit den vier Einsen hintereinander (Bit 7–10) sind Bits verloren gegangen. Mit der Fenster-Methode und dem Abhaken der Bits passiert das nicht.

---

## Teil 5: Übungsaufgaben

Rechne zuerst selbst, danach vergleiche mit Teil 6.

### Aufgabe 1: Polynom ↔ Bitfolge

a) Wandle in Bitfolgen um: x³ + x² + 1, x⁴ + x + 1, x³ + 1, x⁵ + x² + 1.

1101
10011
1001
100101

b) Welches Polynom gehört zu `1011`? Zu `10011`?
c) Wie viele Nullen hängst du bei `100101` an?

Immer k - 1 also 5

### Aufgabe 2: CRC berechnen

Nachricht `1001101`, G = x³ + x + 1. Berechne den CRC und die übertragene Nachricht.

1001101
1011

1001101000
1011
––––
0010101000
||1011
–––––––
||00011000
|||||1011
––––––––––
|||||01110
||||||1011
––––––––––
||||||0101

### Aufgabe 3: CRC berechnen (anderes G)

Nachricht `11100101`, G = x³ + x² + 1 (`1101`). Berechne den CRC und die übertragene Nachricht.

### Aufgabe 4: CRC berechnen (G mit Lücke)

Nachricht `110010`, G = x³ + 1 (`1001`). Berechne CRC und übertragene Nachricht.

### Aufgabe 5: Empfänger prüfen

a) G = `1011` (x³ + x + 1). Empfangen wurde `1001101101`. Ist die Übertragung fehlerfrei?
b) G = `1101` (x³ + x² + 1). Empfangen wurde `11100101111`. Ist die Übertragung fehlerfrei?

### Aufgabe 6: Längeres Generatorpolynom

Nachricht `100111`, G = x⁴ + x + 1 (`10011`). Berechne CRC und übertragene Nachricht.

### Aufgabe 7: Verständnisfragen

a) Was wird am Ende tatsächlich gesendet: Nachricht + Nullen oder Nachricht + Rest?
b) Der Empfänger berechnet den Rest 000. Heißt das, dass garantiert kein Bit gekippt ist?

---

## Teil 6: Lösungen

### Lösung 1

a) x³ + x² + 1 = **1101** · x⁴ + x + 1 = **10011** · x³ + 1 = **1001** (x² und x fehlen, also 0) · x⁵ + x² + 1 = **100101**
b) `1011` = **x³ + x + 1** · `10011` = **x⁴ + x + 1**
c) `100101` hat 6 Bit → Grad 5 → **5 Nullen**.

### Lösung 2

Mit 3 Nullen: `1001101000`.

Reste nacheinander: Start `1001` XOR `1011` = **010**, dann Bit 5 bis 10: **101, 001, 011, 110, 111, 101**.

**CRC = 101**, übertragen: **1001101101**.

### Lösung 3

Mit 3 Nullen: `11100101000`.

Start: `1110` XOR `1101` = **011**, dann Bit 5 bis 11: **110, 000, 000, 001, 010, 100, 101**.

**CRC = 101**, übertragen: **11100101101**.

### Lösung 4

Mit 3 Nullen: `110010000`.

Start: `1100` XOR `1001` = **101**, dann Bit 5 bis 9: **010, 100, 001, 010, 100**.

**CRC = 100**, übertragen: **110010100**.

### Lösung 5

a) Das ist die Nachricht aus Aufgabe 2. Division: `1001` → 010; dann 101, 001, 011, 111, 101, **000**. Rest 000 → **fehlerfrei** (soweit erkennbar).

b) Division durch `1101`: `1110` XOR `1101` = 011; dann Reste 110, 000, 000, 001, 011, 111, **010**. Rest 010 ≠ 000 → **Fehler erkannt**, der Frame wird verworfen. (Gegenüber Aufgabe 3 sind die letzten beiden Bits gekippt: gesendet 101, empfangen 111.)

### Lösung 6

G hat 5 Bit → Grad 4 → **4 Nullen**: `1001110000`.

Fenster sind jetzt 5 Bit lang. Start: `10011` XOR `10011` = **0000**, dann Bit 6 bis 10: Reste **0001, 0010, 0100, 1000, 0011**.

**CRC = 0011** (immer 4 Stellen, führende Nullen nicht weglassen!), übertragen: **1001110011**.

### Lösung 7

a) **Nachricht + Rest**. Die angehängten Nullen sind nur Rechenhilfe, sie werden nie gesendet.
b) **Nein.** Rest 000 heißt nur: kein Fehler *erkannt*. Wenn mehrere Bits so kippen, dass die Nachricht wieder durch G teilbar ist, fällt es nicht auf. CRC erkennt aber zuverlässig alle Einzelbitfehler und Fehlerbündel, die höchstens so lang sind wie der CRC. CRC *erkennt* nur Fehler, er *korrigiert* nichts.

---

## Merkzettel für die Klausur

1. **Bits von G − 1 = Anzahl Nullen** (Grad des Polynoms).
2. Fenster = Länge von G. Vorderstes Bit 1 → XOR G, sonst nur schieben.
3. Nach jedem Schritt das **nächste Bit** der Nachricht herunterholen und abhaken.
4. Der Rest hat immer so viele Bits wie Nullen angehängt wurden.
5. **Senden = Originalnachricht + Rest.**
6. Empfänger: Rest 000 → okay, sonst Fehler.
