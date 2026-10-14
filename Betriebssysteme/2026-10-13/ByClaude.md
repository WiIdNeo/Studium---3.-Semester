# Lösungen: Betriebssysteme, 4 – Dateiverwaltung

## Aufgabe 1: Dateien und Verzeichnisse

### a) Die vier großen Probleme der Speicherverwaltung

Die vier Probleme stammen aus der Speicherverwaltung (VL-Einheit 3). In den hochgeladenen Folien stehen sie nicht. Ich gehe von dieser klassischen Liste aus: **Relokation, Schutz, Fragmentierung, Platzmangel**. Falls in eurer Vorlesung eine Variante vorkommt (z. B. "gemeinsame Nutzung" statt eines der Punkte), bitte kurz abgleichen.

Alle vier treten bei der Dateiverwaltung ebenfalls auf:

| Problem | Bedeutung im Hauptspeicher | Bei Dateien |
|---|---|---|
| **Relokation** | Programme dürfen nicht an feste physische Adressen gebunden sein. | Dateien werden über Namen und Pfade angesprochen. Ob und wo auf dem Datenträger die Blöcke liegen, ist versteckt (FAT, I-Node). Dadurch kann das OS Blöcke verschieben und Dateien umbenennen, ohne dass Programme etwas merken. |
| **Schutz** | Prozesse dürfen nicht im Speicher anderer Prozesse lesen oder schreiben. | Dateien gehören verschiedenen Benutzern. Zugriffsrechte (rwx für u/g/o, ACLs) und Attribute wie Read-Only oder Passwort regeln den Zugriff. |
| **Fragmentierung** | Freier Speicher zerfällt in viele kleine, unbrauchbare Stücke (extern) oder Blöcke sind nur teilweise gefüllt (intern). | **Extern:** bei kontinuierlicher Allokation entstehen Lücken nach dem Löschen (Folie 28). **Intern:** eine 64-Byte-Datei belegt trotzdem einen ganzen Block. |
| **Platzmangel** | Der Speicher ist kleiner als der Bedarf. | Der Datenträger ist endlich. Gegenmaßnahmen sind Quotas, Komprimierung, Archivierung auf Band oder Cloud. Anders als im RAM gibt es keine "nächste Ebene" zum Auslagern. |

### b) Beispiel für nicht eindeutige relative Dateinamen

Ein relativer Pfad wird immer gegen das **Arbeitsverzeichnis** aufgelöst, und das ist pro Prozess verschieden. Dasselbe gilt schon für den nackten Dateinamen `notes.txt`, der in sehr vielen Verzeichnissen existiert.

`images\cat.jpg` bedeutet je nach Arbeitsverzeichnis etwas anderes:
- Arbeitsverzeichnis `C:\Programme\Photoshop` ergibt `C:\Programme\Photoshop\images\cat.jpg`.
- Arbeitsverzeichnis `C:\Users\Werner\Desktop` ergibt `C:\Users\Werner\Desktop\images\cat.jpg`.

Das sind zwei verschiedene Dateien. Eindeutig ist nur der absolute (und kanonische) Pfad.

### c) Dateiendung als "Konvention"

**Zusammenhang:** Die Konvention liegt nicht im Dateisystem, sondern in Programmen. Beim Doppelklick liest die Shell (z. B. der Explorer) die Endung und schlägt sie in einer Zuordnungstabelle nach (Endung → Standardprogramm). Dann startet sie das Programm mit der Datei als Argument. Das OS "weiß" also nichts über den Inhalt, es arbeitet nur eine Tabelle ab. Das funktioniert, solange Nutzer und Programme die Konvention einhalten.

**Wenn man sich nicht daran hält:**
- Die Datei lässt sich nicht öffnen oder das falsche Programm startet. Das Programm meldet "Format ungültig" oder zeigt Datenmüll.
- Der Inhalt bleibt unverändert. Wer `foto.jpg` in `foto.txt` umbenennt, ändert nichts an den Bytes, und die Rückbenennung stellt alles wieder her.
- Manche Programme erkennen das Format trotzdem am Inhalt, z. B. über **Magic Numbers** (JPEG beginnt mit `FF D8`, PDF mit `%PDF`). Unter Linux macht das der Befehl `file`.

