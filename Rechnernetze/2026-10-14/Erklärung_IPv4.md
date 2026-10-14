# IPv4-Adressierung, CIDR und Subnetting

> Skript auf Uni-Niveau: Aufbau von IPv4-Adressen, Subnetzmasken, CIDR-Notation, Subnetting (FLSM/VLSM), Aggregation, Übungsaufgaben mit ausführlichen Lösungen.

---

## Inhaltsverzeichnis

1. [Aufbau einer IPv4-Adresse](#1-aufbau-einer-ipv4-adresse)
2. [Netzanteil, Hostanteil und Subnetzmaske](#2-netzanteil-hostanteil-und-subnetzmaske)
3. [CIDR-Notation](#3-cidr-notation)
4. [Besondere Adressen](#4-besondere-adressen)
5. [Rechenverfahren: Die Blockgrößen-Methode](#5-rechenverfahren-die-blockgrößen-methode)
6. [Subnetting](#6-subnetting)
7. [Warum ist 10.0.2.0/22 kein gültiges Netz?](#7-warum-ist-1002022-kein-gültiges-netz)
8. [Supernetting / Route Aggregation](#8-supernetting--route-aggregation)
9. [Übungsaufgaben mit Lösungen](#9-übungsaufgaben-mit-lösungen)
10. [Zusammenfassung / Spickzettel](#10-zusammenfassung--spickzettel)

---

## 1. Aufbau einer IPv4-Adresse

Eine IPv4-Adresse ist eine **32 Bit lange Binärzahl**. Zur besseren Lesbarkeit wird sie in vier **Oktette** (je 8 Bit) unterteilt, jedes Oktett wird dezimal geschrieben (Wertebereich 0–255) und durch Punkte getrennt (*dotted decimal notation*).

```
Dezimal:   192      .   168      .    10      .    77
Binär:     11000000 . 10101000 . 00001010 . 01001101
Bit-Pos.:  31......24  23......16  15.....8   7......0
```

**Stellenwerte innerhalb eines Oktetts:**

| Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|---|---|
| Wert | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |

Beispiel: `01001101` = 64 + 8 + 4 + 1 = **77**.

Der gesamte Adressraum umfasst 2³² = 4 294 967 296 Adressen.

### Logischer Aufbau: Netz- und Hostteil

Jede Adresse besteht aus zwei Teilen:

```
| <-------- Netzanteil (Präfix) --------> | <--- Hostanteil ---> |
|              n Bit                      |      32 - n Bit      |
```

* Der **Netzanteil** identifiziert das (Sub-)Netz. Alle Geräte im selben Netz haben denselben Netzanteil.
* Der **Hostanteil** identifiziert das einzelne Gerät (Interface) innerhalb des Netzes.

Wo die Grenze liegt, bestimmt die **Subnetzmaske** bzw. die **Präfixlänge**.

### Historischer Exkurs: Klassen (classful addressing)

Ursprünglich (RFC 791) war die Grenze fest an die ersten Bits der Adresse gekoppelt:

| Klasse | Erste Bits | Bereich 1. Oktett | Standardmaske | Netze | Hosts/Netz |
|---|---|---|---|---|---|
| A | `0` | 0–127 | /8 | 128 | ≈ 16,7 Mio. |
| B | `10` | 128–191 | /16 | 16 384 | 65 534 |
| C | `110` | 192–223 | /24 | ≈ 2,1 Mio. | 254 |
| D | `1110` | 224–239 | – | Multicast | – |
| E | `1111` | 240–255 | – | reserviert | – |

Dieses Schema war sehr unflexibel (ein Unternehmen mit 300 Hosts brauchte ein Klasse-B-Netz und verschwendete über 65 000 Adressen). Seit **1993 (RFC 1518/1519)** wird es durch **CIDR** (*Classless Inter-Domain Routing*) ersetzt. Die Klassen sind heute nur noch historisch relevant.

---

## 2. Netzanteil, Hostanteil und Subnetzmaske

### 2.1 Die Subnetzmaske

Die **Subnetzmaske** ist ebenfalls eine 32-Bit-Zahl. Sie besteht aus **einer zusammenhängenden Folge von Einsen**, gefolgt von **Nullen**:

* `1` an einer Position → dieses Bit gehört zum **Netzanteil**
* `0` an einer Position → dieses Bit gehört zum **Hostanteil**

Beispiel Maske `255.255.255.0`:

```
11111111.11111111.11111111.00000000
|<------- 24 Netzbits ------>|<-8 Hostbits->
```

**Wichtig:** Gültige Masken haben die Form 1…10…0. Eine Maske wie `255.255.192.128` (`11111111.11111111.11000000.10000000`) ist **ungültig**, da die Einsen nicht zusammenhängend sind.

Mögliche Werte eines „gemischten" Oktetts in einer gültigen Maske:

| Binär | Dezimal | Netzbits im Oktett | Hostbits im Oktett |
|---|---|---|---|
| `00000000` | 0 | 0 | 8 |
| `10000000` | 128 | 1 | 7 |
| `11000000` | 192 | 2 | 6 |
| `11100000` | 224 | 3 | 5 |
| `11110000` | 240 | 4 | 4 |
| `11111000` | 248 | 5 | 3 |
| `11111100` | 252 | 6 | 2 |
| `11111110` | 254 | 7 | 1 |
| `11111111` | 255 | 8 | 0 |

### 2.2 Netzadresse berechnen: bitweises UND

Die **Netzadresse** erhält man, indem man IP-Adresse und Subnetzmaske **bitweise UND-verknüpft**:

```
Netzadresse = IP-Adresse  AND  Subnetzmaske
```

**Beispiel:** `192.168.10.77` mit Maske `255.255.255.192`

```
IP:        11000000.10101000.00001010.01001101   (192.168.10.77)
Maske:     11111111.11111111.11111111.11000000   (255.255.255.192)
---------------------------------------------------------------
UND:       11000000.10101000.00001010.01000000   (192.168.10.64)
```

Die Netzadresse ist also `192.168.10.64`.

### 2.3 Broadcast-Adresse berechnen

Die **Broadcast-Adresse** (gerichteter Broadcast) entsteht, indem im Hostanteil **alle Bits auf 1** gesetzt werden. Formal:

```
Broadcast = Netzadresse  OR  (NOT Subnetzmaske)
```

Fortsetzung des Beispiels (Wildcard-Maske = invertierte Maske = `0.0.0.63`):

```
Netz:      11000000.10101000.00001010.01000000   (192.168.10.64)
NOT Maske: 00000000.00000000.00000000.00111111   (0.0.0.63)
---------------------------------------------------------------
ODER:      11000000.10101000.00001010.01111111   (192.168.10.127)
```

### 2.4 Nutzbare Hostadressen

In jedem Netz mit *h* Hostbits gibt es 2^h Adressen, davon sind zwei reserviert:

* **Alle Hostbits = 0** → Netzadresse (identifiziert das Netz selbst)
* **Alle Hostbits = 1** → Broadcast-Adresse

```
Nutzbare Hosts = 2^h - 2
```

Im Beispiel: h = 6 → 2⁶ − 2 = **62 Hosts**, Bereich `192.168.10.65` bis `192.168.10.126`.

> **Ausnahmen:** Bei **/31** (RFC 3021) werden beide Adressen für Punkt-zu-Punkt-Links genutzt, bei **/32** bezeichnet die Adresse genau einen Host (z. B. Loopback, Host-Routen).

---

## 3. CIDR-Notation

### 3.1 Definition

Bei **CIDR** (*Classless Inter-Domain Routing*) wird die Länge des Netzanteils direkt hinter der Adresse als **Präfixlänge** angegeben:

```
<IP-Adresse>/<Präfixlänge>
```

Die Zahl nach dem Schrägstrich gibt an, **wie viele der 32 Bit zum Netzanteil gehören** (= Anzahl der führenden Einsen in der Subnetzmaske).

| CIDR | Subnetzmaske | Binär |
|---|---|---|
| `/8` | 255.0.0.0 | `11111111.00000000.00000000.00000000` |
| `/16` | 255.255.0.0 | `11111111.11111111.00000000.00000000` |
| `/22` | 255.255.252.0 | `11111111.11111111.11111100.00000000` |
| `/24` | 255.255.255.0 | `11111111.11111111.11111111.00000000` |
| `/27` | 255.255.255.224 | `11111111.11111111.11111111.11100000` |

### 3.2 Umrechnung Präfixlänge → Subnetzmaske

**Verfahren:** Schreibe *n* Einsen, fülle auf 32 Bit mit Nullen auf, gruppiere in Oktette.

**Beispiel /20:**

```
20 Einsen:  11111111.11111111.11110000.00000000
Dezimal:    255     .255     .240     .0
```

Kurzform: 20 = 8 + 8 + 4 → zwei volle Oktette (255), ein Oktett mit 4 Einsen (`11110000` = 240), Rest 0.

### 3.3 Umrechnung Subnetzmaske → Präfixlänge

Zähle die Einsen. Bei `255.255.255.224`: 8 + 8 + 8 + 3 (`224 = 11100000`) = **/27**.

### 3.4 Referenztabelle

| CIDR | Maske | Hostbits h | Adressen 2^h | Nutzbare Hosts |
|---|---|---|---|---|
| /8 | 255.0.0.0 | 24 | 16 777 216 | 16 777 214 |
| /16 | 255.255.0.0 | 16 | 65 536 | 65 534 |
| /20 | 255.255.240.0 | 12 | 4 096 | 4 094 |
| /22 | 255.255.252.0 | 10 | 1 024 | 1 022 |
| /23 | 255.255.254.0 | 9 | 512 | 510 |
| /24 | 255.255.255.0 | 8 | 256 | 254 |
| /25 | 255.255.255.128 | 7 | 128 | 126 |
| /26 | 255.255.255.192 | 6 | 64 | 62 |
| /27 | 255.255.255.224 | 5 | 32 | 30 |
| /28 | 255.255.255.240 | 4 | 16 | 14 |
| /29 | 255.255.255.248 | 3 | 8 | 6 |
| /30 | 255.255.255.252 | 2 | 4 | 2 |
| /31 | 255.255.255.254 | 1 | 2 | 2 (RFC 3021) |
| /32 | 255.255.255.255 | 0 | 1 | 1 (Host-Route) |

### 3.5 Vorteile von CIDR

* **Flexible Netzgrößen**: Präfixlängen von /0 bis /32 statt nur /8, /16, /24.
* **Weniger Adressverschwendung**: Netze passen zur tatsächlichen Hostzahl.
* **Route Aggregation**: Mehrere Netze lassen sich zu einem Präfix zusammenfassen, das hält Routing-Tabellen klein (siehe Abschnitt 8).

---

## 4. Besondere Adressen

| Bereich | Bedeutung |
|---|---|
| `0.0.0.0/8` | „Dieses Netz"; `0.0.0.0` = unspezifiziert, `0.0.0.0/0` = Default-Route |
| `10.0.0.0/8` | **Privat** (RFC 1918) |
| `172.16.0.0/12` | **Privat** (RFC 1918): `172.16.0.0`–`172.31.255.255` |
| `192.168.0.0/16` | **Privat** (RFC 1918) |
| `100.64.0.0/10` | Carrier-Grade NAT (RFC 6598) |
| `127.0.0.0/8` | Loopback (`127.0.0.1` = localhost) |
| `169.254.0.0/16` | Link-Local (APIPA, wenn kein DHCP antwortet) |
| `224.0.0.0/4` | Multicast |
| `240.0.0.0/4` | Reserviert |
| `255.255.255.255` | Limited Broadcast (nur im lokalen Segment) |

---

## 5. Rechenverfahren: Die Blockgrößen-Methode

Binäre UND-Verknüpfungen sind exakt, aber langsam. Schneller geht es mit der **Blockgröße** (*magic number*).

### Vorgehen

1. Finde das **„interessante" Oktett**: das Oktett, in dem die Maske weder 255 noch 0 ist (also die Grenze zwischen Netz und Host liegt).
2. Berechne die **Blockgröße**: `256 − (Maskenwert im interessanten Oktett)`.
3. Die Netzadressen in diesem Oktett sind genau die **Vielfachen der Blockgröße** (0, B, 2B, 3B, …).
4. Die IP-Adresse liegt im Block, dessen Startwert ≤ Oktettwert < nächster Startwert.
5. **Netzadresse** = Blockanfang; **Broadcast** = (nächster Blockanfang − 1) im interessanten Oktett, alle folgenden Oktette 255.

### Warum funktioniert das?

Hat das interessante Oktett *k* Hostbits, dann ist die Blockgröße 2^k. Die letzten *k* Bits einer Netzadresse müssen 0 sein, das sind genau die Vielfachen von 2^k.

### Beispiel

`172.16.37.200/20` → Maske `255.255.240.0`; interessantes Oktett: das dritte; Blockgröße = 256 − 240 = **16**.
Blöcke im 3. Oktett: 0, 16, **32**, 48, … → 37 liegt im Block 32–47.

* Netzadresse: `172.16.32.0`
* Broadcast: `172.16.47.255`
* Hosts: `172.16.32.1` – `172.16.47.254`

---

## 6. Subnetting

**Subnetting** bedeutet, ein größeres Netz in mehrere kleinere Teilnetze zu zerlegen. Dazu werden Bits vom **Hostanteil in den Netzanteil** „geliehen".

```
Vorher:   | Netz (n Bit)          | Host (32-n Bit)             |
Nachher:  | Netz (n Bit) | Subnet (s Bit) | Host (32-n-s Bit)   |
```

Gründe: Trennung von Abteilungen/VLANs, Broadcast-Domänen verkleinern, Sicherheitszonen, effiziente Adressnutzung.

### 6.1 Grundformeln

Werden *s* Bit geliehen:

```
Anzahl Subnetze     = 2^s
Neue Präfixlänge    = n + s
Hostbits pro Subnetz = 32 - (n + s)
Nutzbare Hosts      = 2^(32-(n+s)) - 2
Blockgröße (im interessanten Oktett) = 2^(Hostbits im Oktett)
```

### 6.2 FLSM: Fixed Length Subnet Masks

Alle Subnetze sind **gleich groß**.

**Beispiel:** `192.168.1.0/24` in mindestens 6 Subnetze teilen.

1. 2^s ≥ 6 → s = 3 (2³ = 8 Subnetze).
2. Neue Länge: 24 + 3 = **/27** (Maske `255.255.255.224`).
3. Hostbits: 5 → 2⁵ − 2 = **30 Hosts** pro Subnetz.
4. Blockgröße: 32.

| Nr. | Netzadresse | Hostbereich | Broadcast |
|---|---|---|---|
| 0 | 192.168.1.0/27 | .1 – .30 | .31 |
| 1 | 192.168.1.32/27 | .33 – .62 | .63 |
| 2 | 192.168.1.64/27 | .65 – .94 | .95 |
| 3 | 192.168.1.96/27 | .97 – .126 | .127 |
| 4 | 192.168.1.128/27 | .129 – .158 | .159 |
| 5 | 192.168.1.160/27 | .161 – .190 | .191 |
| 6 | 192.168.1.192/27 | .193 – .222 | .223 |
| 7 | 192.168.1.224/27 | .225 – .254 | .255 |

### 6.3 VLSM: Variable Length Subnet Masks

Subnetze haben **unterschiedliche Größen**, angepasst an den jeweiligen Bedarf. Das ist heute der Normalfall.

**Algorithmus:**

1. Bedarf je Subnetz bestimmen: Hosts **+ 2** (Netz- und Broadcast-Adresse; ggf. + Gateway einrechnen).
2. Für jedes Subnetz die **kleinste Zweierpotenz ≥ Bedarf** wählen → daraus Hostbits *h* und Präfix `/(32−h)`.
3. Subnetze **nach Größe absteigend sortieren**.
4. Der Reihe nach vergeben, beginnend am Anfang des Adressraums. Jedes Subnetz startet direkt hinter dem vorherigen.

Absteigende Sortierung garantiert, dass jedes Subnetz an einer Adresse beginnt, die ein Vielfaches seiner Blockgröße ist (Ausrichtung/Alignment, siehe Abschnitt 7).

---

## 7. Warum ist 10.0.2.0/22 kein gültiges Netz?

> **Frage:** Warum geht `10.0.2.0/22` als Netz nicht, aber `10.0.4.0/22` und `10.0.0.0/22` schon?

### 7.1 Die Regel

Eine Netzadresse mit Präfix `/n` ist nur gültig, wenn **alle Hostbits = 0** sind. Äquivalent: `Adresse AND Maske = Adresse`. Anders gesagt: die Adresse muss an der **Blockgrenze** liegen, also ein Vielfaches der Netzgröße sein.

### 7.2 Nachrechnen mit /22

`/22` = 22 Netzbits, 10 Hostbits. Verteilung auf die Oktette:

* 1. Oktett: 8 Netzbits
* 2. Oktett: 8 Netzbits
* 3. Oktett: **6 Netzbits, 2 Hostbits** ← das „interessante" Oktett
* 4. Oktett: 8 Hostbits

Maske: `255.255.252.0`; Blockgröße im 3. Oktett: 256 − 252 = **4**.
Gültige Netzadressen haben im 3. Oktett also die Werte **0, 4, 8, 12, 16, …**

### 7.3 Binärvergleich

Maske im 3. Oktett: `11111100`. Die letzten **2 Bit** des 3. Oktetts sind Hostbits und müssen 0 sein.

| Adresse | 3. Oktett binär | Hostbits (letzte 2) | Alle 0? | Gültiges Netz? |
|---|---|---|---|---|
| `10.0.0.0/22` | `000000`**`00`** | `00` | ✅ | **ja** |
| `10.0.2.0/22` | `000000`**`10`** | `10` | ❌ | **nein** |
| `10.0.4.0/22` | `000001`**`00`** | `00` | ✅ | **ja** |

Per UND-Verknüpfung für `10.0.2.0/22`:

```
IP:      00001010.00000000.00000010.00000000   (10.0.2.0)
Maske:   11111111.11111111.11111100.00000000   (255.255.252.0)
------------------------------------------------------------
UND:     00001010.00000000.00000000.00000000   (10.0.0.0)   ≠ 10.0.2.0
```

Das Ergebnis ist `10.0.0.0`, nicht `10.0.2.0`. Die Adresse `10.0.2.0` **gehört also zum Netz `10.0.0.0/22`** und ist dort nicht die Netzadresse.

### 7.4 Die /22-Blöcke im Überblick

Ein /22 umfasst 1024 Adressen = 4 aufeinanderfolgende /24-Blöcke:

| Netz | Adressbereich | Entspricht 3. Oktett |
|---|---|---|
| `10.0.0.0/22` | 10.0.0.0 – 10.0.3.255 | 0, 1, 2, 3 |
| `10.0.4.0/22` | 10.0.4.0 – 10.0.7.255 | 4, 5, 6, 7 |
| `10.0.8.0/22` | 10.0.8.0 – 10.0.11.255 | 8, 9, 10, 11 |
| `10.0.12.0/22` | 10.0.12.0 – 10.0.15.255 | 12, 13, 14, 15 |

`10.0.2.0` liegt mitten im ersten Block (`10.0.0.0/22`), also nicht an einer Blockgrenze. Man könnte die Netze nur „bei 2" beginnen lassen, wenn sie die Größe 2 (im 3. Oktett) hätten, das wäre ein **/23** (`10.0.2.0/23` ist gültig: 2 ist Vielfaches von 2).

### 7.5 Genauigkeit: Netzadresse ≠ Hostadresse

`10.0.2.0/22` ist als **Schreibweise** nicht verboten. Es kann z. B. eine **Interface-Konfiguration** sein: Die Adresse `10.0.2.0` ist innerhalb von `10.0.0.0/22` weder Netz- noch Broadcast-Adresse, also sogar eine **nutzbare Hostadresse** (sie ist nur für Menschen verwirrend, weil sie auf `.0` endet). Als **Netzadresse** (z. B. in einer Routing-Tabelle oder Firewall-Regel) ist sie hingegen **ungültig**; viele Geräte lehnen den Eintrag ab oder normalisieren ihn automatisch auf `10.0.0.0/22`.

### 7.6 Merkregel

> Eine Netzadresse `/n` ist gültig, wenn der Wert im interessanten Oktett ein **ganzzahliges Vielfaches der Blockgröße** ist.
> Für `/22` gilt: Blockgröße 4 → 0, 4, 8, … gültig; 1, 2, 3, 5, 6, 7, … ungültig.

---

## 8. Supernetting / Route Aggregation

Das Gegenstück zum Subnetting: Mehrere aufeinanderfolgende Netze werden zu **einem größeren Präfix** zusammengefasst, indem Netzbits **zurück in den Hostanteil** verschoben werden.

**Bedingungen für Aggregation von 2^k Netzen:**

1. Die Netze sind **zusammenhängend** (lückenlos).
2. Alle Netze haben **dieselbe Größe**.
3. Die erste Netzadresse ist **durch die Gesamtgröße teilbar** (Ausrichtung, wie in Abschnitt 7).

**Beispiel:** `192.168.4.0/24`, `192.168.5.0/24`, `192.168.6.0/24`, `192.168.7.0/24`

3. Oktett binär: `00000100`, `00000101`, `00000110`, `00000111`; die ersten 6 Bit sind identisch (`000001`), nur die letzten 2 Bit variieren.
→ gemeinsames Präfix: 16 + 6 = **/22** → `192.168.4.0/22` (4 ist Vielfaches von 4 ✅).

**Gegenbeispiel:** `192.168.5.0/24` + `192.168.6.0/24` ergeben **kein** /23, denn 5 ist kein Vielfaches von 2 (`00000101` vs. `00000110` unterscheiden sich schon im vorletzten Bit).

---

## 9. Übungsaufgaben mit Lösungen

### Aufgabe 1: Netzadresse, Broadcast, Hostbereich

Gegeben: `192.168.10.77/26`. Bestimme Subnetzmaske, Netzadresse, Broadcast-Adresse, Hostbereich und Anzahl nutzbarer Hosts.

**Lösung**

*Schritt 1: Maske.* /26 = 8 + 8 + 8 + 2 Einsen → letztes Oktett `11000000` = 192 → **255.255.255.192**.

*Schritt 2: Hostbits.* 32 − 26 = 6 → 2⁶ = 64 Adressen, **62 nutzbare Hosts**.

*Schritt 3: Blockgröße.* 256 − 192 = 64. Blöcke im 4. Oktett: 0, 64, 128, 192. Die 77 liegt im Block 64–127.

*Schritt 4: Ergebnis.*

* Netzadresse: **192.168.10.64**
* Broadcast: **192.168.10.127**
* Hostbereich: **192.168.10.65 – 192.168.10.126**

*Probe (binär):* `77 = 01001101`, AND `11000000` = `01000000` = 64 ✅.

---

### Aufgabe 2: Netz über zwei Oktette

Gegeben: `172.16.37.200/20`. Bestimme Netzadresse, Broadcast und Hostanzahl.

**Lösung**

*Maske:* /20 = 8 + 8 + 4 → `255.255.240.0`. Interessantes Oktett: das dritte. Blockgröße: 256 − 240 = **16**.

*Block:* Vielfache von 16: …, 32, 48, … → 37 liegt im Block 32–47.

*Binär zur Kontrolle:* 37 = `00100101`, Maske `11110000` → UND = `00100000` = 32 ✅.

* Netzadresse: **172.16.32.0**
* Broadcast: **172.16.47.255** (3. Oktett: 47 = nächster Block 48 − 1; 4. Oktett alle Hostbits 1 → 255)
* Hostbereich: 172.16.32.1 – 172.16.47.254
* Hostbits: 12 → 2¹² − 2 = **4094 Hosts**

---

### Aufgabe 3: FLSM-Subnetting

Teile `192.168.1.0/24` in **4 gleich große Subnetze**. Gib für jedes Subnetz Netzadresse, nutzbaren Bereich und Broadcast an.

**Lösung**

*Bits leihen:* 2^s ≥ 4 → s = 2. Neue Länge: 24 + 2 = **/26** (Maske `255.255.255.192`). Hostbits: 6 → 62 Hosts. Blockgröße: 64.

| Subnetz | Netzadresse | Nutzbarer Bereich | Broadcast |
|---|---|---|---|
| 1 | 192.168.1.0/26 | .1 – .62 | .63 |
| 2 | 192.168.1.64/26 | .65 – .126 | .127 |
| 3 | 192.168.1.128/26 | .129 – .190 | .191 |
| 4 | 192.168.1.192/26 | .193 – .254 | .255 |

*Binäre Sicht:* Die beiden geliehenen Bits (Bit 7 und 6 des 4. Oktetts) nehmen die Werte `00`, `01`, `10`, `11` an → 0, 64, 128, 192.

---

### Aufgabe 4: VLSM

Das Netz `10.10.0.0/24` soll auf vier Segmente aufgeteilt werden:

| Segment | Benötigte Hosts |
|---|---|
| A (Entwicklung) | 100 |
| B (Verwaltung) | 50 |
| C (Gäste-WLAN) | 25 |
| D (Router-Link) | 2 |

**Lösung**

*Schritt 1: Adressbedarf = Hosts + 2, aufrunden auf Zweierpotenz.*

| Segment | Hosts + 2 | Zweierpotenz | Hostbits h | Präfix | Nutzbare Hosts |
|---|---|---|---|---|---|
| A | 102 | 128 = 2⁷ | 7 | /25 | 126 |
| B | 52 | 64 = 2⁶ | 6 | /26 | 62 |
| C | 27 | 32 = 2⁵ | 5 | /27 | 30 |
| D | 4 | 4 = 2² | 2 | /30 | 2 |

*Schritt 2: Absteigend sortiert vergeben* (bereits sortiert).

| Segment | Netzadresse | Hostbereich | Broadcast | Nächster freier Start |
|---|---|---|---|---|
| A | 10.10.0.0/25 | .1 – .126 | .127 | .128 |
| B | 10.10.0.128/26 | .129 – .190 | .191 | .192 |
| C | 10.10.0.192/27 | .193 – .222 | .223 | .224 |
| D | 10.10.0.224/30 | .225 – .226 | .227 | .228 |

*Ergebnis:* Es werden 228 von 256 Adressen belegt, **10.10.0.228 – 10.10.0.255** (28 Adressen) bleiben frei für Erweiterungen.

*Kontrolle der Ausrichtung:* 0 (Vielfaches von 128 ✅), 128 (Vielfaches von 64 ✅), 192 (Vielfaches von 32 ✅), 224 (Vielfaches von 4 ✅).

*Warum die Sortierung wichtig ist:* Würde man D (/30) zuerst bei .0 vergeben, könnte A (/25) erst bei .128 beginnen, und es entstünden Lücken bzw. Platzprobleme.

---

### Aufgabe 5: Ist das eine gültige Netzadresse?

Prüfe jeweils, ob die Adresse als **Netzadresse** gültig ist. Falls nicht, gib das Netz an, zu dem sie gehört.

| # | Adresse |
|---|---|
| a | `172.16.16.0/20` |
| b | `192.168.1.64/25` |
| c | `10.1.0.0/15` |
| d | `192.168.1.128/25` |

**Lösung**

**a)** /20 → 4 Hostbits im 3. Oktett, Blockgröße 16. 16 ist Vielfaches von 16 → ✅ **gültig** (Bereich 172.16.16.0 – 172.16.31.255).

**b)** /25 → 7 Hostbits im 4. Oktett, Blockgröße 128 (Blöcke: 0, 128). 64 ist kein Vielfaches von 128 → ❌ **ungültig**. Binär: `64 = 01000000`, das höchste Hostbit (Wert 64) ist gesetzt. Gehört zu **192.168.1.0/25** (.0 – .127).

**c)** /15 → 7 Netzbits im 2. Oktett, **1 Hostbit** im 2. Oktett, Blockgröße 2 (Blöcke: 0, 2, 4, …). Der Wert 1 ist kein Vielfaches von 2 → ❌ **ungültig**. Gehört zu **10.0.0.0/15** (10.0.0.0 – 10.1.255.255).

**d)** /25, Blockgröße 128; 128 ist Vielfaches von 128 → ✅ **gültig** (Bereich 192.168.1.128 – .255).

---

### Aufgabe 6: Maske ↔ CIDR

a) Gib `255.255.248.0` in CIDR-Notation an.
b) Welche Maske gehört zu `/29`?
c) Ist `255.255.192.128` eine gültige Subnetzmaske?

**Lösung**

**a)** `248 = 11111000` → 5 Einsen. 8 + 8 + 5 = **/21**.

**b)** /29 = 8 + 8 + 8 + 5 → letztes Oktett `11111000` = 248 → **255.255.255.248** (3 Hostbits → 6 nutzbare Hosts).

**c)** Binär: `11111111.11111111.11000000.10000000`. Nach den Nullen im 3. Oktett (`000000`) folgt im 4. Oktett wieder eine `1` → die Einsen sind nicht zusammenhängend → ❌ **ungültig**.

