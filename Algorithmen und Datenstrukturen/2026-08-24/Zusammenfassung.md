# Algorithmen und Datenstrukturen – Kapitel 1: Einführung
## Zusammenfassende Übersicht mit ausführlicher Erklärung der Grundlagen

Diese Übersicht fasst die Vorlesung (VL) und die Übung (ÜB) zum Thema "Einführung" zusammen. Der Fokus liegt darauf, die grundlegenden Konzepte wirklich zu verstehen, da alle späteren Kapitel (OOP, Grundalgorithmen, Bäume, Hashverfahren, Graphen) auf diesen Begriffen aufbauen.

---

## 1. Die zentralen Grundbegriffe

### 1.1 Algorithmus

Ein **Algorithmus** ist eine Handlungsvorschrift, die aus endlich vielen, eindeutig definierten Einzelschritten besteht. Wichtig ist hier die Betonung auf "endlich" – ein Algorithmus muss (zumindest im klassischen Sinn) irgendwann terminieren und ein Ergebnis liefern.

Man kann sich einen Algorithmus als eine Art Kochrezept vorstellen: Er nimmt eine **Eingabe** entgegen, führt eine feste Abfolge von Schritten aus (die auch Verzweigungen und Wiederholungen enthalten können) und produziert daraus eine **Ausgabe**. Das Konzept ist nicht auf Computer beschränkt – auch das Nachschlagen einer Telefonnummer in einer Liste "von Hand" ist ein Algorithmus.

Die **Church-Turing-These** besagt, dass eine Turing-Maschine (ein einfaches theoretisches Rechenmodell) grundsätzlich in der Lage ist, jeden denkbaren Algorithmus nachzubilden. Das ist die theoretische Grundlage dafür, dass "normale" Computer (die im Kern Turing-äquivalent sind) prinzipiell jedes berechenbare Problem lösen können.

**Merksatz:** Algorithmen sind die Grundlage aller Computerprogramme – jedes Programm ist letztlich die konkrete Umsetzung eines oder mehrerer Algorithmen.

### 1.2 Datum und Daten

Ein **Datum** (Plural: *Daten*) ist eine gemessene, errechnete oder erdachte Information, die eine **konzeptionelle Semantik** (also eine Bedeutung) besitzt. Diese Definition ist bewusst abstrakt gehalten: Ein Datum ist zunächst nichts Technisches, sondern ein Bedeutungsträger.

Daten können unterschiedliche Eigenschaften haben, unter anderem:
- **wahr oder falsch**
- **real oder hypothetisch**
- **relevant oder irrelevant** für einen bestimmten Zweck
- **fehlerhaft oder fehlerfrei**
- **lückenhaft oder lückenlos**
- **konsistent oder widersprüchlich**

Wichtig ist der Unterschied zwischen einem Datum (der abstrakten, bedeutungstragenden Information) und seiner **Repräsentation** (siehe unten) – das Gleiche Datum kann auf ganz unterschiedliche Arten "dargestellt" werden, ohne dass sich seine Bedeutung ändert.

### 1.3 Datenrepräsentation und Datenformat

Da die allermeisten digitalen Rechensysteme ausschließlich mit **Folgen von Bits** umgehen können, muss jedes konzeptionelle Datum in eine solche Bitfolge übersetzt werden. Diese konkrete Darstellung nennt man **Datenrepräsentation**.

Ein **Datenformat** (bzw. **Dateiformat**, wenn es um Dateien geht) ist die begleitende Spezifikation, die festlegt:
1. **wie viele Bits** an welcher Speicherstelle zu einem Datum gehören,
2. welche **Syntax**-Regeln die Bits einhalten müssen,
3. welche **Semantik** die einzelnen Bits gegenüber dem Datum besitzen.

Ein zentraler Punkt: **Ein einzelnes konzeptionelles Datum kann mehrere unterschiedliche Repräsentationen besitzen.** Ein Bild kann z. B. als `.xcf`-Datei, als `.jpg`-Datei oder als reine Bitfolge im Speicher vorliegen – es bleibt inhaltlich "das gleiche Bild", nur die technische Darstellung ändert sich. Ein solcher Wechsel der Repräsentation kann **verlustfrei oder verlustbehaftet** erfolgen (z. B. verliert eine JPEG-Kompression Bildinformationen).

### 1.4 Datenaufbereitung

Die **Datenaufbereitung** beschreibt den Prozess, aus vorhandenen Daten (bzw. deren Repräsentationen) weitere, für nachfolgende Schritte besser geeignete Daten zu gewinnen. Dabei unterscheidet man:

- **Rohdaten**: die möglichst ursprüngliche Repräsentation, z. B. direkt vom Sensor kommend.
- **Abgeleitete Daten**: Daten, die aus anderen Daten (meist Rohdaten) errechnet wurden.

Typische Tätigkeiten der Datenaufbereitung sind:
- Erkennen und Auffüllen lückenhafter Daten
- Erkennen und Verwerfen unwichtiger Daten
- Erkennen und Bereinigen von Fehlern/Widersprüchen
- Ändern des Datenformats bzw. der Repräsentation
- Zusammenführen mehrerer Daten zu einem gemeinsamen Datum

