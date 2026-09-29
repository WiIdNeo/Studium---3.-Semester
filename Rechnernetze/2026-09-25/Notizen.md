- Spanning Tree
- Link Aggregation Control Protocol
- LAG und MLAG
- EAPS
- FDP-Paket: Speichert MAC-Adressen zu den Ports

|Schicht | Geräte|
|--|--|
5 - 7 Anwendungsschicht | Anwendungs-Gateway
4 Transportschicht | Transport-Gateway
3 Vermittlungsschicht | Router
2 Sicherungsschicht | Switches (Bridges)
1 Bitübertragungsschicht|Hubs, Repearter

- CSMA/CD


# Layer 3

- IPv4-Paket
  - TTL: Time to Live, Maximale Hops
  - Total Length, Maximal 64 kByte
- ICMP
- IGMP
- GRE
- ESP
- IP-Fragmentierung

- IP-Adressen (IPv4)
  - Private Addressbereiche
  - Subnetting
  - Supernetting



# Zusammenfassung: Netzwerktechnik (Uni-Niveau)

## Schicht 2 – Sicherungsschicht (Data Link Layer)

### Spanning Tree Protocol (STP, IEEE 802.1D)
Verhindert Schleifen (Loops) in vermaschten Switch-Netzen, die sonst zu Broadcast-Stürmen und instabilen MAC-Tabellen führen würden.

- **Root Bridge**: wird über die niedrigste Bridge-ID (Priorität + MAC-Adresse) gewählt; Ausgangspunkt des Spannbaums.
- **Portrollen**: Root Port (kürzester Weg zur Root), Designated Port (weiterleitend pro Segment), Blocking Port (deaktiviert zur Schleifenvermeidung).
- **BPDUs** (Bridge Protocol Data Units): dienen dem Informationsaustausch zwischen Switches.
- **Konvergenzzeit**: klassisches STP braucht ca. 30–50 s.
- **Weiterentwicklungen**: RSTP (802.1w, deutlich schnellere Konvergenz), MSTP (802.1s, mehrere Spannbäume pro VLAN-Gruppe für Lastverteilung).

### Link Aggregation Control Protocol (LACP, IEEE 802.3ad / 802.1AX)
Bündelt mehrere physische Links zu einem logischen Link (höhere Bandbreite + Redundanz), ohne dass STP diese blockiert.

- Dynamische Aushandlung zwischen den Endpunkten über **LACPDUs**.
- Lastverteilung meist per Hash-Algorithmus (z. B. auf Basis MAC-, IP-Adresse oder Portnummer).
- Abgrenzung zu **statischem** Port-Channel (ohne Aushandlungsprotokoll, „Mode On“).

### LAG und MLAG
- **LAG (Link Aggregation Group)**: Oberbegriff für gebündelte Links zwischen zwei Geräten (kann statisch oder via LACP realisiert sein).
- **MLAG (Multi-Chassis LAG)**: Erweiterung, bei der ein LAG über **zwei physisch getrennte Switches** aufgespannt wird, die sich gegenüber dem angeschlossenen Gerät als ein logischer Switch verhalten. Vorteil: Redundanz auf Switch-Ebene ohne STP-Blocking, da beide Uplinks aktiv genutzt werden. Herstellerspezifische Umsetzungen (z. B. Cisco vPC, HPE IRF).

### EAPS (Ethernet Automatic Protection Switching, RFC 3619)
Ring-basiertes Redundanzprotokoll (v. a. für Metro-Ethernet/Provider-Netze), Alternative zu STP.

- Ein **Master-Node** mit Primär- und Sekundärport überwacht den Ring; im Normalbetrieb ist der Sekundärport blockiert.
- Health-Check-Pakete über ein Control-VLAN erkennen Ausfälle.
- Bei Linkausfall wird der blockierte Port sehr schnell (< 1 s) freigegeben → deutlich schneller als klassisches STP.

### MAC-Adresstabelle / Forwarding Database (Anmerkung)
Vermutlich meinst du die **FDB (Forwarding Database)**, nicht „FDP": Ein Switch lernt beim Empfang von Frames die Quell-MAC-Adresse und den zugehörigen Eingangsport und trägt dies in seine MAC-/CAM-Tabelle ein. Anhand dieser Tabelle entscheidet er, ob ein Frame gezielt weitergeleitet oder (bei unbekanntem Ziel) geflutet wird. Einträge besitzen einen Aging-Timer und werden nach Inaktivität verworfen.

