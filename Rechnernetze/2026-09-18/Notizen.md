> Alles bezieht sich auf Ethernet!

- Empfangen von Rahmen
  - Switches (MAC-Adressen sind bekannt)
- Switch-Architekturen (nur kurz)
  - Switch-Fabric
  - Shared Memory
  - Shared Bus
  - ...
- Symmetrisches / asymmetrisches Switches
- VLAN
  - Untagged VLAN
    - Acces Port
  - Tagged VLAN
    - VLAN ID
    - Trunk Port
- Spinning Tree
- STP
- UPBG
- Weiterführend 
    - NAC
    - Private VLAN
    - XVLAN
    - MPLS
    - SDN


# Ethernet-Switching: Von der Rahmenweiterleitung bis SDN

> Vorlesungsskript Rechnernetze — Schwerpunkt: Ethernet (Schicht 2)

---

## 1. Empfangen von Rahmen in Switches (MAC-Adressen bekannt)

Ein Ethernet-Switch arbeitet auf **Schicht 2** (Sicherungsschicht) des OSI-Modells und leitet Rahmen (*Frames*) anhand der **Ziel-MAC-Adresse** weiter. Im Gegensatz zu einem Hub, der jedes Bit an alle Ports repliziert (physikalische Ebene, Kollisionsdomäne), trifft ein Switch eine **gezielte Weiterleitungsentscheidung**.

### 1.1 Die Forwarding-/MAC-Adresstabelle

Jeder Switch verwaltet eine Tabelle (auch *Filtering Database*, *CAM-Table* – Content Addressable Memory) mit Einträgen der Form:

| MAC-Adresse | Port | VLAN | Alter/TTL |
|---|---|---|---|
| 00:1A:2B:3C:4D:5E | Port 3 | 10 | 120 s |

Diese Tabelle wird durch **Backward Learning** aufgebaut:

1. Trifft ein Rahmen an Port *p* ein, liest der Switch die **Quell-MAC-Adresse** aus und trägt `(Quell-MAC → Port p)` in die Tabelle ein (bzw. aktualisiert den Zeitstempel).
2. Einträge, die eine Aging-Zeit (typisch 300 s) überschreiten, ohne erneut gesehen zu werden, werden gelöscht (wichtig bei Topologieänderungen, z. B. wenn ein Endgerät den Port wechselt).

### 1.2 Weiterleitungsentscheidung (Fall: Ziel bekannt)

Ist die **Ziel-MAC-Adresse** bereits in der Tabelle vorhanden, verfährt der Switch wie folgt:

1. Nachschlagen der Ziel-MAC in der Forwarding-Tabelle → Ergebnis: Ausgangsport *q*.
2. **Filtering**: Ist *q* identisch mit dem Eingangsport *p* (Ziel hängt am selben Segment wie die Quelle), wird der Rahmen verworfen – er muss nicht weitergeleitet werden.
3. Andernfalls **Forwarding**: Der Rahmen wird ausschließlich an Port *q* ausgegeben (*unicast, gezielt* – kein Flooding).

Dieses Verfahren wird als **transparentes Switching** oder **Transparent Bridging** bezeichnet, da Endgeräte von der Existenz des Switches nichts bemerken (keine Konfiguration nötig, selbstlernend).

### 1.3 Weiterleitungsmodi

- **Store-and-Forward**: Der komplette Rahmen wird empfangen, die FCS (*Frame Check Sequence*, CRC-Prüfsumme) geprüft, defekte Rahmen verworfen. Hohe Latenz, aber hohe Fehlererkennung.
- **Cut-Through**: Sobald die Ziel-MAC-Adresse (erste 6 Byte nach Präambel) gelesen ist, beginnt die Weiterleitung, ohne den Rest des Rahmens abzuwarten. Geringere Latenz, aber fehlerhafte Rahmen können weitergeleitet werden.
- **Fragment-Free**: Kompromiss – es werden mindestens die ersten 64 Byte (Mindestrahmenlänge) abgewartet, um Kollisionsfragmente auszufiltern, bevor weitergeleitet wird.

---