### 1.5 Datenstruktur

Eine **Datenstruktur** ist eine Vorgabe, *wie* Daten und ihre Zusammenhänge in einer konkreten Repräsentation angeordnet werden (z. B. im Arbeitsspeicher). Dieselben Daten können in unterschiedlichen Datenstrukturen (z. B. als Array oder als binärer Suchbaum) organisiert sein – mit jeweils unterschiedlichen Vor- und Nachteilen für nachfolgende Operationen.

### 1.6 Operationen auf Datenstrukturen

Unter **Operationen** versteht man Algorithmen, die gezielt die spezielle Anordnung der Daten in einer Datenstruktur ausnutzen, um ein Ergebnis effizient zu erzielen. Typische Operationen sind u. a.:
- Anlegen/Löschen der gesamten Struktur
- Einfügen neuer Daten (am Anfang, Ende, an vorgegebener oder "richtiger" Stelle)
- Löschen einzelner Daten
- Navigieren zum nächsten/vorherigen Element
- Zugriff auf das n-te Element
- Prüfen, ob ein bestimmtes Datum enthalten ist (und ggf. Auslesen)

### 1.7 Verweise

**Verweise** (Bezüge) zwischen Daten sind meist selbst ein (Teil-)Datum mit eigener Semantik und werden häufig als Pfeil dargestellt. Man unterscheidet:
- **intern relevante Verweise** – wichtig für den Algorithmus selbst (z. B. Sortierstruktur eines Baums)
- **anwendungsrelevante Verweise** – wichtig für den Nutzer/die Anwendung (z. B. Verbindungen zwischen Orten)

---

## 2. Formalisierung einfacher Daten (mathematische Sicht)

Dieser Abschnitt überträgt die oben genannten Begriffe in eine strengere, mathematische Notation – das ist wichtig, um später präzise über Datentypen und Datenstrukturen sprechen zu können.

### 2.1 Grundidee

- Für eine Menge von \(|D|\) konzeptionellen Daten vergibt man eindeutige Namen \(d_i\).
- Diese Namen bilden zusammen eine Menge \(D = \{d_1, d_2, \dots, d_{|D|}\}\).
- Jedem Datum \(d_i\) wird ein **Datentyp** in Form einer Menge zulässiger Werte \(W_i\) zugeordnet (der sogenannte Wertebereich). Wichtig: Auf einem realen Rechner ist \(W_i\) immer **endlich**, in der realen Welt ist das nicht zwingend so (z. B. reelle Zahlen).
- Der tatsächliche Wert wird über eine Funktion \(f: D \rightarrow W\) mit \(f(d_i) = w_i\) modelliert.

Diese Zuordnung ist im mathematischen Sinne **statisch**: Ändert sich ein Wert im Zeitverlauf, handelt es sich formal um ein *neues* Datum (der Index kann z. B. den Messzeitpunkt kodieren).

### 2.2 Zusammengesetzte Daten

Mehrere Einzeldaten lassen sich zu einem neuen, zusammengesetzten Datum kombinieren:

$$\left[ d_j = (d_{i_1}, d_{i_2}, \dots, d_{i_k}) \right]$$

Der Wertebereich des zusammengesetzten Datums ergibt sich als **kartesisches Produkt** der Einzel-Wertebereiche:

$$\left[ W_j = W_{i_1} \times W_{i_2} \times \dots \times W_{i_k} \right]$$

Dabei muss die Wertzuordnungsfunktion konsistent bleiben – der Wert des Gesamtdatums ist immer das Tupel der Einzelwerte.

### 2.3 Unstrukturierte vs. strukturierte Daten

- **Unstrukturierte Daten**: liegen in einer weitgehend unspezifizierten, meist "flachen" Struktur vor (z. B. eine reine Bytefolge oder ein Array eines einzigen Datentyps). Zwischen den Elementen gibt es kaum oder keine expliziten Verweise.
- **Strukturierte Daten**: liegen in einer spezifizierten, höheren Struktur vor (z. B. Liste, Baum, Tabelle mit festgelegten Spalten, allgemeiner Graph). Zwischen den Daten existieren implizit (durch die Struktur) oder explizit modellierte Verweise – etwa Fremdschlüssel-Beziehungen zwischen Tabellen in einer relationalen Datenbank.

---

## 3. Maschinennahe Datenrepräsentation

Dieser Themenblock beschreibt, wie Daten *tatsächlich auf Hardware-Ebene* abgelegt werden.

### 3.1 Binäre Repräsentation einzelner Daten

Jeder Datentyp legt über sein Datenformat fest, wie viele Bits verwendet werden und was diese Bits bedeuten. Beispiele:
- `char` belegt häufig 8 Bit,
- `int` häufig 32 Bit,
- ein `float` nach IEEE-Norm ebenfalls 32 Bit, aber mit einer deutlich komplexeren Umrechnungsvorschrift (Vorzeichen, Exponent, Mantisse).

### 3.2 Speichermodell

Der Speicher (Hauptspeicher, Datenträger, Datei) lässt sich als **lineare Folge von Speicherzellen** auffassen. Jede Zelle fasst üblicherweise 1 Byte (8 Bit) und besitzt eine **Adresse** (ihren Index/Abstand vom Anfang). Bei zusammengesetzten Daten wird per Konvention die *niedrigste* Adresse als Adresse der gesamten Repräsentation verwendet (vergleichbar mit dem `&`-Operator in C/C++).