**Seitenthema Sicherheit:** Der Explorer blendet bekannte Endungen oft aus. Eine Datei `rechnung.pdf.exe` erscheint dann als `rechnung.pdf`, ein klassischer Phishing-Trick. Unter Linux entscheidet übrigens nicht die Endung, sondern das **x-Bit**, ob etwas ausführbar ist.

### d) Kurzfragen

- **.docx: Text oder Binär?** **Binärdatei.** Eine .docx-Datei ist ein ZIP-Archiv, das mehrere XML-Dateien enthält. Das Archiv ist komprimiert und besteht aus beliebigen Bytes, ist also nicht menschenlesbar. Die XML-Dateien darin sind zwar Text, aber der Container ist binär.
- **Wo ist gespeichert, ob Text oder Binär?** In heutigen Dateisystemen **nirgends verbindlich**. Die Folie nennt zwar ein ASCII/Binary-Flag als mögliches Attribut, aber in der Praxis ergibt sich die Einordnung erst aus der Interpretation durch das Programm, ggf. gestützt durch Endung oder Magic Number. Die Aufteilung ist, wie die Folie sagt, "schwammig".
- **Ist jede Textdatei auch eine Binärdatei?** **Ja.** Jede Datei ist physisch eine Folge von Bytes. Eine Textdatei ist der Spezialfall, bei dem diese Bytes nach einer Zeichentabelle (ASCII, UTF-8) als Zeichen gelesen werden.
- **Ist jede Binärdatei auch eine Textdatei?** **Nein.** Beliebige Bytefolgen (z. B. `0x00`, ungültige UTF-8-Sequenzen) ergeben in einer Zeichentabelle keinen sinnvollen Text. Man kann zwar jede Bytefolge formal irgendwie als Zeichen darstellen (z. B. Latin-1), aber das wäre kein lesbarer Inhalt.

### e) Beispiele für Gerätedateien (Linux)

- **Zeichenorientiert:** `/dev/tty` bzw. `/dev/ttyS0` (Terminal bzw. serielle Schnittstelle).
  Daten fließen Byte für Byte. Was ein Programm hineinschreibt, erscheint am Terminal. Tastatureingaben liest man byteweise heraus. Es gibt kein Zurückspringen (kein sinnvolles `seek`).
- **Blockorientiert:** `/dev/sda` (ganze Festplatte) oder `/dev/sda1` (Partition).
  Der Zugriff erfolgt blockweise (z. B. 512 B oder 4 KB) mit wahlfreiem Zugriff. Das Lesen von `/dev/sda` liefert die rohen Bytes des Datenträgers. So arbeitet auch `dd if=/dev/sda ...`. Das Dateisystem selbst setzt auf dieser Ebene auf.
- **Pseudo-Gerät:** `/dev/urandom` liefert beliebig viele Zufallsbytes, die der Kernel algorithmisch erzeugt. Dahinter steckt keine Hardware und es gibt kein Dateiende. Weitere Beispiele sind `/dev/zero` (endlos Nullbytes) und `/dev/null` (verschluckt alles, liefert beim Lesen sofort EOF).
- Windows kennt Ähnliches, z. B. `CON`, `NUL` und `\\.\PhysicalDrive0`.

### f) Hard Link oder Sym-Link mit nur `delete()` und `read()`

**Vorgehen:** Lösche die **Originaldatei** über ihren Namen (`delete(original)`), dann lies über die Verknüpfung (`read(link)`).

- **`read()` liefert weiter den bekannten Inhalt → Hard Link.**
  Beim Hard Link zeigen zwei Verzeichniseinträge auf dieselben Daten und Metadaten. `delete()` entfernt nur einen Eintrag und senkt den Referenzzähler. Die Daten werden erst bei Zähler 0 freigegeben.
- **`read()` schlägt fehl (Datei nicht gefunden) → Sym-Link.**
  Der Sym-Link enthält nur den *Pfad* zum Ziel. Das Ziel existiert nicht mehr, also läuft der Link ins Leere (*dangling link*).

