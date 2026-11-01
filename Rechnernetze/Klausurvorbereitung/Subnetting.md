# Subnetting verstehen und üben

## Teil 1: Die Grundidee

### Was ist eine IPv4-Adresse?

Eine IPv4-Adresse besteht aus **32 Bit**, aufgeteilt in 4 Blöcke (Oktette) à 8 Bit:

```text
192      .168      .10       .130
11000000 .10101000 .00001010 .10000010
```

### Was bedeutet /26?

Die Zahl nach dem Schrägstrich (das **Präfix**) sagt, **wie viele Bits von links zum Netzanteil gehören**. Der Rest sind **Hostbits**.

```text
/26  →  26 Bit Netz, 32 - 26 = 6 Bit Host

11111111.11111111.11111111.11000000   ← Subnetzmaske = 255.255.255.192
|-------- 26 Netzbits ----------|hhhhhh|
                                 6 Hostbits
```

Die Subnetzmaske ist also nur eine andere Schreibweise des Präfixes: Links so viele Einsen wie das Präfix, rechts Nullen.

### Die drei Spezialadressen eines Netzes

Mit **h Hostbits** hat ein Subnetz **2^h Adressen**:

| Adresse | Hostbits | Bedeutung |
|---|---|---|
| **Netzadresse** | alle 0 | erste Adresse, bezeichnet das Netz selbst |
| **Broadcast-Adresse** | alle 1 | letzte Adresse, geht an alle im Netz |
| Hosts dazwischen | beliebig | **2^h − 2** nutzbare Adressen |

Deshalb rechnest du bei Hostanzahlen immer **+2**.

### Die Tabelle zum Auswendiglernen (letztes Oktett)

| Präfix | Maske | Hostbits | Adressen pro Netz (Blockgröße) | nutzbare Hosts |
|---|---|---|---|---|
| /24 | 255.255.255.0 | 8 | 256 | 254 |
| /25 | 255.255.255.128 | 7 | 128 | 126 |
| /26 | 255.255.255.192 | 6 | 64 | 62 |
| /27 | 255.255.255.224 | 5 | 32 | 30 |
| /28 | 255.255.255.240 | 4 | 16 | 14 |
| /29 | 255.255.255.248 | 3 | 8 | 6 |
| /30 | 255.255.255.252 | 2 | 4 | 2 |

Die Blockgröße ist 2^(32 − Präfix). Die Zweierpotenzen kennst du: 2, 4, 8, 16, 32, 64, 128, 256.

---

## Teil 2: Die zwei Aufgabentypen

### Typ A: In gleich große Netze teilen

**Rezept:**

1. Anzahl der Netze auf die nächste Zweierpotenz aufrunden: 2^k.
2. Präfix = altes Präfix + k.
3. Blockgröße = 2^(32 − neues Präfix).
4. Die Netze beginnen bei 0 und steigen jeweils um die Blockgröße.
5. Broadcast = Beginn des nächsten Netzes − 1.

### Typ B: Netze mit unterschiedlichen Hostzahlen (VLSM)

**Rezept:**

1. Anforderungen **nach Größe sortieren, größtes zuerst**.
2. Pro Netz: Hosts **+ 2** rechnen, auf die nächste Zweierpotenz aufrunden. Daraus ergibt sich Blockgröße und Präfix.
3. Netze **lückenlos hintereinander** ab der Startadresse vergeben.
4. Pro Netz: Netzadresse, Broadcast (= nächster Start − 1), Host-Bereich (Netz + 1 bis Broadcast − 1).

Warum größtes zuerst? Blöcke müssen auf Vielfachen ihrer eigenen Größe beginnen. Ein 128er-Block kann nur bei 0 oder 128 starten. Fängst du mit kleinen Netzen an, landet der große Block ungünstig, oder es bleibt keine passende Stelle mehr.

---

## Teil 3: Ausführliches Beispiel (Typ B)

**Aufgabe:** Das Netz `192.168.10.0/24` soll in vier Netze aufgeteilt werden:

| Netz | benötigte Hosts |
|---|---|
| A | 100 |
| B | 50 |
| C | 25 |
| D | 10 |

Die Reihenfolge ist schon nach Größe sortiert (100 → 50 → 25 → 10).

### Schritt 1: Blockgröße und Präfix je Netz

| Netz | Hosts + 2 | nächste Zweierpotenz | Hostbits | Präfix |
|---|---|---|---|---|
| A | 102 | 128 = 2^7 | 7 | 32 − 7 = **/25** |
| B | 52 | 64 = 2^6 | 6 | 32 − 6 = **/26** |
| C | 27 | 32 = 2^5 | 5 | 32 − 5 = **/27** |
| D | 12 | 16 = 2^4 | 4 | 32 − 4 = **/28** |

Kontrolle: 128 + 64 + 32 + 16 = 240 ≤ 256, es passt in das /24.