### 3.3 Zusammengesetzte Daten im Speicher

Eine naheliegende ("naive") Umsetzung legt die Repräsentationen der Einzeldaten einfach **hintereinander in aufeinanderfolgenden Speicherzellen** ab – das entspricht z. B. der klassischen Speicherung eines `struct` in C/C++.

### 3.4 Verweise auf Maschinenebene

Ein **Zeiger** (C/C++) bzw. eine **Referenz** (C++, Java, C#) speichert die Adresse eines anderen Datums. Analoge Konzepte finden sich auch bei anderen linear durchnummerierten Speicherarten, z. B. als relative Position in einer Datei oder als Index in einem Array.

### 3.5 Bewertung

**Vorteile** maschinennaher Repräsentation:
- deutlich schnelleres Rechnen und schnellerer Verweiszugriff (Größenordnung: Faktor 5 bis 1000 gegenüber maschinenfernen Varianten)
- geringerer Speicherplatzbedarf

**Nachteile:**
- für Menschen ohne Aufbereitung schwer nachvollziehbar
- häufig maschinen- bzw. prozessabhängig (z. B. unterschiedliches Speicherlayout), sodass beim Austausch zwischen Systemen eine Konvertierung nötig ist – sonst drohen Datenkorruption oder Fehlinterpretation.

Ein klassisches Beispiel dafür ist die **Byte-Reihenfolge (Endianness)**: Bei *Big Endian* liefert das erste Byte den höchstwertigen Beitrag zum Zahlenwert, bei *Little Endian* das letzte Byte. Dieselbe Bytefolge ergibt je nach Interpretation also einen völlig anderen Zahlenwert.

---

## 4. Maschinenferne Datenrepräsentation

Hier geht es um Repräsentationsformen, die bewusst **unabhängig von konkreter Hardware** gestaltet sind.

### 4.1 Grundidee

Statt einer hardwarenahen Bitfolge wird eine **maschinenunabhängige** Darstellung gewählt – typischerweise menschenlesbarer ASCII-Text (seltener ein maschinenunabhängiges Binärformat). Der Vorteil: Diese Darstellung lässt sich (im Prinzip) auf jedem System gleich interpretieren, unabhängig von internem Speicherlayout oder Prozessorarchitektur.

### 4.2 Zusammengesetzte Daten / Datenformate

Für komplexere, zusammengesetzte Daten werden eigene Datenformate mit strukturierenden Elementen (Schlüsselwörtern, Trennzeichen, Einrückung) definiert. Bekannte Beispiele aus der Praxis sind CSV (kommagetrennte Werte), JSON (JavaScript Object Notation) und XML (Extensible Markup Language) – sie unterscheiden sich vor allem in Lesbarkeit, Verschachtelungstiefe und Ausdrucksstärke.

### 4.3 Verweise auf maschinenferner Ebene

Die Grundidee ist, für eine Datenrepräsentation eine **eindeutige ID** zu erzeugen und in Verweisen nur diese ID statt der eigentlichen Repräsentation anzugeben. Der Zugriff auf das eigentliche Datum erfolgt dann über einen **Lookup**-Schritt, bei dem das System zur ID die passende Repräsentation lokalisiert.

Solche IDs können:
- (teilweise) durch Menschen vergeben werden,
- maschinell durch einen Algorithmus erzeugt werden,
- zufällig generiert werden.

Bekannte Beispiele: **UUID/GUID** (128-Bit-Zahl, teils zufallsbasiert), sowie **URI**-basierte Verfahren wie **ISBN** (für Bücher) oder **URL** (Zugriffsmethode plus Ort).

### 4.4 Bewertung

**Vorteile:**
- problemloser Austausch zwischen Prozessen, Speicherarten und Rechnern
- von Menschen (mehr oder weniger gut) prüfbar

**Nachteile:**
- zusätzlicher Rechenzeitbedarf (komplexere Algorithmen, Umrechnung in maschinennahe Formate, Lookup-Aufwand für Verweise)
- zusätzlicher Speicherbedarf und implizite Redundanz, was wiederum das Risiko von Inkonsistenzen erhöht

---

## 5. Warum diese Unterscheidung so wichtig ist

Der rote Faden des Kapitels lässt sich so zusammenfassen:

| | Maschinennah | Maschinenfern |
|---|---|---|
| Geschwindigkeit | sehr schnell | deutlich langsamer |
| Speicherbedarf | gering | höher (Redundanz) |
| Menschenlesbarkeit | schlecht | meist gut |
| Systemübergreifender Austausch | problematisch | unproblematisch |
| Verweise | einfach zu erzeugen/verfolgen | aufwendiger (Lookup nötig) |

In der Praxis wählt man je nach Anwendungsfall bewusst zwischen beiden Extremen oder kombiniert sie (z. B. schnelle interne Verarbeitung in maschinennaher Form, Austausch mit anderen Systemen in maschinenferner Form wie JSON).

---

## 6. Überblick über die Themen der Übungsaufgaben

Die zugehörige Übung vertieft die Vorlesungsinhalte anhand von drei Aufgabenblöcken (ohne die konkreten Aufgabenstellungen hier zu wiederholen):

1. **Begrifflichkeiten**: Anwendung der Konzepte Datum/Repräsentation/parallele Programmausführung auf ein konkretes (bewusst unsicheres) C-Codebeispiel, sowie Übertragung der Konzepte auf einen unternehmensweiten Big-Data-Kontext und auf Baumstrukturen.
2. **Formalisierung**: Übung der mathematischen Notation aus Abschnitt 2 – u. a. Funktionsnotation, der Unterschied zwischen geordneten Tupeln und ungeordneten Mengen als zusammengesetzte Daten, sowie die formale Beschreibung von ASCII-Strings und einer C-`struct` als Menge.
3. **Einfache Datenrepräsentation**: praktische Anwendung von Endianness, Zweier-/Einerkomplement-Darstellung negativer Zahlen, Portabilitätsproblemen beim Datenaustausch zwischen Rechnern sowie ein Performance-Vergleich zwischen maschinennaher und maschinenferner Repräsentation (inklusive einer verlustfreien Float-zu-String-Konvertierung in C++).

---

## 7. Wichtigste Begriffe im Schnellüberblick (Glossar)

- **Algorithmus** – endliche Handlungsvorschrift, die aus einer Eingabe eine Ausgabe berechnet
- **Datum / Daten** – bedeutungstragende Information (Semantik)
- **Datenrepräsentation** – konkrete (meist binäre) Darstellung eines Datums
- **Datenformat** – Spezifikation, wie eine Repräsentation aufgebaut ist
- **Rohdaten / abgeleitete Daten** – ursprüngliche vs. errechnete Daten
- **Datenaufbereitung** – Prozess zur Verbesserung/Umwandlung von Daten
- **Datenstruktur** – Vorgabe zur Anordnung von Daten und ihren Beziehungen
- **Verweis** – Bezug zwischen zwei Daten, oft als Adresse/ID realisiert
- **Maschinennahe Repräsentation** – schnell, kompakt, aber schwer portabel
- **Maschinenferne Repräsentation** – portabel, menschenlesbar, aber langsamer und redundanter
- **Endianness** – Reihenfolge, in der Bytes einer Mehrbyte-Zahl interpretiert werden

---

*Diese Übersicht dient als Lernhilfe zur Wiederholung der Kapitel-1-Inhalte und ersetzt nicht das Studium der Original-Folien und der Übungsaufgaben.*

# Algorithmen und Datenstrukturen – Übung 1: Einführung
## Aufgaben mit Lösungen

---

## Aufgabe 1: Begrifflichkeiten

### a) C-Programm mit `gets`

**Frage:** Welche Daten gibt es in dem Programmfragment?

**Lösung:** Es gibt vier konzeptionelle Daten:
- `username` – der eingegebene Benutzername
- `password` – das eingegebene Passwort
- `previous_login_error_count_str` – Anzahl bisheriger Fehlversuche, als Zeichenkette geladen
- `previous_login_error_count` – dieselbe Anzahl, aber als Ganzzahl interpretiert

---

**Frage:** Welche Repräsentation besitzen die Daten?

**Lösung:**
- `username`, `password`, `previous_login_error_count_str` sind jeweils als `char`-Array (also ASCII-Zeichenfolge) repräsentiert.
- `previous_login_error_count` ist als `int` repräsentiert (hardwarenahe Binärdarstellung).

---

**Frage:** Hat ein Datum mehrere Repräsentationen?

**Lösung:** Ja. Die "Fehlversuchsanzahl" existiert als **zwei Repräsentationen desselben konzeptionellen Datums**: einmal als Zeichenkette (`previous_login_error_count_str`, z. B. maschinenfern/menschenlesbar) und einmal als Ganzzahl (`previous_login_error_count`, maschinennah). `atoi` überführt die eine Repräsentation in die andere.

---

**Frage:** Wie wirkt es sich auf Daten und Repräsentationen aus, wenn man das Programm mehrmals parallel startet?

**Lösung:** Jede lokale Variable (`username`, `password`, `previous_login_error_count_str`, `previous_login_error_count`) liegt auf dem **Stack des jeweiligen Prozesses** – jeder parallele Programmstart bekommt also seine eigenen, voneinander unabhängigen Speicherbereiche und damit eigene Repräsentationen dieser Daten. Kritisch ist hingegen der Zugriff auf die **gemeinsam genutzte Datenquelle** hinter `load_login_error_count_from_table` (z. B. eine Datei oder Datenbank): Greifen mehrere parallele Instanzen gleichzeitig lesend/schreibend darauf zu, kann es zu **Race Conditions** (Wettlaufsituationen) und inkonsistenten Zwischenständen kommen, wenn keine Synchronisation erfolgt.

---

**Frage:** Warum ist `gets` eine schlechte Idee?

**Lösung:** `gets` liest eine Zeile von der Standardeingabe ein, **ohne die Länge des Zielpuffers zu prüfen**. Ist die Eingabe länger als der reservierte Puffer (hier 512 Byte), schreibt `gets` trotzdem weiter über die Puffergrenze hinaus – ein klassischer **Pufferüberlauf (Buffer Overflow)**. Das kann benachbarte Speicherbereiche (z. B. andere Variablen oder die Rücksprungadresse auf dem Stack) überschreiben, was zu Programmabstürzen oder – gezielt ausgenutzt – zu Sicherheitslücken (Code-Injection) führen kann. Aus diesem Grund wurde `gets` aus dem C-Standard entfernt; sichere Alternativen sind z. B. `fgets` mit expliziter Längenangabe.

---

### b) Big-Data-Szenario über mehrere Standorte

**Frage:** Warum ist es wichtig, sich auf die Repräsentation der Daten zu einigen?

**Lösung:** Wenn verschiedene Standorte unterschiedliche Datenrepräsentationen verwenden (z. B. unterschiedliche Zeichenkodierungen, Zahlenformate oder Byte-Reihenfolgen), können dieselben Rohdaten an anderer Stelle **falsch interpretiert** werden, obwohl die Bits technisch korrekt übertragen wurden. Eine gemeinsame Konvention stellt sicher, dass alle Beteiligten dieselbe Semantik aus denselben Bits ableiten – sie ist die Voraussetzung für **Interoperabilität**.

---

**Frage:** An welcher Stelle muss eine konventionsgemäße Datenrepräsentation mindestens eingehalten werden?

**Lösung:** Mindestens **an den Schnittstellen des Datenaustauschs** (also beim Senden/Empfangen bzw. Import/Export zwischen den Standorten). Intern darf jeder Standort durchaus eine eigene, für ihn optimale Repräsentation nutzen (z. B. maschinennah für schnelle lokale Verarbeitung) – solange beim Übergang zu einem anderen System in das vereinbarte, gemeinsame Format konvertiert wird.

---

**Frage:** Welche Rolle spielt in diesem Fall eine Datenaufbereitung?

**Lösung:** Die Datenaufbereitung übernimmt genau diese Konvertierung: Sie wandelt die (evtl. uneinheitlichen, lückenhaften oder fehlerhaften) Rohdaten der einzelnen Standorte in ein **einheitliches, vereinbartes Format** um, bereinigt Inkonsistenzen und macht die Daten dadurch erst sinnvoll für die unternehmensweite Weiterverarbeitung nutzbar.

---

### c) Baum von Folie 16

**Frage:** Wie sieht der Baum aus, wenn *bratwurst* statt *krautsalat* in der Wurzel stehen soll?

**Lösung:** Der gezeigte Baum ist ein **binärer Suchbaum (BST)** über den Wörtern in alphabetischer Ordnung. Bei einem BST gilt: Im linken Teilbaum eines Knotens stehen ausschließlich Werte, die (hier: alphabetisch) kleiner sind als der Knotenwert, im rechten Teilbaum ausschließlich größere.

Mit *bratwurst* als Wurzel müssten also im linken Teilbaum alle Wörter liegen, die alphabetisch vor *bratwurst* kommen (z. B. *apfel*, *bier*), und im rechten Teilbaum alle, die danach kommen (z. B. *burger*, *cola*, *krautsalat*, *schnitzel*, *tomate*). Die genaue Form (welches Wort wo im jeweiligen Teilbaum steht) hängt zusätzlich von der **Einfügereihenfolge** ab – das führt direkt zur nächsten Frage.

---

**Frage:** Ist über das Wort in der Wurzel eindeutig festgelegt, wie der Baum aussieht?

**Lösung:** **Nein.** Die Wurzel legt lediglich fest, welche Werte in den linken bzw. rechten Teilbaum gehören – nicht aber, wie diese Teilbäume selbst intern aufgebaut sind.

**Gegenbeispiel:** Fügt man bei gleicher Wurzel *bratwurst* die restlichen Wörter in aufsteigender alphabetischer Reihenfolge ein (*apfel, bier, burger, cola, krautsalat, schnitzel, tomate*), entsteht im rechten Teilbaum eine reine, unbalancierte "Kette" (im Grunde eine verkettete Liste) – jeder Knoten hat nur ein rechtes Kind. Fügt man dieselben Wörter dagegen in einer geschickt gewählten Reihenfolge ein (z. B. zuerst den jeweiligen "mittleren" verbleibenden Wert), entsteht ein deutlich flacherer, balancierter Baum. Beide Bäume haben *bratwurst* in der Wurzel, sehen aber vollkommen unterschiedlich aus.

---

**Frage:** Welche Bedingung müssen die Daten erfüllen, damit alle Äste gleich lang sind?

**Lösung:** Alle Wege von der Wurzel bis zu den Blättern sind genau dann gleich lang, wenn der Baum ein **vollständiger (perfekt balancierter) Binärbaum** ist, d. h. jede Ebene des Baums bis auf die letzte ist vollständig mit Knoten besetzt, und alle Blätter befinden sich auf derselben Tiefe. Das erfordert insbesondere, dass die Gesamtanzahl der Knoten die Form \(2^h - 1\) (für eine Höhe \(h\)) hat und die Werte in einer Reihenfolge eingefügt werden, die diese perfekte Balance erzeugt (z. B. durch Einfügen des jeweiligen Medians der verbleibenden Werte).

---

## Aufgabe 2: Formalisierung

### a) Formalisierung eines Lautstärkereglers

**Lösung:** Gesucht ist eine Funktion, die eine Eingabelautstärke auf eine (kleinere) Ausgabelautstärke abbildet. Ohne die konkrete Abbildungsvorschrift zu kennen, reicht die Angabe von Definitions- und Zielmenge sowie ein Funktionsname:

\[ f: [0, V_{max}] \rightarrow [0, V_{max}] \]

wobei \([0, V_{max}] \subset \mathbb{R}_{\ge 0}\) die Menge aller physikalisch sinnvollen Lautstärken (z. B. in Dezibel oder als normierter Wert) bezeichnet. Wichtig an dieser Notation ist, dass sie unabhängig von der konkreten Abbildungsvorschrift bereits klarstellt, welche Werte überhaupt sinnvoll ein- bzw. ausgegeben werden können.

---

### b) Umsetzung am Rechner

**Frage:** Worin besteht das Problem?

**Lösung:** Die mathematische Definitionsmenge \([0, V_{max}] \subset \mathbb{R}\) ist **unendlich** (überabzählbar), da reelle Zahlen beliebig fein abgestuft sind. Ein Rechner kann aber – wie in Abschnitt zur Formalisierung erläutert – nur **endliche** Wertebereiche direkt abbilden (z. B. eine begrenzte Anzahl von Bits). Eine exakte Umsetzung der reellen Funktion ist daher grundsätzlich nicht möglich.

**Frage:** Wie muss die Definition angepasst werden?

**Lösung:** Definitions- und Zielmenge müssen auf **endliche, diskrete Teilmengen** eingeschränkt werden, z. B. auf eine endliche Menge von Lautstärkestufen \(\{0, 1, \dots, 100\}\) oder auf eine Gleitkommazahl mit fester Bitbreite (`float`). Die kontinuierliche Funktion wird damit zu einer diskretisierten Näherung, bei der zwangsläufig Rundungs- bzw. Quantisierungsfehler auftreten.

---

### c) \(z_1 = (x,y)\) vs. \(z_2 = \{x,y\}\)

**Frage:** Worin unterscheiden sich \(z_1\) und \(z_2\)?

**Lösung:** \(z_1\) ist ein **geordnetes Paar (Tupel)**: Die Position (erste/zweite Stelle) ist Teil der Information, \(x\) und \(y\) bleiben eindeutig unterscheidbar und ihrer jeweiligen "Rolle" zuordenbar. \(z_2\) ist eine **ungeordnete Menge**: Es gibt keine Reihenfolge, und – rein mengentheoretisch – auch keine Möglichkeit, ein Element eindeutig als "das erste" oder "das zweite" zu benennen; zudem können in einer Menge keine Duplikate auftreten.

**Frage:** Welche Variante ist im Allgemeinen geschickter?

**Lösung:** In der Praxis meist das **Tupel** \(z_1\), da bei zusammengesetzten Daten in aller Regel klar sein muss, welcher Bestandteil welche Bedeutung hat (hier: welcher Wert ist \(x\), welcher \(y\)) – genau das leistet die geordnete Notation.

**Frage:** Was ist die Basismenge für \(z_1\)?

**Lösung:** \( \mathbb{R} \times \mathbb{N}^+ \)

**Frage (für Profis):** Was ist die Basismenge für \(z_2\)?

**Lösung:** \(z_2\) ist eine ein- oder zweielementige Teilmenge von \(\mathbb{R} \cup \mathbb{N}^+\), formal also ein Element der Potenzmenge dieser Vereinigung, eingeschränkt auf Kardinalität 1 oder 2:

\[ z_2 \in \{ T \subseteq (\mathbb{R} \cup \mathbb{N}^+) \mid 1 \le |T| \le 2 \} \]

(Kardinalität 1 deckt den – hier durch die unterschiedlichen Wertebereiche eigentlich ausgeschlossenen – Sonderfall \(x = y\) ab.)

---

### d) Menge aller terminierten ASCII-Strings

**Lösung:**

- Menge für ein einzelnes ASCII-Zeichen: \( M_1 = \{0, 1, \dots, 127\} \) (die 128 ASCII-Codepunkte).
- Menge aller Strings mit **exakt zwei** Zeichen: \( M_1 \times M_1 = M_1^2 \)
- Menge aller Strings mit **exakt \(n\)** Zeichen (für \(n = 3, 4, 5, \dots\)): \( M_1^n = \underbrace{M_1 \times M_1 \times \dots \times M_1}_{n \text{ mal}} \)
- Menge aller Strings mit **1 bis 4** Zeichen: Vereinigung der Einzelmengen:
\[ M_1^1 \cup M_1^2 \cup M_1^3 \cup M_1^4 \]
- Menge **aller** möglichen (nicht-leeren) ASCII-Strings:
\[ \bigcup_{n=1}^{\infty} M_1^n \]

---

### e) `struct obstacle` als Menge

**Lösung:** Mit \(M_S\) als Menge aller möglichen ASCII-Strings (siehe Teilaufgabe d) und \(\mathbb{Z}\) als Wertebereich für die (vorzeichenbehafteten) Positions-Ganzzahlen ergibt sich die struct als kartesisches Produkt:

\[ \text{Obstacle} = \mathbb{Z} \times \mathbb{Z} \times M_S \]

Ein konkretes Hindernis ist dann ein Tupel \((x, y, s) \in \text{Obstacle}\) mit \(x\) = `x_position`, \(y\) = `y_position` und \(s\) = `name`.

---

## Aufgabe 3: Einfache Datenrepräsentation

### a) Big-Endian vs. Little-Endian am Beispiel `CA FF EE 00`

**Lösung:**

- **Big-Endian:** Das erste Byte trägt den höchsten Stellenwert. Die Bytefolge wird also direkt als `0xCAFFEE00` gelesen, das entspricht dezimal **3.405.770.240**.
- **Little-Endian:** Das letzte Byte trägt den höchsten Stellenwert, die Byte-Reihenfolge wird zur Interpretation umgedreht: `0x00EEFFCA`, das entspricht dezimal **15.663.050**.

Der Unterschied liegt also ausschließlich darin, **welchem Byte welche "Wertigkeit"** (Zehnerpotenz im Binärsystem) zugeordnet wird – die Bits selbst ändern sich nicht, nur ihre Interpretation.

---

### b) `-107` als hexadezimale Bytefolge

**Lösung** (angenommen: 32-Bit-Ganzzahl):

- **Signed int, big-endian, Zweierkomplement:**
`+107` = `0x0000006B`. Zweierkomplement von `-107`: alle Bits invertieren und 1 addieren → `0xFFFFFF95`.
Big-endian (höchstwertiges Byte zuerst): **`FF FF FF 95`**

- **Signed int, little-endian, Einerkomplement:**
Einerkomplement von `-107` = bitweise Invertierung von `+107` (ohne +1) → `0xFFFFFF94`.
Für die little-endian-*Speicherung* wird die Byte-Reihenfolge umgedreht (niedrigstwertiges Byte zuerst): **`94 FF FF FF`**

- **Array mit ASCII-Zeichen** (Zeichenkette `"-107"`):
`'-'` = `0x2D`, `'1'` = `0x31`, `'0'` = `0x30`, `'7'` = `0x37`
→ **`2D 31 30 37`**

---

### c) `fwrite`/`fread` über Netzwerkshare

**Frage:** Warum tritt eventuell ein Problem auf? Was für eine Ausgabe ergibt sich?

**Lösung:** `fwrite`/`fread` schreiben bzw. lesen die **hardwarenahe** (maschinenabhängige) Binärrepräsentation von `int` – inklusive der auf dem jeweiligen Rechner geltenden Byte-Reihenfolge (Endianness) und ggf. Größe des `int`-Typs. Läuft das schreibende Programm auf einer Maschine mit anderer Endianness (oder anderer `int`-Breite) als das lesende Programm, werden die Bytes zwar korrekt übertragen, aber **falsch interpretiert**. `printf("%i", value)` gibt dann einen völlig anderen, meist willkürlich wirkenden Zahlenwert aus als ursprünglich gespeichert (vgl. Rechenbeispiel in a): aus derselben Bytefolge kann ein winziger oder ein riesiger Wert werden, je nach Interpretation).