**Slow oder fast Sym-Link:** Das lässt sich mit diesen beiden Aufrufen **nicht** unterscheiden. Der Unterschied liegt nur darin, *wo* das Dateisystem den Zielpfad ablegt (extra Datenblock oder direkt in den Metadaten). Das ist ein Implementierungsdetail, das für Programme transparent ist. In beiden Fällen schlägt `read()` nach dem Löschen des Ziels fehl. Unterscheiden könnte man nur über Nebenwirkungen wie Zugriffszeit (ein Block mehr lesen) oder über eine Längenbegrenzung des Zielpfads bei fast Sym-Links.

### g) Algorithmus: relativer Pfad → absoluter, kanonischer Pfad

Idee: Man zerlegt den Pfad in Komponenten und baut den Ergebnispfad mit einem **Stack** auf. `.` und leere Komponenten werden ignoriert, `..` entfernt das oberste Element, alles andere wird hinzugefügt.

```python
def kanonisch(arbeitsverz, rel_pfad, sep="\\"):
    # Wurzel (Laufwerk wie "C:" bzw. "" bei Linux) vom Rest trennen
    teile = arbeitsverz.split(sep)
    wurzel = teile[0]
    stack = [t for t in teile[1:] if t != ""]

    for komp in rel_pfad.split(sep):
        if komp == "" or komp == ".":
            continue                    # nichts zu tun
        elif komp == "..":
            if stack:                   # an der Wurzel bleibt ".." wirkungslos
                stack.pop()
        else:
            stack.append(komp)

    return wurzel + sep + sep.join(stack)

# Beispiel
print(kanonisch(r"C:\Users\Werner\Desktop",
                r"..\..\test\hallo\..\ordner\.\hier.txt"))
# -> C:\Users\test\ordner\hier.txt
```

Der Ablauf im Beispiel: Der Stack startet mit `Users, Werner, Desktop`. Die zwei `..` entfernen `Desktop` und `Werner`. Dann kommen `test` und `hallo` dazu, das `..` entfernt `hallo`, es folgen `ordner` und `hier.txt`. Das Ergebnis ist `C:\Users\test\ordner\hier.txt`.

Für Linux ruft man `kanonisch("/home/user", "../x/./y", "/")` auf. Dann ist `wurzel = ""` und das Ergebnis lautet `/home/x/y`.