## 2. Switch-Architekturen (Kurzüberblick)

Intern muss ein Switch Rahmen von einem Eingangsport zu einem (oder mehreren) Ausgangsports transportieren. Dafür gibt es verschiedene **Switching-Fabric**-Architekturen:

### 2.1 Switching via Speicher (klassisch, CPU-gesteuert)
Der Rahmen wird in den Hauptspeicher kopiert, die CPU liest die Ziel-MAC, bestimmt den Ausgangsport und kopiert den Rahmen von dort in den Ausgangspuffer. Einfach, aber langsam (zweifacher Bus-Zugriff, CPU als Flaschenhals).

### 2.2 Switching über einen (geteilten) Bus – *Shared Bus*
Alle Ports sind an einen gemeinsamen internen Bus angeschlossen. Ein eingehender Rahmen wird über den Bus an **alle** Portmodule übertragen; nur das Modul mit dem passenden Ausgangsport übernimmt ihn tatsächlich (ähnlich einem internen Broadcast-Medium). 
**Nachteil**: Der Bus selbst wird zur gemeinsamen Ressource und limitiert die Gesamtbandbreite (nur ein Rahmen gleichzeitig „on the bus“).

### 2.3 Switching über eine Kreuzschienen-/Crossbar-Matrix
Eine Matrix aus Schaltelementen verbindet jeden Eingangsport potenziell direkt mit jedem Ausgangsport. Ermöglicht **mehrere gleichzeitige, nicht überlappende Verbindungen** (parallele Pfade) und damit hohen Durchsatz, ist aber aufwendiger in der Hardware.

### 2.4 Shared-Memory-Switching
Alle Ports schreiben eingehende Rahmen in einen **gemeinsamen, sehr schnellen Speicherbereich** (statt über einen Bus zu anderen Ports). Ein Speichercontroller verwaltet Warteschlangen (Queues) pro Ausgangsport und liest die Rahmen aus dem Shared Memory in den jeweiligen Ausgangspuffer. Vorteil: effiziente Pufferverwaltung, gute Skalierbarkeit bei modernen ASICs.

> **Merke**: In der Praxis kombinieren moderne Switch-ASICs Elemente aus Crossbar- und Shared-Memory-Architekturen, um sowohl hohen Durchsatz als auch flexible Pufferverwaltung zu erreichen.

---

## 3. Symmetrische vs. asymmetrische Switches

- **Symmetrischer Switch**: Alle Ports besitzen die **gleiche Bandbreite** (z. B. alle Ports 1 GbE). Geeignet, wenn Endgeräte untereinander gleichberechtigt kommunizieren (z. B. reines Client-Netz mit gleichartigen Arbeitsplätzen).

- **Asymmetrischer Switch**: Ports besitzen **unterschiedliche Bandbreiten** (z. B. 24× 1 GbE Access-Ports + 2× 10 GbE Uplink-Ports). Dies erfordert internes **Pufferspeichern/Buffering** und ggf. **Rate Adaptation** in der Switching-Fabric, da Daten von einem schnellen in einen langsamen Port (oder umgekehrt) übertragen werden müssen, ohne dass Rahmen verloren gehen (Flusskontrolle, Queueing).

Asymmetrische Switches sind der Regelfall in realen Netzen: viele Access-Ports zu Endgeräten, wenige, schnellere Uplink-/Trunk-Ports zum Backbone bzw. zu anderen Switches.

---

## 4. VLAN (Virtual Local Area Network)

Ein **VLAN** unterteilt ein physisches Switching-Netz logisch in mehrere **getrennte Broadcast-Domänen**, ohne dass eine physikalische Neuverkabelung nötig ist. Rahmen aus VLAN A erreichen nie automatisch VLAN B — eine Kommunikation zwischen VLANs erfordert einen Router bzw. ein Layer-3-Gerät (*Inter-VLAN-Routing*).

Vorteile: Sicherheit (Trennung von Abteilungen), reduzierte Broadcast-Last, logische statt physische Netzstruktur, Flexibilität bei Umzügen von Endgeräten.

### 4.1 Untagged VLAN – Access Port