**Frage:** Wie beheben, wenn man auf hardwarenahe Repräsentation beschränkt ist?

**Lösung:** Eine **feste, vereinbarte Byte-Reihenfolge** (klassischerweise "Network Byte Order" = big-endian) für den Austausch vorschreiben und beim Schreiben/Lesen explizit dorthin bzw. davon konvertieren (in C z. B. mit `htonl`/`ntohl`). Zusätzlich sollten plattformunabhängige, fest breite Typen (z. B. `int32_t` statt `int`) verwendet werden, um Unterschiede in der Typgröße auszuschließen.

**Frage:** Wie beheben, wenn eine beliebige Repräsentation wählbar ist? Vor-/Nachteil?

**Lösung:** Man kann auf eine **maschinenferne Repräsentation** wechseln, z. B. den Wert als ASCII-Text (`"8914049"`) statt als rohe Binärzahl speichern.
*Vorteil:* Die Darstellung ist unabhängig von Endianness und `int`-Breite garantiert korrekt interpretierbar, zusätzlich menschenlesbar/prüfbar.
*Nachteil:* Höherer Speicherbedarf und zusätzlicher Rechenaufwand für die Umwandlung zwischen Text- und Binärform bei jedem Lese-/Schreibvorgang.

---

### d) Performancetest: Konvertierung vs. Rechenoperation