---

### Aufgabe 7: Gleiches Subnetz?

Liegen `10.0.3.250` und `10.0.4.5` jeweils mit Präfix **/22** im selben Subnetz? Und mit Präfix **/21**?

**Lösung**

*/22:* Blockgröße im 3. Oktett = 4.

* `10.0.3.250` → 3. Oktett 3 liegt im Block 0–3 → Netz **10.0.0.0/22**
* `10.0.4.5` → 3. Oktett 4 liegt im Block 4–7 → Netz **10.0.4.0/22**

→ **Verschiedene Subnetze**, obwohl die Adressen direkt benachbart sind. Kommunikation läuft über einen Router.

*/21:* Maske `255.255.248.0`, Blockgröße 8 im 3. Oktett. Beide 3. Oktette (3 und 4) liegen im Block 0–7 → beide im Netz **10.0.0.0/21** → **gleiches Subnetz**.

*Lehre:* Die Entscheidung „gleiches Subnetz oder nicht" hängt immer vom Präfix ab, nicht von der „Nähe" der Adressen.

---

### Aufgabe 8: Aggregation

Fasse die Netze `10.20.8.0/24`, `10.20.9.0/24`, `10.20.10.0/24`, `10.20.11.0/24` zu einem Präfix zusammen. Ist das exakt möglich?