Ein **Access Port** ist einem **genau einem** VLAN fest zugeordnet.

- Rahmen, die vom Endgerät am Access Port eintreffen, sind **untagged** (Standard-Ethernet-Rahmen, kein VLAN-Kennzeichen).
- Der Switch merkt sich intern, dass dieser Rahmen zum konfigurierten VLAN des Ports gehört (implizite Zuordnung über die Portkonfiguration), und behandelt ihn ausschließlich innerhalb dieser Broadcast-Domäne.
- Beim Verlassen des Switches über einen anderen Access Port desselben VLANs wird der Rahmen wieder **untagged** ausgeliefert — das Endgerät „sieht“ nie ein VLAN-Tag.

Typischer Einsatz: Anschluss von PCs, Druckern, IP-Telefonen etc.

### 4.2 Tagged VLAN

Wenn ein Rahmen über einen Link läuft, der Datenverkehr **mehrerer VLANs gleichzeitig** transportieren muss (z. B. zwischen zwei Switches), muss dem Switch am anderen Ende mitgeteilt werden, zu welchem VLAN jeder einzelne Rahmen gehört. Dazu dient das Standard **IEEE 802.1Q**.

#### VLAN-ID (VID)
802.1Q fügt dem Ethernet-Header ein **4 Byte großes Tag** ein (zwischen Quell-MAC und Type/Length-Feld), bestehend u. a. aus:
- **TPID** (Tag Protocol Identifier, 0x8100 – signalisiert „dies ist ein 802.1Q-Tag“)
- **Priority (PCP)** – 3 Bit für QoS/Priorisierung (802.1p)
- **VLAN-ID (VID)** – 12 Bit, erlaubt Werte **1–4094** (0 und 4095 sind reserviert), identifiziert eindeutig, zu welchem VLAN der Rahmen gehört.

Da das Tag den Rahmen um 4 Byte vergrößert, steigt die maximale Ethernet-Rahmenlänge von 1518 auf 1522 Byte (*Baby Giant Frame*).

#### Trunk Port
Ein **Trunk Port** verbindet typischerweise zwei Switches (oder Switch und Router) und überträgt Rahmen **mehrerer VLANs gleichzeitig** über eine einzige physische Verbindung:

- Jeder Rahmen, der über den Trunk läuft, trägt ein **802.1Q-Tag** mit der zugehörigen VLAN-ID.
- Der empfangende Switch liest die VID aus dem Tag und ordnet den Rahmen intern dem korrekten VLAN zu, statt sich auf den Eingangsport allein zu verlassen.
- Optional kann ein **Native VLAN** definiert werden: Rahmen dieses VLANs werden auf dem Trunk *ohne* Tag übertragen (Kompatibilität mit älteren/einfacheren Geräten) — eine häufige Fehlerquelle (*VLAN Hopping*), wenn beide Trunk-Enden unterschiedliche Native VLANs konfiguriert haben.

**Zusammenfassung Access vs. Trunk:**

| Merkmal | Access Port | Trunk Port |
|---|---|---|
| Anzahl VLANs | genau 1 | mehrere |
| Tagging | untagged | 802.1Q-getaggt |
| Typischer Einsatz | Endgerät ↔ Switch | Switch ↔ Switch/Router |

---

## 5. Spanning Tree Protocol (STP)

### 5.1 Problem: Redundante Verbindungen

In realen Netzen werden Switches oft redundant verkabelt (Ausfallsicherheit). Da Ethernet Schicht-2-Rahmen **keine Time-to-Live (TTL)** besitzt, führen physikalische Schleifen (*Loops*) zu:

- **Broadcast-Stürmen** (ein Broadcast-Rahmen zirkuliert endlos und wird exponentiell vervielfacht),
- **Mehrfachzustellung** desselben Rahmens an Endgeräte,
- **Instabilität der Forwarding-Tabellen** (ein Switch lernt dieselbe Quell-MAC abwechselnd auf verschiedenen Ports).

### 5.2 Grundidee des Spanning Tree