**Lösung (Vorgehen und erwartetes Ergebnis):**

Ein solcher Test lässt sich in C++ etwa wie folgt aufbauen (vereinfachtes Gerüst):

```cpp
#include <vector>
#include <string>
#include <chrono>
#include <cstdlib>
#include <cstdio>

const size_t N = 5'000'000;

int main() {
    std::vector<float> values(N);
    for (auto& v : values) v = static_cast<float>(rand()) / RAND_MAX;

    // Schleife 1: float -> string
    std::vector<std::string> strs(N);
    auto t1 = std::chrono::steady_clock::now();
    for (size_t i = 0; i < N; ++i) {
        char buf[32];
        snprintf(buf, sizeof(buf), "%f", values[i]);
        strs[i] = buf;
    }
    auto t2 = std::chrono::steady_clock::now();

    // Schleife 2: string -> float (zurückschreiben)
    for (size_t i = 0; i < N; ++i) {
        values[i] = std::strtof(strs[i].c_str(), nullptr);
    }
    auto t3 = std::chrono::steady_clock::now();

    // Schleife 3: reine Rechenoperationen
    float acc = 0.f;
    for (size_t i = 0; i + 5 < N; i += 6) {
        acc += values[i] + values[i+1] - values[i+2]
             + values[i+3] - values[i+4] + values[i+5];
    }
    auto t4 = std::chrono::steady_clock::now();

    printf("float->string: %ld ms\n",
        std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count());
    printf("string->float: %ld ms\n",
        std::chrono::duration_cast<std::chrono::milliseconds>(t3 - t2).count());
    printf("nur Rechnen:   %ld ms\n",
        std::chrono::duration_cast<std::chrono::milliseconds>(t4 - t3).count());
    printf("Ergebnis (verhindert Wegoptimierung): %f\n", acc);
    return 0;
}
```