**Einschränkungen (Seitenthema):**
- Die Lösung arbeitet rein **textuell (lexikalisch)**. Gibt es Sym-Links, kann `link\..` etwas anderes bedeuten als "das Verzeichnis oberhalb von `link`". Echte kanonische Pfade (`realpath`) lösen Links deshalb zusätzlich auf.
- Die Aufgabe setzt voraus, dass die Datei existiert. Bei `dog\.\..\` auf einem nicht vorhandenen `dog` würde das OS einen Fehler melden, der Algorithmus nicht.

---

## Aufgabe 2: Dateien und Verzeichnisse

### a) Dateistrukturen vs. Allokationsverfahren

- **Dateistrukturen** (Folie 12/13: byte-sequentiell, block-sequentiell, hierarchisch) beschreiben die **logische Sicht**. Sie legen fest, *wie ein Programm auf den Inhalt zugreift*, nämlich als Bytefolge, als Blockfolge oder als Baum.
- **Allokationsverfahren** (Folie 28 ff.: kontinuierlich, verkettete Liste, FAT, I-Nodes) beschreiben die **physische Sicht**. Sie legen fest, *wo und wie die Blöcke einer Datei auf dem Datenträger liegen* und wie das OS sie wiederfindet.

Beides ist weitgehend unabhängig voneinander. So bietet das OS heute byte-sequentielle Systemaufrufe, obwohl die Hardware blockweise arbeitet, und dahinter kann beliebig allokiert sein.

### b) Warum nicht auch für den Arbeitsspeicher?

Der Grund sind die **Zugriffszeiten**. Grobe Größenordnungen:

| Operation | Dauer |
|---|---|
| Rechnung in einem Register | unter 1 ns |
| Zeiger in einer Tabelle im RAM verfolgen | etwa 100 ns |
| Daten von SSD/HDD in den RAM lesen | etwa 100 µs (SSD) bis 10 ms (HDD) |

Bei Dateien wird jeder Zugriff ohnehin durch den langsamen Datenträger dominiert (Faktor 10³ bis 10⁷ gegenüber dem RAM). Ein zusätzlicher Zeigersprung in der RAM-Tabelle fällt daneben kaum ins Gewicht.

Im Arbeitsspeicher wäre das anders. Fast jeder Befehl greift auf den Speicher zu. Müsste dafür jedes Mal eine Tabelle oder Zeigerkette durchlaufen werden, würde das System um ein Vielfaches langsamer. Dazu kommt:
- Eine verkettete Liste hat Zugriffszeit O(n). Der RAM braucht dagegen wahlfreien Zugriff in konstanter Zeit.
- Eine FAT mit einem Eintrag pro Speicherzelle bzw. kleinem Block wäre riesig.

Deshalb nutzt das RAM **Adressrechnung** in Hardware (Basis + Offset, Seitentabellen mit MMU und TLB). Das ist ein mehrstufiger Aufbau, der den I-Nodes mit indirekten Blöcken ähnelt, aber hardwarebeschleunigt und gecacht ist.

### c) Blöcke à 1 MB, 5 TB Datenträger, FAT-Eintrag 10 Byte

Ich rechne mit Zweierpotenzen (1 MB = 2²⁰ B, 1 TB = 2⁴⁰ B). Mit Zehnerpotenzen kommt fast dasselbe heraus.

- **Platz einer 50-kB-Textdatei:** Die kleinste Zuteilungseinheit ist ein Block, also belegt die Datei **1 MB**. Von den 1 MB bleiben ca. 950 kB ungenutzt (**interne Fragmentierung**).
- **Größe der gesamten FAT:**
  Anzahl Blöcke = 5 TB / 1 MB = 5 · 2²⁰ = 5 242 880 (dezimal: 5 · 10⁶).
  FAT-Größe = 5 242 880 · 10 B ≈ **52,4 MB**, also ca. 50 MiB (dezimal: 50 MB).
- **Wo liegt die FAT?** **Beides:** Die dauerhafte Fassung liegt auf dem Datenträger (sonst wäre sie nach dem Ausschalten weg). Vor dem Dateizugriff wird sie in den Hauptspeicher geladen (Folie 30). Mit ca. 50 MB ist das heute unproblematisch. Beim Beispiel auf der Folie (8 TB, 16 KB Blöcke) wären es dagegen etwa 2,5 GB.
- **Platzbedarf mit I-Nodes:** Die große Tabelle entfällt. Dafür gibt es pro Datei einen I-Node fester Größe (plus ggf. indirekte Blöcke bei großen Dateien). Der Bedarf hängt dann von der **Anzahl und Größe der Dateien** ab statt von der Datenträgergröße. Im Hauptspeicher müssen nur die I-Nodes **geöffneter** Dateien liegen, also deutlich weniger. Die 50-kB-Datei braucht weiterhin 1 Block, zusätzlich einen I-Node. Bei sehr vielen winzigen Dateien kann die Summe der I-Nodes die FAT sogar übersteigen.

### d) Vorteile von NTFS gegenüber FAT

Der wichtigste Vorteil ist die **Verwaltung über "Läufe"** (Extents). Ein MFT-Eintrag speichert Paare aus Startblock und Länge (z. B. "Blöcke 20–23, 64–65, 80–82"). Eine FAT braucht dagegen einen Eintrag pro Block. Das spart Platz und beschleunigt den Zugriff bei wenig fragmentierten Dateien. Außerdem muss nicht eine riesige globale Tabelle im RAM liegen.

Weitere Vorteile laut Folien und Tabelle:
- 64-Bit-Adressen und damit sehr große Partitionen und Dateien
- Zugriffsrechte pro Datei (ACLs), FAT kennt kaum Schutz
- **Journaling** und damit Robustheit gegen Abstürze
- lange Unicode-Namen und mehrere Datenströme pro Datei

### e) FAT-Eintrag in Pseudocode

**Speicherplatz auf dem Datenträger:**
Die FAT hat 65 536 Einträge. Jeder Eintrag verwaltet einen Block von 1 kB:
65 536 · 1024 B = 2¹⁶ · 2¹⁰ B = 2²⁶ B = **64 MiB**.

Die FAT selbst belegt zusätzlich Platz. Bei 4-Byte-INTs hat ein Eintrag 4 + 16 + 4 + 4 + 4 = 32 B, die Tabelle also 2 MiB. Ob die FAT zu den 64 MiB zählt, ist eine Definitionsfrage.

**Programm zur Ausgabe aller Block-Startadressen:**
Die Struktur enthält kein explizites "next"-Feld. Ich nehme an, wie in Folie 30: Der Index in `fat` entspricht der Block-ID, und `file_block_address` im Eintrag ist die **Adresse des Folgeblocks**. Das Ende der Kette markiere ich mit `-1`. Ein Flag in `flags` wäre eine gleichwertige Alternative. Die Annahme sollte man in der Abgabe benennen.

```python
BLOCK_SIZE = 1024
ENDE = -1                      # Annahme: Markierung für "letzter Block"