STP (IEEE 802.1D) berechnet automatisch einen **schleifenfreien, aufspannenden Baum (Spanning Tree)** über die physische Netztopologie, indem es redundante Links logisch **blockiert** (nicht abschaltet – sie bleiben als Backup verfügbar).

**Ablauf des Algorithmus:**

1. **Root Bridge wählen**: Jeder Switch (Bridge) besitzt eine **Bridge-ID** (Priorität + MAC-Adresse). Über den Austausch von **BPDUs** (*Bridge Protocol Data Units*) wird die Bridge mit der niedrigsten Bridge-ID zur **Root Bridge** gewählt.
2. **Root Port bestimmen**: Jeder Nicht-Root-Switch bestimmt an sich selbst denjenigen Port mit dem **geringsten Pfadkosten** (Root Path Cost, abhängig von der Bandbreite der Links) zur Root Bridge — dies wird der **Root Port**.
3. **Designated Port bestimmen**: Für jedes Netzsegment (jede Leitung zwischen zwei Switches) wird derjenige Switch mit den geringsten Pfadkosten zur Root Bridge zum „Designated Switch“ für dieses Segment; dessen entsprechender Port wird **Designated Port** (leitet Verkehr für dieses Segment weiter).
4. **Blockierte Ports**: Alle übrigen Ports (weder Root- noch Designated Port) werden in den Zustand **Blocking** versetzt — sie verwerfen Nutzdaten, hören aber weiterhin BPDUs ab, um bei Ausfällen reagieren zu können.

### 5.3 Portzustände (klassisches 802.1D)

| Zustand | Bedeutung |
|---|---|
| Blocking | keine Datenweiterleitung, empfängt nur BPDUs |
| Listening | Vorbereitung, hört BPDUs, leitet noch nicht weiter |
| Learning | lernt MAC-Adressen, leitet noch nicht weiter |
| Forwarding | normale Datenweiterleitung |
| Disabled | Port administrativ deaktiviert |

Der Übergang von Blocking zu Forwarding dauert klassisch **bis zu 50 Sekunden** (Timer *Forward Delay* + *Max Age*) — ein zentraler Kritikpunkt an klassischem STP, den Weiterentwicklungen wie **RSTP** (Rapid STP, 802.1w, Sekunden statt Sekunden-zig) adressieren.

### 5.4 BPDUs

BPDUs sind spezielle Multicast-Rahmen, die zwischen Switches ausgetauscht werden und u. a. enthalten: Root-Bridge-ID, Absender-Bridge-ID, Pfadkosten zur Root sowie Timer-Werte. Über den periodischen Austausch (Standard: alle 2 s) erkennt STP Topologieänderungen und rekonfiguriert den Baum bei Bedarf neu.

---

## 6. Erweiterungen: UplinkFast, PortFast, BackboneFast, Guard-Funktionen (UPBG)

Da klassisches STP im Fehlerfall recht langsam konvergiert, wurden (v. a. herstellerspezifisch, z. B. Cisco) mehrere **Optimierungen** eingeführt:

- **PortFast**: Für Ports, an denen garantiert **kein weiterer Switch**, sondern nur ein Endgerät hängt (z. B. Access Port zu einem PC). Der Port überspringt die Zustände Listening/Learning und geht **sofort** in Forwarding — verhindert unnötige Wartezeit beim Hochfahren eines PCs (z. B. DHCP-Timeout).

- **UplinkFast**: Beschleunigt die **Umschaltung des Root Ports** bei Ausfall der aktiven Root-Verbindung an einem Access-Switch mit redundanten Uplinks. Statt auf die normalen STP-Timer zu warten, wird sofort auf einen vorher blockierten Backup-Uplink umgeschaltet (typisch < 1 s statt ~50 s).

- **BackboneFast**: Beschleunigt die Konvergenz bei **indirekten** Linkausfällen (ein Ausfall, der nicht direkt am eigenen Switch liegt, sondern „irgendwo weiter hinten“ im Baum). Reduziert die Wartezeit auf den Max-Age-Timer, indem aktiv nach alternativen Pfaden gefragt wird.