**Erwartetes Ergebnis:** Beide Konvertierungsschleifen (float→String und String→float) sind **um Größenordnungen teurer** als die reine Additions-/Subtraktionsschleife – erfahrungsgemäß etwa **Faktor 10 bis 100**, da bei der Konvertierung aufwendige Algorithmen zur Dezimaldarstellung von Gleitkommazahlen (bzw. deren Parsing) durchlaufen werden, während eine einfache Addition/Subtraktion nur wenige Prozessortakte benötigt.

**Für Profis:** Ein Profiler zeigt in der Regel, dass die Zeit vor allem in der **Umrechnung zwischen Binär- und Dezimalsystem** (Bestimmung der einzelnen Dezimalstellen bzw. deren Rückrechnung, inklusive korrektem Runden) sowie in **Speicherallokationen** für die entstehenden Strings verloren geht – nicht im eigentlichen Kopieren der Daten.

---

### e) Verlustfreie Float-zu-String-Konvertierung (C++)

**Lösung:** Der einfachste, garantiert verlustfreie Weg ist, **nicht** die Dezimaldarstellung zu nutzen, sondern die rohe Bitrepräsentation des `float` (32 Bit) z. B. hexadezimal zu kodieren:

```cpp
#include <cstdint>
#include <cstring>
#include <string>
#include <cstdio>
#include <cstdlib>

std::string to_string(float v) {
    uint32_t bits;
    std::memcpy(&bits, &v, sizeof(bits)); // Bit-Reinterpretation, kein Wertewechsel
    char buf[9];
    snprintf(buf, sizeof(buf), "%08X", bits); // exakt 8 Hex-Zeichen
    return std::string(buf);
}

float to_float(const std::string& s) {
    uint32_t bits = static_cast<uint32_t>(std::strtoul(s.c_str(), nullptr, 16));
    float v;
    std::memcpy(&v, &bits, sizeof(v));
    return v;
}
```