### Schritt 2: Der Reihe nach vergeben

**Netz A (/25, Blockgröße 128):**

- Start: `192.168.10.0`
- Nächster Start: 0 + 128 = 128, also Broadcast = 128 − 1 = `192.168.10.127`
- Hosts: `.1` bis `.126`

**Netz B (/26, Blockgröße 64):**

- Start: `192.168.10.128` (direkt nach A)
- Nächster Start: 128 + 64 = 192, also Broadcast `192.168.10.191`
- Hosts: `.129` bis `.190`

**Netz C (/27, Blockgröße 32):**

- Start: `192.168.10.192`
- Nächster Start: 192 + 32 = 224, also Broadcast `192.168.10.223`
- Hosts: `.193` bis `.222`

**Netz D (/28, Blockgröße 16):**

- Start: `192.168.10.224`
- Nächster Start: 224 + 16 = 240, also Broadcast `192.168.10.239`
- Hosts: `.225` bis `.238`

Übrig bleibt `192.168.10.240` bis `.255` (ein freies /28).

### Ergebnis

| Netz | Netzadresse/Präfix | Subnetzmaske | Broadcast | Host-Bereich |
|---|---|---|---|---|
| A | 192.168.10.0/25 | 255.255.255.128 | 192.168.10.127 | .1 – .126 |
| B | 192.168.10.128/26 | 255.255.255.192 | 192.168.10.191 | .129 – .190 |
| C | 192.168.10.192/27 | 255.255.255.224 | 192.168.10.223 | .193 – .222 |
| D | 192.168.10.224/28 | 255.255.255.240 | 192.168.10.239 | .225 – .238 |

### Schritt 3 (zum Verstehen): Dasselbe binär für Netz B

Netz B ist `192.168.10.128/26`. Nur das letzte Oktett ändert sich, die ersten drei sind fest. Das letzte Oktett hat bei /26 **2 Netzbits und 6 Hostbits**:

```text
Netzadresse:   10 000000  = 128   (Hostbits alle 0)
Broadcast:     10 111111  = 191   (Hostbits alle 1)
erster Host:   10 000001  = 129
letzter Host:  10 111110  = 190
```

Die zwei festen Bits `10` sind das, was dieses Subnetz von den anderen unterscheidet. Alle 6 Hostbits dürfen frei variieren: 2^6 = 64 Adressen, davon 62 nutzbar.

Genau so entstehen die Blöcke bei einem /26:

```text
00 000000 = 0     → Netz 1 (0–63)
01 000000 = 64    → Netz 2 (64–127)
10 000000 = 128   → Netz 3 (128–191)
11 000000 = 192   → Netz 4 (192–255)
```

Beim Teilen "leihst" du dir also Bits vom Hostteil und machst sie zu Netzbits. Jedes geliehene Bit **verdoppelt die Zahl der Netze** und **halbiert deren Größe**.

---

## Teil 4: Zusatzwissen

### In welchem Subnetz liegt eine IP?

Beispiel: `192.168.1.77/26`, Blockgröße 64.

- Das Vielfache von 64, das **nicht größer als 77** ist: 64.
- Netzadresse = `192.168.1.64`
- Nächster Block beginnt bei 128, also Broadcast = `192.168.1.127`
- Hosts: `.65` bis `.126`

### Wenn das Präfix nicht auf Oktettgrenze liegt (z. B. /18)

Das Prinzip bleibt gleich, aber du schaust auf das Oktett, in dem die Grenze liegt:

- /18 = 16 + 2 → Grenze im **3. Oktett**, dort 2 Netzbits → Blockgröße 64 **im 3. Oktett**.
- Netze: `x.y.0.0`, `x.y.64.0`, `x.y.128.0`, `x.y.192.0`. Der Broadcast ist dann `x.y.63.255` usw. (das 4. Oktett ist komplett Host, also .255).

### Maske ↔ Präfix umrechnen

Zähle die Einsen. `255.255.255.224`: 24 Einsen + `224 = 11100000` (3 Einsen) → **/27**.

---

## Teil 5: Übungsaufgaben

Rechne zuerst selbst, dann vergleiche mit den Lösungen in Teil 6.

### Aufgabe 1: Maske und Präfix

a) Gib die Subnetzmaske für **/28** an.
b) Gib das Präfix für **255.255.255.224** an.
c) Wie viele nutzbare Hosts hat ein **/29**?
d) Wie viele nutzbare Hosts hat ein **/22**? Welche Subnetzmaske hat es?

### Aufgabe 2: Netz bestimmen

Gegeben: `192.168.2.200/27`.

a) Wie lauten Netzadresse und Broadcast-Adresse?
b) Wie lautet der Host-Bereich?
c) Liegt `192.168.2.190` im selben Subnetz?

### Aufgabe 3: In gleich große Netze teilen