- **Guard-Mechanismen** (Schutzfunktionen):
  - **BPDU Guard**: Deaktiviert einen PortFast-Port automatisch, sobald dort unerwartet eine BPDU empfangen wird (Schutz vor versehentlichem/böswilligem Anschluss eines weiteren Switches an einen Endgeräte-Port).
  - **Root Guard**: Verhindert, dass ein Port zum Root Port wird bzw. dass ein fremder Switch über diesen Port die Rolle der Root Bridge übernimmt — schützt die gewünschte, administrativ festgelegte Root-Bridge-Position.

**Gemeinsames Ziel dieser Erweiterungen**: die strukturelle Robustheit von STP (Schleifenfreiheit) mit deutlich schnellerer Reaktion auf Topologieänderungen und besserem Schutz vor Fehlkonfigurationen zu verbinden.

---

## 7. Weiterführende Themen (nur Überblick, Funktionsweise irrelevant)

Die folgenden Konzepte werden hier bewusst nur **konzeptionell/oberflächlich** vorgestellt — es geht nur darum, *was* sie leisten, nicht *wie* sie es im Detail tun.

### 7.1 NAC – Network Access Control
Verfahren/Systeme, die vor der Vergabe von Netzzugriff prüfen, **wer oder was** sich an einem Port anmelden möchte (z. B. Authentifizierung eines Geräts via 802.1X, Prüfung des Sicherheitsstatus/Patch-Level). Ziel: nur autorisierte, „gesunde“ Geräte erhalten Zugang zum Netz.

### 7.2 Private VLAN (PVLAN)
Eine Erweiterung des klassischen VLAN-Konzepts, mit der innerhalb **eines** VLANs (einer IP-Subnetz-Domäne) zusätzliche Isolation zwischen einzelnen Ports erreicht wird — z. B. dürfen Geräte zwar alle mit einem gemeinsamen Gateway/Server kommunizieren, aber **nicht untereinander**. Nützlich in Hosting-/Rechenzentrumsumgebungen, um Kunden voneinander zu isolieren, ohne für jeden Kunden ein eigenes VLAN/Subnetz anzulegen.

### 7.3 MPLS – Multiprotocol Label Switching
Eine Technik, die Pakete anhand kurzer, fest zugewiesener **Labels** statt anhand vollständiger Layer-3-Routing-Entscheidungen durch ein Netz weiterleitet (angesiedelt „zwischen“ Schicht 2 und Schicht 3, daher „Layer 2.5“). Wird vor allem in Provider-Backbone-Netzen eingesetzt, um Traffic-Engineering, VPN-Dienste und schnelle Weiterleitung zu ermöglichen.

### 7.4 SDN – Software-Defined Networking
Architekturansatz, bei dem die **Kontrollebene** (Entscheidung, wohin Verkehr geleitet wird) von der **Datenebene** (tatsächliche Weiterleitung in den Switches) getrennt und zentral in einem **SDN-Controller** (Software) gebündelt wird — z. B. über Protokolle wie OpenFlow. Ermöglicht zentrale, programmierbare Steuerung eines gesamten Netzes anstelle dezentraler, gerätespezifischer Konfiguration.

---

## 8. Zusammenfassung

| Thema | Kernidee |
|---|---|
| Frame-Empfang im Switch | Backward Learning + gezieltes Forwarding/Filtering anhand der MAC-Tabelle |
| Switch-Architektur | Shared Bus, Shared Memory, Crossbar – Kompromiss aus Kosten, Durchsatz, Pufferung |
| Symmetrisch/asymmetrisch | Gleiche vs. unterschiedliche Portbandbreiten, Pufferung bei asymmetrischen Switches nötig |
| VLAN (Access/Trunk) | Logische Trennung von Broadcast-Domänen, 802.1Q-Tagging für Trunks |
| STP | Verhindert Schleifen durch Berechnung eines aufspannenden Baums, blockiert redundante Ports |
| UPBG | Beschleunigt/härtet STP: PortFast, UplinkFast, BackboneFast, BPDU/Root Guard |
| NAC, PVLAN, MPLS, SDN | Erweiterte Konzepte für Zugriffskontrolle, feinere Isolation, Provider-Switching, zentrale Steuerung |