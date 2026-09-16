# Rechnernetze – Ausführliche Erklärung der offenen Themen

Diese Zusammenfassung erklärt die Themen aus deiner Vorlesung, die noch unklar waren: Fourier-Reihen und Signalspektren, das OSI-Modell, Durchlassbandübertragung, QAM und Gray-Code, Multiplexing-Verfahren sowie physikalische Übertragungsmedien (Kupfer & Glasfaser).

> **Hinweis zu „Seite 57 bis 61“:** Ich habe leider keinen Zugriff auf eure konkreten Vorlesungsfolien und weiß daher nicht, was dort genau behandelt wird. Wenn du mir sagst, welches Thema dort steht (oder die Folien/das PDF hier hochlädst), erkläre ich dir den Inhalt gezielt dazu.

---

## 1. Fourier-Reihe des Rechtecksignals (reelle Darstellung, ohne komplexe Zahlen)

### 1.1 Grundidee

Die Fourier-Reihe besagt: **Jedes periodische Signal** lässt sich als Summe von (unendlich vielen) Sinus- und Kosinusschwingungen unterschiedlicher Frequenz, Amplitude und Phase darstellen. Diese Schwingungen sind ganzzahlige Vielfache einer **Grundfrequenz** $f_0 = 1/T$ (T = Periodendauer des Signals). Man nennt sie **Harmonische** oder **Oberwellen**.

Die reelle (nicht-komplexe) Form der Fourier-Reihe lautet:

$$s(t) = a_0 + \sum_{n=1}^{\infty} \Big[ a_n \cos(n\,\omega_0 t) + b_n \sin(n\,\omega_0 t) \Big]$$

mit $\omega_0 = 2\pi f_0 = \dfrac{2\pi}{T}$.

Die Koeffizienten berechnet man durch Integration über eine Periode:

$$a_0 = \frac{1}{T}\int_0^{T} s(t)\,dt \quad \text{(Gleichanteil / Mittelwert)}$$

$$a_n = \frac{2}{T}\int_0^{T} s(t)\cos(n\omega_0 t)\,dt$$

$$b_n = \frac{2}{T}\int_0^{T} s(t)\sin(n\omega_0 t)\,dt$$

Das ist der Trick "ohne komplexe Zahlen": Statt mit $e^{jn\omega_0 t}$ zu rechnen (komplexe Form), zerlegt man das Signal direkt in reine Kosinus- und Sinus-Anteile. Beide Formen beschreiben dasselbe, die reelle Form ist nur anschaulicher für Anfänger.

### 1.2 Anwendung auf ein Rechtecksignal

Nimm ein symmetrisches Rechtecksignal, das zwischen $-A$ und $+A$ hin- und herspringt (Tastverhältnis 50 %, Periode $T$). Wegen der Symmetrie des Signals verschwinden alle $a_n$ (es ist eine **ungerade Funktion**), und es bleiben nur Sinus-Terme mit **ungeradem** $n$ übrig:

$$s(t) = \frac{4A}{\pi}\sum_{n=1,3,5,\dots}^{\infty} \frac{1}{n}\sin(n\,\omega_0 t)$$

Ausgeschrieben für die ersten Terme:

$$s(t) \approx \frac{4A}{\pi}\left[\sin(\omega_0 t) + \frac{1}{3}\sin(3\omega_0 t) + \frac{1}{5}\sin(5\omega_0 t) + \frac{1}{7}\sin(7\omega_0 t) + \dots\right]$$

**Wichtige Beobachtungen:**
- Nur **ungerade Vielfache** der Grundfrequenz kommen vor (1., 3., 5., 7. Harmonische …), die geraden Harmonischen fehlen komplett.
- Die Amplitude der n-ten Harmonischen fällt mit $1/n$ ab – hohe Frequenzen tragen also immer weniger zum Signal bei, sind aber nötig, um die "scharfen Kanten" des Rechtecks nachzubilden.
- Je mehr Terme man addiert, desto besser nähert sich die Summe dem echten Rechtecksignal an. Mit unendlich vielen Termen wäre die Näherung exakt (an den Sprungstellen bleibt aber immer ein kleines Überschwingen – das sogenannte **Gibbs-Phänomen**).