Teile `172.16.20.0/24` in **vier** gleich große Netze. Gib für jedes Netz Netzadresse mit Präfix und Broadcast an.

### Aufgabe 4: Mehr gleiche Netze

Teile `10.0.5.0/24` in **16** gleich große Netze.

a) Welches Präfix und wie viele Hosts pro Netz?
b) Gib die ersten drei und das letzte Netz mit Broadcast an.

### Aufgabe 5: VLSM (leicht)

Teile `172.16.8.0/24` in drei Netze: **100 Hosts, 50 Hosts, 50 Hosts**. Gib je Netz Netzname mit Präfix und Broadcast an.

### Aufgabe 6: VLSM (mittel)

Teile `192.168.100.0/24` in vier Netze mit **60, 30, 12 und 2 Hosts**. Gib je Netz Netzname mit Präfix, Broadcast und Host-Bereich an.

### Aufgabe 7: Präfix über Oktettgrenze

Teile `10.20.0.0/16` in **vier** gleich große Netze. Gib Netzadressen mit Präfix und Broadcast an.

---

## Teil 6: Lösungen

### Lösung 1

a) /28 → `255.255.255.240`
b) 255.255.255.224 → **/27** (24 + 3 Einsen)
c) /29 hat 3 Hostbits → 2³ − 2 = **6** Hosts
d) /22 hat 10 Hostbits → 2¹⁰ − 2 = **1022** Hosts. Maske: 22 = 8 + 8 + 6, also `255.255.252.0` (6 Einsen im 3. Oktett = 252).

### Lösung 2

Blockgröße /27 = 32. Vielfache von 32: …, 160, **192**, 224. Die 200 liegt im Block ab 192.

a) Netz `192.168.2.192`, Broadcast `192.168.2.223`
b) Hosts `192.168.2.193` bis `192.168.2.222`
c) Nein. `.190` liegt im Block 160–191 (Netz `192.168.2.160/27`).

### Lösung 3

4 Netze = 2² → /24 + 2 = **/26**, Blockgröße 64.

| Netz | Broadcast |
|---|---|
| 172.16.20.0/26 | 172.16.20.63 |
| 172.16.20.64/26 | 172.16.20.127 |
| 172.16.20.128/26 | 172.16.20.191 |
| 172.16.20.192/26 | 172.16.20.255 |

### Lösung 4

16 Netze = 2⁴ → /24 + 4 = **/28**, Blockgröße 16, 14 Hosts pro Netz.

| Netz | Broadcast |
|---|---|
| 10.0.5.0/28 | 10.0.5.15 |
| 10.0.5.16/28 | 10.0.5.31 |
| 10.0.5.32/28 | 10.0.5.47 |
| … | … |
| 10.0.5.240/28 | 10.0.5.255 |

### Lösung 5

Größtes zuerst: 100 + 2 = 102 → 128 → **/25**. 50 + 2 = 52 → 64 → **/26**.

| Netz | Broadcast |
|---|---|
| 172.16.8.0/25 (100 Hosts) | 172.16.8.127 |
| 172.16.8.128/26 (50 Hosts) | 172.16.8.191 |
| 172.16.8.192/26 (50 Hosts) | 172.16.8.255 |

Es bleibt nichts übrig, das /24 ist komplett belegt.

### Lösung 6

60 + 2 = 62 → 64 → /26. 30 + 2 = 32 → 32 → /27. 12 + 2 = 14 → 16 → /28. 2 + 2 = 4 → 4 → /30.

| Netz | Broadcast | Host-Bereich |
|---|---|---|
| 192.168.100.0/26 | 192.168.100.63 | .1 – .62 |
| 192.168.100.64/27 | 192.168.100.95 | .65 – .94 |
| 192.168.100.96/28 | 192.168.100.111 | .97 – .110 |
| 192.168.100.112/30 | 192.168.100.115 | .113 – .114 |

Alle Netze folgen lückenlos aufeinander (0 → 64 → 96 → 112 → 116).

### Lösung 7

4 Netze = 2² → /16 + 2 = **/18**. Die Grenze liegt im 3. Oktett, Blockgröße dort 64.

| Netz | Broadcast |
|---|---|
| 10.20.0.0/18 | 10.20.63.255 |
| 10.20.64.0/18 | 10.20.127.255 |
| 10.20.128.0/18 | 10.20.191.255 |
| 10.20.192.0/18 | 10.20.255.255 |

---

## Merkzettel für die Klausur

1. **Hosts + 2**, dann auf die Zweierpotenz aufrunden.
2. **Präfix = 32 − Hostbits.**
3. **Größtes Netz zuerst**, lückenlos hintereinander.
4. **Broadcast = Start des nächsten Netzes − 1.**
5. Immer prüfen: Alle Blöcke zusammen dürfen das Ausgangsnetz nicht überschreiten.