### OSI-Schichten und zugehörige Geräte

| Schicht | Geräte |
|---|---|
| 5–7 Anwendungsschicht | Anwendungs-Gateway |
| 4 Transportschicht | Transport-Gateway |
| 3 Vermittlungsschicht | Router |
| 2 Sicherungsschicht | Switches (Bridges) |
| 1 Bitübertragungsschicht | Hubs, Repeater |

Grundprinzip: Geräte arbeiten jeweils bis zu der Schicht, deren Adressierungsinformationen sie auswerten (Hub: nur Signalregeneration, Switch: MAC-Adressen, Router: IP-Adressen, Gateways: höhere Protokollumsetzung).

### CSMA/CD (Carrier Sense Multiple Access with Collision Detection)
Zugriffsverfahren des klassischen (Halbduplex-)Ethernet:

1. **Carrier Sense**: Medium vor dem Senden abhören.
2. **Multiple Access**: mehrere Stationen teilen sich dasselbe Medium.
3. **Collision Detection**: Kollisionen werden während des Sendens erkannt, ein Jam-Signal wird gesendet, danach folgt ein zufälliger Backoff (Binary Exponential Backoff) vor erneutem Sendeversuch.

In modernen vollduplexfähigen Switch-Netzen praktisch obsolet, da es keine gemeinsam genutzten Kollisionsdomänen mehr gibt.

---

## Schicht 3 – Vermittlungsschicht

### IPv4-Paket
- **TTL (Time to Live)**: begrenzt die maximale Anzahl an Hops; wird bei jedem Router um 1 dekrementiert, bei 0 wird das Paket verworfen und ein ICMP „Time Exceeded" gesendet – verhindert unendlich kreisende Pakete.
- **Total Length**: 16-Bit-Feld, daher maximal 65.535 Byte (≈ 64 KB) inklusive Header – in der Praxis meist durch die MTU der Verbindung stärker begrenzt.

### ICMP (Internet Control Message Protocol)
Dient der Fehlermeldung und Diagnose auf Netzwerkebene (z. B. „Destination Unreachable", „Time Exceeded"); Basis für Ping und Traceroute. Wird direkt in IP gekapselt, kennt keine Portnummern.

### IGMP (Internet Group Management Protocol)
Verwaltet Multicast-Gruppenmitgliedschaften zwischen Hosts und Routern (Beitritt/Verlassen von Multicast-Gruppen). Versionen 1–3 mit zunehmender Funktionalität (u. a. Source-Filtering in v3).

### GRE (Generic Routing Encapsulation)
Tunnelprotokoll, das beliebige Layer-3-Pakete in IP kapselt (z. B. für VPNs oder Routing über nicht-IP-fähige Zwischennetze). Bietet selbst **keine Verschlüsselung**.

### ESP (Encapsulating Security Payload)
Teil von **IPsec**; bietet Vertraulichkeit (Verschlüsselung), Integrität und Authentizität der Nutzdaten. Abgrenzung zu **AH (Authentication Header)**, das nur Integrität/Authentizität, aber keine Verschlüsselung liefert.

### IP-Fragmentierung
Wird nötig, wenn ein Paket größer als die MTU eines Teilstrecken-Links ist.

- Relevante Header-Felder: **Identification**, **Flags** (DF = Don't Fragment, MF = More Fragments), **Fragment Offset**.
- Reassemblierung erfolgt erst am **Zielsystem**, nicht auf Zwischenroutern.
- In der Praxis oft unerwünscht (Performance, Paketverlustanfälligkeit) → **Path MTU Discovery** ermittelt die kleinste MTU entlang des Pfads, um Fragmentierung zu vermeiden.

### IP-Adressen (IPv4)
- **Private Adressbereiche (RFC 1918)**: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 – nicht im öffentlichen Internet routbar.
- **Subnetting**: Aufteilung eines Adressblocks in kleinere Subnetze durch Verlängerung der Netzmaske (Host-Bits werden zu Netz-Bits) – reduziert Broadcast-Domänen, erhöht Struktur.
- **Supernetting**: umgekehrter Vorgang – Zusammenfassung mehrerer kleinerer, zusammenhängender Netze zu einem größeren Adressblock (CIDR-Aggregation), z. B. zur Reduktion von Routing-Tabellen-Einträgen (Route Summarization).