*Viele Lehrbücher (u. a. Tanenbaum) verwenden statt eines symmetrischen Signals ein Rechtecksignal zwischen 0 und $A$ (z. B. zur Darstellung von Bitmustern). Dann kommt zusätzlich ein Gleichanteil $A/2$ dazu:*

$$g(t) = \frac{A}{2} + \frac{2A}{\pi}\sum_{n=1,3,5,\dots}^{\infty} \frac{1}{n}\sin(n\,\omega_0 t)$$

**Warum ist das für Rechnernetze relevant?** Digitale Signale (Bitfolgen wie 0-1-0-1) sind im Prinzip Rechtecksignale. Um sie unverzerrt zu übertragen, bräuchte man theoretisch unendlich viele Harmonische, also unendliche Bandbreite. Reale Übertragungskanäle (Kupferkabel, Funk) haben aber eine begrenzte Bandbreite – deshalb werden hohe Harmonische abgeschnitten, das Signal "verschleift" und wird runder. Das ist die Grundlage dafür, warum die Kanalbandbreite die maximale Datenrate begrenzt (siehe Nyquist/Shannon).

---

## 2. Spektralanalyse der Fourier-Reihe

Die **Spektralanalyse** ist der Übergang von der **Zeitbereichs-Darstellung** (Signal als Funktion der Zeit, $s(t)$) zur **Frequenzbereichs-Darstellung** (welche Frequenzanteile mit welcher Stärke im Signal enthalten sind).

Die Fourier-Reihe liefert dafür genau die nötigen Zahlen: Jede Harmonische $n$ hat eine Frequenz $n f_0$ und eine zugehörige Amplitude/Phase (berechnet aus $a_n$ und $b_n$). Trägt man diese Werte über der Frequenz auf, erhält man das **Spektrum** des Signals.

Ein zeitlich periodisches Signal hat immer ein **diskretes (Linien-)Spektrum**: Es gibt nur Energie bei den Frequenzen $0, f_0, 2f_0, 3f_0, \dots$ – nicht dazwischen. Deshalb sieht ein Spektrum einer Fourier-Reihe wie eine Reihe einzelner senkrechter "Linien" aus, nicht wie eine durchgehende Kurve (das wäre bei nicht-periodischen Signalen mit der Fourier-**Transformation** der Fall, das ist aber ein anderes Thema).

---

## 3. Amplitudenspektrum und Phasenspektrum

Jede Harmonische lässt sich statt durch $(a_n, b_n)$ auch durch eine **Amplitude** $c_n$ und eine **Phase** $\varphi_n$ beschreiben – das sind einfach zwei unterschiedliche Arten, dieselbe Information darzustellen:

$$a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) = c_n \cos(n\omega_0 t - \varphi_n)$$

mit

$$c_n = \sqrt{a_n^2 + b_n^2} \qquad \text{und} \qquad \varphi_n = \arctan\!\left(\frac{b_n}{a_n}\right)$$

### 3.1 Amplitudenspektrum

Das **Amplitudenspektrum** ist die Auftragung von $c_n$ über der Frequenz $n f_0$. Es zeigt, **wie stark** jede Harmonische im Signal vertreten ist – also die "Lautstärke" jeder Frequenzkomponente.

Für unser symmetrisches Rechtecksignal von oben gilt (nur ungerade $n$):

$$c_n = \frac{4A}{\pi n}$$

Das Amplitudenspektrum besteht also aus Linien bei $f_0, 3f_0, 5f_0, 7f_0,\dots$, deren Höhe mit $1/n$ abnimmt. Bei geraden $n$ ist die Amplitude 0 (keine Linie).

### 3.2 Phasenspektrum

Das **Phasenspektrum** ist die Auftragung von $\varphi_n$ über der Frequenz. Es zeigt, **wie weit jede Harmonische zeitlich verschoben** ist (in Radiant oder Grad).