Da `memcpy` die 32 Bit des `float` unverändert in einen `uint32_t` kopiert (und umgekehrt), ist die Hex-Darstellung **exakt bit-identisch** reversibel – unabhängig davon, ob es sich um reguläre Zahlen, `NAN`, `INF` oder Sonderwerte wie `-0.0` handelt. Ein vollständiger Beweis ließe sich führen, indem man alle \(2^{32}\) möglichen Bitmuster durchläuft und `to_float(to_string(v)) == v` (bzw. Bit-Gleichheit über `memcmp`, da `NAN != NAN` bei normalem `==`-Vergleich gilt) prüft.

---

### f) Für Profis: Menschenlesbare, verlustfreie Darstellung

**Lösung (Ansatzskizze):** Statt der Hex-Bitdarstellung nutzt man eine **dezimale Darstellung mit ausreichend vielen signifikanten Stellen**, die eine korrekte Rundtrip-Konvertierung garantiert (für `float` genügen nachweislich 9 signifikante Dezimalstellen). In modernem C++ bietet sich `std::to_chars`/`std::from_chars` (seit C++17, Header `<charconv>`) an, da diese Funktionen speziell für **exakte, verlustfreie Rundtrip-Konvertierung** von Gleitkommazahlen spezifiziert sind:

```cpp
#include <charconv>
#include <string>
#include <cmath>

std::string to_string_readable(float v) {
    if (std::isnan(v)) return "NAN";
    if (std::isinf(v)) return v > 0 ? "INF" : "-INF";
    char buf[32];
    auto res = std::to_chars(buf, buf + sizeof(buf), v);
    return std::string(buf, res.ptr);
}

float to_float_readable(const std::string& s) {
    if (s == "NAN") return NAN;
    if (s == "INF") return INFINITY;
    if (s == "-INF") return -INFINITY;
    float v;
    std::from_chars(s.data(), s.data() + s.size(), v);
    return v;
}
```

Sonderwerte (`NAN`, `INF`, `-INF`) werden dabei bewusst als fester Text abgefangen, da sie sich nicht sinnvoll als "Kommazahl" darstellen lassen.