**Lösung**

3. Oktett binär: 8 = `00001000`, 9 = `00001001`, 10 = `00001010`, 11 = `00001011`.
Gemeinsame führende Bits: `000010` (6 Bit); die letzten 2 Bit variieren (4 Netze = 2²).

Präfix: 16 + 6 = **/22** → **10.20.8.0/22**.

*Prüfung der Ausrichtung:* Blockgröße 4, und 8 ist ein Vielfaches von 4 ✅. Die Zusammenfassung ist exakt, ohne zusätzliche Adressen.

*Variante:* Bei `10.20.9.0/24`–`10.20.12.0/24` wäre das nicht exakt möglich (9 ist kein Vielfaches von 4); man bräuchte mehrere Einträge, z. B. `10.20.9.0/24`, `10.20.10.0/23`, `10.20.12.0/24`.

---

### Aufgabe 9: Subnetz-Planung mit Hostanforderung

Ein Unternehmen erhält `172.20.0.0/16` und braucht mindestens **500 Subnetze** mit je mindestens **100 Hosts**. Welche Präfixlänge ist geeignet?

**Lösung**

*Subnetze:* 2^s ≥ 500 → s = 9 (2⁹ = 512). Neue Länge: 16 + 9 = /25.

*Hosts prüfen:* /25 → 7 Hostbits → 2⁷ − 2 = 126 ≥ 100 ✅.