Da unser Rechtecksignal-Beispiel eine reine Sinus-Reihe ist ($a_n = 0$), gilt $\sin(x) = \cos(x - 90°)$, also ist bei jeder vorhandenen Harmonischen $\varphi_n = 90°$ (bzw. $\pi/2$) konstant. Bei den fehlenden (geraden) Harmonischen ist die Phase nicht definiert, da dort keine Amplitude existiert.

> **Merke:** Amplituden- **und** Phasenspektrum zusammen enthalten exakt dieselbe Information wie die Zeitfunktion $s(t)$ selbst – nichts geht verloren, es ist nur eine andere Darstellungsform (genau wie $a_n,b_n$ vs. $c_n,\varphi_n$ zwei Darstellungen desselben sind).

---

## 4. OSI-Modell – Zuordnung der Geräte zu den Schichten

Das OSI-Modell hat 7 Schichten. Netzwerkgeräte arbeiten auf unterschiedlichen Schichten, je nachdem, welche Informationen sie zur Weiterleitung eines Signals/Pakets auswerten:

| Schicht | Name (deutsch) | Aufgabe | Typische Geräte |
|---|---|---|---|
| 7 | Anwendungsschicht (Application) | Anwendungsdienste (HTTP, FTP, DNS …) | Gateway (Protokollumsetzung), Proxy |
| 6 | Darstellungsschicht (Presentation) | Datenformat, Verschlüsselung, Kompression | (meist Software, kaum eigene Geräte) |
| 5 | Sitzungsschicht (Session) | Verbindungsauf-/-abbau, Sitzungsverwaltung | (meist Software) |
| 4 | Transportschicht (Transport) | Ende-zu-Ende-Übertragung (TCP/UDP) | Firewall (teils), Gateway |
| 3 | Vermittlungsschicht (Network) | Routing zwischen Netzen, IP-Adressierung | **Router**, Layer-3-Switch |
| 2 | Sicherungsschicht (Data Link) | Fehlererkennung, MAC-Adressierung | **Switch**, Bridge, WLAN-Access-Point |
| 1 | Bitübertragungsschicht (Physical) | Übertragung roher Bits als Signale | **Hub**, Repeater, Kabel, Stecker |

**Merkregel:**
- **Hub / Repeater** → Schicht 1: kennt nur elektrische Signale, verstärkt/verteilt sie, versteht keine Adressen.
- **Switch / Bridge** → Schicht 2: liest MAC-Adressen und leitet Frames gezielt nur an den richtigen Port weiter.
- **Router** → Schicht 3: liest IP-Adressen und verbindet unterschiedliche Netzwerke/Subnetze miteinander.
- **Gateway** → kann auf jeder Schicht bis hoch zur Anwendungsschicht arbeiten, meist zur Protokollumsetzung zwischen völlig unterschiedlichen Systemen (z. B. E-Mail-Gateway zwischen zwei Mail-Systemen).

Faustregel: Je höher die Schicht, desto "intelligenter" (aber auch langsamer/komplexer) ist das Gerät, weil es mehr Informationen im Paket auswerten muss.

---

## 5. Durchlassbandübertragung

Man unterscheidet zwei grundsätzliche Arten, ein digitales Signal auf eine Leitung zu bringen:

### 5.1 Basisbandübertragung (Baseband)
Das digitale Signal (z. B. Rechtecksignal aus 0/1-Bits) wird **direkt**, ohne Modulation, auf das Medium gegeben. Das Spektrum des Signals liegt dabei um 0 Hz herum (siehe Fourier-Reihe oben – die Grundschwingung und ihre Harmonischen beginnen bei niedrigen Frequenzen). Beispiel: klassisches Ethernet über Kupferkabel.