def gib_blockadressen_aus(fat, erster_index):
    i = erster_index
    schritte = 0
    while i != ENDE and schritte < len(fat):   # Schutz gegen Zyklen
        print(i * BLOCK_SIZE)                  # Startadresse des aktuellen Blocks
        naechste_adr = fat[i].file_block_address
        if naechste_adr == ENDE:
            break
        i = naechste_adr // BLOCK_SIZE         # Adresse -> Block-ID
        schritte += 1
```

Das Programm folgt der Kette Block für Block. Dabei ist nur die FAT im Hauptspeicher nötig, es müssen keine Datenblöcke gelesen werden. Das ist genau der Vorteil gegenüber der Liste mit Zeigern in den Blöcken.

### f) I-Node-Eintrag in Pseudocode

**Programm zur Ausgabe aller Block-Startadressen:**
Ein I-Node enthält 8 direkte Adressen und je 16 Referenzen auf weitere I-Nodes mit 1-, 2- und 3-facher Indirektion. Ein referenzierter I-Node hat denselben Aufbau, also reicht eine **rekursive Funktion**. Die Tiefe ergibt sich von selbst daraus, welche Felder des referenzierten I-Nodes belegt sind.

```python
def gib_blockadressen_aus(node):
    # 1. direkte Blöcke
    for adr in node.file_block_addresses:
        if adr != 0:                       # 0 = kein Block verknüpft
            print(adr)

    # 2. indirekte Knoten, in Dateireihenfolge: 1-, 2-, 3-stufig
    for ref in (node.one_indirection
                + node.two_indirections
                + node.three_indirections):
        if ref is not None:                # Referenz vorhanden?
            gib_blockadressen_aus(ref)     # gleiche Struktur, rekursiv
```

Die Reihenfolge direkt → einfach → zweifach → dreifach entspricht der Reihenfolge der Dateiblöcke, wie bei ext2 (Folie 38).

**Vorteil der festen 1-/2-/3-stufigen Aufteilung statt eines Baums beliebiger Tiefe:**
- **Begrenzte Zugriffszeit:** Es sind maximal 3 zusätzliche Lesezugriffe auf Indexblöcke nötig. Bei beliebiger Tiefe wäre die Zahl der Zugriffe unbeschränkt (im Extremfall wie eine verkettete Liste).
- **Optimiert für die Praxis** (Folie 31): Es gibt viele kleine und wenige große Dateien. Kleine Dateien kommen mit den direkten Adressen aus, ohne Indirektion und ohne zusätzliche Zugriffe. Nur große Dateien zahlen für die Indirektion.
- **Feste Struktur:** Der I-Node hat eine feste Größe. Die Algorithmen sind einfacher und weniger fehleranfällig (kein Balancieren und kein unbegrenztes Wachsen des Baums). Auch Konsistenzprüfungen sind einfacher.

Der Preis ist eine **begrenzte Maximaldateigröße**, die durch die Zahl der Referenzen und Stufen festgelegt ist.