→ **/25** (Maske `255.255.255.128`): 512 Subnetze mit je 126 Hosts. Das ist die einzige passende Wahl, da /26 nur 62 Hosts (< 100) und /24 nur 256 Subnetze (< 500) liefern würde.

---

## 10. Zusammenfassung / Spickzettel

| Größe | Formel |
|---|---|
| Hostbits | `h = 32 − n` |
| Adressen im Netz | `2^h` |
| Nutzbare Hosts | `2^h − 2` |
| Subnetze beim Leihen von *s* Bit | `2^s` |
| Blockgröße im interessanten Oktett | `256 − Maskenwert` |
| Netzadresse | `IP AND Maske` |
| Broadcast | `Netz OR (NOT Maske)` |
| Gültige Netzadresse | Hostbits alle 0, also Vielfaches der Blockgröße |

**Ablauf bei Standardaufgaben:**

1. Präfix → Maske, interessantes Oktett finden.
2. Blockgröße = 256 − Maskenwert.
3. Passenden Block für die Adresse suchen → Netzadresse.
4. Broadcast = nächster Block − 1.
5. Hosts = 2^h − 2.

**Häufige Fehler:**

* Netz- und Broadcast-Adresse als Host vergeben (bei /30 und größer gibt es 2^h − 2 Hosts).
* Bei VLSM Gateway/Netz-/Broadcast-Adresse im Bedarf vergessen.
* Netzadressen nicht an der Blockgrenze ausrichten (z. B. `10.0.2.0/22`).
* Nicht zusammenhängende Subnetzmasken verwenden.
* Annahme, benachbarte Adressen lägen im selben Subnetz.