### 5.2 Durchlassbandübertragung (Passband / Bandpass-Übertragung)
Hier wird das Signal **auf eine Trägerfrequenz** $f_c$ **aufmoduliert**, sodass sein Spektrum in einen bestimmten Frequenzbereich (das „Durchlassband" des Kanals) verschoben wird – statt bei 0 Hz liegt es dann z. B. um 1000 MHz herum.

**Warum braucht man das?**
- Manche Kanäle können niedrige Frequenzen (nahe 0 Hz) gar nicht übertragen (z. B. Telefonleitungen, Funkstrecken, die nur ein bestimmtes Frequenzband „durchlassen" – daher der Name).
- Mehrere Signale können durch Verschiebung auf unterschiedliche Trägerfrequenzen **gleichzeitig** über dasselbe Medium übertragen werden (→ Frequenzmultiplex, siehe unten).
- Funkübertragung (WLAN, Mobilfunk) funktioniert grundsätzlich nur mit einem Träger, da elektromagnetische Wellen bei sehr niedrigen Frequenzen unpraktikabel große Antennen bräuchten.

Die Modulation erfolgt durch Verändern von **Amplitude**, **Frequenz** oder **Phase** der Trägerschwingung im Takt der zu übertragenden Bits (ASK, FSK, PSK) – oder einer Kombination davon, wie bei **QAM** (siehe Punkt 7).

---

## 6. Konstellationsdiagramm

Ein **Konstellationsdiagramm** stellt die möglichen Sendezustände (Symbole) eines modulierten Signals in einer 2D-Ebene dar:

- Die **x-Achse** zeigt die **In-Phase-Komponente (I)** – das ist der Anteil des Signals, der mit einem Kosinus-Träger moduliert wird.
- Die **y-Achse** zeigt die **Quadratur-Komponente (Q)** – das ist der Anteil, der mit einem dazu um 90° phasenverschobenen Sinus-Träger moduliert wird.

Jeder **Punkt** im Diagramm entspricht einer eindeutigen Kombination aus Amplitude und Phase der Trägerschwingung und steht für ein bestimmtes **Symbol**, dem eine feste Bitfolge zugeordnet ist.

- Der **Abstand eines Punktes vom Ursprung** entspricht der Amplitude des Signals in diesem Zustand.
- Der **Winkel zur x-Achse** entspricht der Phase.

**Wichtig für die Praxis:** Je enger die Punkte im Diagramm zusammenliegen, desto mehr Bits pro Symbol lassen sich übertragen (höhere Datenrate) – aber desto leichter kann Rauschen einen Punkt in einen benachbarten "verschieben" und so einen Übertragungsfehler verursachen. Das Konstellationsdiagramm macht diesen Kompromiss zwischen **Datenrate** und **Störanfälligkeit** direkt sichtbar.

---

## 7. QAM (Quadraturamplitudenmodulation)

QAM kombiniert **Amplitudenmodulation zweier orthogonaler (90° phasenverschobener) Träger**, um sowohl Amplitude als auch Phase gleichzeitig zur Informationskodierung zu nutzen:

$$s(t) = I(t)\cdot\cos(2\pi f_c t) - Q(t)\cdot\sin(2\pi f_c t)$$

Dabei sind $I(t)$ und $Q(t)$ die beiden Datenströme (In-Phase und Quadratur), die jeweils mehrere Amplitudenstufen annehmen können.

**Bezeichnung nach Symbolanzahl:** Bei **QAM-$M$** gibt es $M$ mögliche Symbole (Punkte im Konstellationsdiagramm), und jedes Symbol kodiert $\log_2(M)$ Bit:

| Modulationsart | Anzahl Symbole $M$ | Bits pro Symbol |
|---|---|---|
| QAM-4 (= QPSK) | 4 | 2 |
| QAM-16 | 16 | 4 |
| QAM-64 | 64 | 6 |
| QAM-256 | 256 | 8 |

**Trade-off:** Je höher die Stufe (z. B. QAM-256), desto mehr Bits pro Symbol → höhere Datenrate bei gleicher Symbolrate, aber die Punkte im Konstellationsdiagramm liegen enger beieinander → höhere Fehleranfälligkeit bei Rauschen. Deshalb wird die QAM-Stufe in der Praxis (z. B. bei WLAN, DSL, Kabelmodem) oft dynamisch an die Kanalqualität angepasst.

---

## 8. Gray-Code

Der **Gray-Code** ist eine spezielle Art, Zahlen binär zu kodieren, bei der sich **zwischen zwei benachbarten Werten immer nur genau ein einziges Bit ändert** (im Gegensatz zum normalen Binärcode, wo sich beim Übergang z. B. von 3 auf 4 gleich mehrere Bits ändern: `011` → `100`).

**Beispiel (3-Bit):**

| Dezimal | Normaler Binärcode | Gray-Code |
|---|---|---|
| 0 | 000 | 000 |
| 1 | 001 | 001 |
| 2 | 010 | 011 |
| 3 | 011 | 010 |
| 4 | 100 | 110 |
| 5 | 101 | 111 |
| 6 | 110 | 101 |
| 7 | 111 | 100 |

**Warum wird Gray-Code bei QAM/Konstellationsdiagrammen verwendet?**

Weil Rauschen einen empfangenen Punkt im Konstellationsdiagramm am wahrscheinlichsten in einen **benachbarten** Punkt "verschiebt" (kleiner Fehler = kleine Verschiebung). Ordnet man den benachbarten Symbolen im Diagramm Bitmuster nach dem Gray-Code zu, unterscheidet sich jedes Symbol von seinen direkten Nachbarn nur in **einem einzigen Bit**. Ein solcher "Nachbarschaftsfehler" führt dann nur zu **einem** falschen Bit statt möglicherweise mehreren – das reduziert die Bitfehlerrate erheblich, ohne dass sich an der eigentlichen Übertragungstechnik etwas ändert.

---

## 9. Multiplexing – Überblick

**Multiplexing** bezeichnet Verfahren, mit denen **mehrere Datenströme gleichzeitig über ein einziges gemeinsames physikalisches Medium** übertragen werden, indem man sie in unterschiedlichen "Dimensionen" voneinander trennt:

| Verfahren | Trennung nach | Kurzbeschreibung |
|---|---|---|
| **FDM** (Frequency Division Multiplexing) | Frequenz | Jeder Kanal bekommt sein eigenes Frequenzband, gleichzeitig aktiv |
| **TDM** (Time Division Multiplexing) | Zeit | Jeder Kanal bekommt reihum ein festes Zeitfenster (Slot) |
| **CDM** (Code Division Multiplexing) | Code | Jeder Kanal bekommt einen eindeutigen Code, alle senden gleichzeitig im selben Band |
| **WDM** (Wavelength Division Multiplexing) | Wellenlänge (Farbe) | Wie FDM, aber speziell für Glasfaser mit Licht unterschiedlicher Wellenlänge |
| **SDM** (Space Division Multiplexing) | Raum | Getrennte physische Leitungen/Fasern pro Kanal |

---

## 10. CDM (Code Division Multiplexing) im Detail

Bei CDM senden **alle Teilnehmer gleichzeitig** im **selben Frequenzband** und zur **selben Zeit** – die Trennung erfolgt nicht durch Zeit oder Frequenz, sondern durch **eindeutige, orthogonale Codes** (sogenannte Chip-Sequenzen), die jedem Sender fest zugeordnet sind.

**Grundprinzip:**
1. Jeder Sender bekommt einen eigenen Code, z. B. Sender A: `+1 +1 -1 -1`, Sender B: `+1 -1 +1 -1`. Diese Codes sind **orthogonal** zueinander (ihr "Skalarprodukt" ergibt 0).
2. Um ein Bit zu senden, multipliziert der Sender sein Bit (+1 oder −1) mit seinem gesamten Code und sendet das Ergebnis.
3. Alle Sender senden gleichzeitig – auf dem gemeinsamen Medium addieren sich die Signale einfach.
4. Der Empfänger kennt den Code eines bestimmten Senders und **korreliert** (multipliziert und summiert) das empfangene Summensignal mit genau diesem Code. Wegen der Orthogonalität heben sich die Beiträge aller *anderen* Sender dabei rechnerisch auf (Summe ≈ 0), und nur das gesuchte Signal bleibt übrig.

**Wichtigste Anwendung:** Mobilfunkstandard CDMA (z. B. in älteren UMTS/3G-Netzen), wo mehrere Teilnehmer gleichzeitig dieselbe Frequenz nutzen können, ohne sich gegenseitig zu stören – solange die Codes orthogonal sind und synchron gesendet wird.

---

## 11. Twisted-Pair-Kabel

Ein Twisted-Pair-Kabel besteht aus **zwei isolierten Kupferadern, die miteinander verdrillt** sind (statt parallel geführt zu werden).

**Warum verdrillt?** Elektromagnetische Störungen (z. B. von benachbarten Kabeln, Motoren, Funksignalen) induzieren in beiden Adern nahezu **gleich starke** Störspannungen, wenn die Adern eng zusammen und regelmäßig verdrillt sind. Da am Empfänger nur die **Differenz** der beiden Adernspannungen ausgewertet wird (symmetrische/differenzielle Übertragung), heben sich die Störungen dabei größtenteils auf – man nennt das Prinzip **Übersprechunterdrückung (Crosstalk-Reduktion)**.

**Typen:**
- **UTP** (Unshielded Twisted Pair): keine zusätzliche Abschirmung, günstig, Standard in normalen Bürogebäuden.
- **STP / FTP** (Shielded/Foiled Twisted Pair): zusätzliche Metallfolie/Geflecht um die Adern(-paare) für noch bessere Störunterdrückung, teurer, für elektrisch belastete Umgebungen.

**Kategorien** (bestimmen die maximale Bandbreite/Datenrate):

| Kategorie | Max. Frequenz | Typische Anwendung |
|---|---|---|
| Cat 5e | 100 MHz | 1 Gbit/s Ethernet |
| Cat 6 | 250 MHz | 1–10 Gbit/s (Reichweite begrenzt) |
| Cat 6a | 500 MHz | 10 Gbit/s bis 100 m |
| Cat 7/7a | 600–1000 MHz | 10 Gbit/s+, geschirmt |
| Cat 8 | 2000 MHz | 25/40 Gbit/s, kurze Distanzen (Rechenzentren) |

---

## 12. Glasfaserkabel – Grundlagen

Ein Glasfaserkabel überträgt Daten nicht elektrisch, sondern als **Lichtimpulse**. Aufbau von innen nach außen:

1. **Kern (Core):** dünner Glas- (oder Kunststoff-)faden, durch den das Licht läuft.
2. **Mantel (Cladding):** umgibt den Kern mit Glas von leicht **niedrigerem** Brechungsindex.
3. **Schutzhülle (Coating/Jacket):** mechanischer Schutz.

**Funktionsprinzip – Totalreflexion:** Da der Kern einen höheren Brechungsindex hat als der Mantel, wird Licht, das in einem flachen Winkel auf die Grenzfläche Kern/Mantel trifft, **vollständig zurück in den Kern reflektiert** (statt auszutreten). Das Licht "hüpft" so praktisch verlustfrei durch die Faser, auch über sehr lange Strecken.

**Vorteile gegenüber Kupfer:** sehr hohe Bandbreite, extrem geringe Dämpfung über lange Strecken, **immun gegen elektromagnetische Störungen**, kein "Übersprechen", schwerer abzuhören (mehr Sicherheit).

---

## 13. Multimode-Faser vs. Singlemode-Faser

Der Unterschied liegt im **Kerndurchmesser** und damit in der Anzahl der möglichen Lichtwege ("Moden") durch die Faser.

### 13.1 Multimode-Faser (MMF)
- **Großer Kerndurchmesser** (typisch 50 µm oder 62,5 µm).
- Licht kann auf **vielen verschiedenen Wegen (Moden)** mit unterschiedlichen Winkeln durch den Kern laufen.
- Problem: Da die verschiedenen Wege unterschiedlich lang sind, kommen Lichtanteile eines einzelnen Impulses **zeitlich leicht versetzt** am Ende an → **Modendispersion**. Das begrenzt die maximale Distanz/Bandbreite.
- Lichtquelle: meist **LED** oder **VCSEL** (günstiger als Laser).
- Einsatz: **kurze Distanzen** (typisch bis ca. 300–550 m, je nach Standard), z. B. innerhalb von Gebäuden/Rechenzentren.
- Günstiger in Anschaffung und Betrieb als Singlemode.

### 13.2 Singlemode-Faser (SMF)
- **Sehr kleiner Kerndurchmesser** (typisch ca. 9 µm) – so klein, dass **nur ein einziger Lichtweg (Mode)**, nämlich der direkte, geradlinige Weg, möglich ist.
- Da es keine unterschiedlich langen Wege gibt, entfällt die Modendispersion fast komplett → deutlich geringere Signalverzerrung.
- Lichtquelle: **Laserdiode** (präziser, aber teurer als LED).
- Einsatz: **lange bis sehr lange Distanzen** (mehrere zehn bis hunderte Kilometer, mit Verstärkern auch interkontinental), z. B. Weitverkehrsnetze, Anbindung zwischen Städten/Rechenzentren.
- Teurer in Anschaffung (Laser, präzisere Fertigung), aber langfristig die Technologie mit der größten erreichbaren Bandbreite und Reichweite.

**Merksatz:** *Multimode = mehrere Lichtwege = kurze Strecke, günstig. Singlemode = ein Lichtweg = lange Strecke, hohe Präzision.*

---

## 14. OM-/OS-Typen im Überblick

Diese Kürzel sind genormte Klassen für Glasfaserkabel (ISO/IEC 11801):

- **OM** = **O**ptical **M**ultimode → Multimode-Fasern
- **OS** = **O**ptical **S**ingle-mode → Singlemode-Fasern

| Typ | Kerndurchmesser | Farbe (üblich) | Besonderheit / Einsatz |
|---|---|---|---|
| **OM1** | 62,5 µm | Orange | Ältester Standard, LED-basiert, für Fast Ethernet/Gigabit auf kurzer Distanz |
| **OM2** | 50 µm | Orange | Etwas bessere Bandbreite als OM1, ebenfalls älter |
| **OM3** | 50 µm | Aqua (Türkis) | Laseroptimiert, für 10-Gigabit-Ethernet bis ca. 300 m |
| **OM4** | 50 µm | Aqua oder Violett | Verbesserte Bandbreite, 10G bis 400 m, 40/100G bis ca. 100–150 m |
| **OM5** | 50 µm | Limettengrün | „Wideband"-Multimode, unterstützt mehrere Wellenlängen gleichzeitig (SWDM) für höhere Kapazität auf einer Faser |
| **OS1** | ~9 µm | Gelb | Singlemode für **Innenbereich**, engere Dämpfungstoleranzen, bis ca. 10 km |
| **OS2** | ~9 µm | Gelb | Singlemode für **Innen- und Außenbereich**, sehr geringe Dämpfung, Standard für Weitverkehrs-/Backbone-Strecken (zig bis hunderte km) |

**Merkregel für die Farben** (in der Praxis sehr nützlich zur schnellen Identifikation von Patchkabeln): Orange/Aqua/Violett/Limettengrün → Multimode (OM-Reihe), Gelb → Singlemode (OS-Reihe).

---

## Kurzübersicht zum Schnell-Wiederholen

- **Fourier-Reihe (reell):** $s(t) = a_0 + \sum (a_n\cos + b_n\sin)$ – Rechtecksignal → nur ungerade Harmonische, Amplitude $\propto 1/n$.
- **Amplituden-/Phasenspektrum:** zwei Ansichten derselben Information wie $a_n,b_n$, zusammen vollständig äquivalent zu $s(t)$.
- **OSI-Geräte:** Hub = Schicht 1, Switch = Schicht 2, Router = Schicht 3, Gateway = bis Schicht 7.
- **Durchlassband:** Signal wird auf Trägerfrequenz moduliert statt im Basisband (um 0 Hz) übertragen.
- **QAM + Konstellationsdiagramm:** Amplitude & Phase kodieren gemeinsam mehrere Bits pro Symbol; Gray-Code minimiert Bitfehler bei Nachbarschaftsverwechslung.
- **Multiplexing:** FDM = Frequenz, TDM = Zeit, CDM = Code, WDM = Wellenlänge.
- **Twisted-Pair:** Verdrillung reduziert Störeinstrahlung/Übersprechen.
- **Glasfaser:** Totalreflexion führt Licht durch den Kern; Multimode = kurze Strecke/günstig, Singlemode = lange Strecke/präzise; OM = Multimode-Normen, OS = Singlemode-Normen.