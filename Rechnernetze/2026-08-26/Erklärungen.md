# Netzwerke – Grundlagen zu deinen Vorlesungs-Stichpunkten
## 1. Verkehrswert

Das ist wahrscheinlich der ungewöhnlichste Begriff für dich, weil er nicht sehr "sprechend" ist. Er kommt aus der **Verkehrstheorie** (auch Warteschlangentheorie genannt) – einem Teilgebiet der Nachrichtentechnik, das sich damit beschäftigt, wie stark eine Leitung, ein Kanal oder ein Server "unter Last" ist.

**Definition:** Der Verkehrswert beschreibt, wie stark eine Ressource (z. B. eine Telefonleitung, ein Funkkanal, ein Server) im Durchschnitt ausgelastet ist. Er wird in der Einheit **Erlang (Erl)** gemessen.

**Beispiel:** Wird eine Leitung eine Stunde lang beobachtet und ist davon 30 Minuten belegt, hat sie einen Verkehrswert von **0,5 Erlang**. Ist sie die ganze Stunde durchgängig belegt, sind das **1 Erlang**.

Man braucht diesen Wert, um Netze und Anlagen richtig zu dimensionieren: Wie viele Leitungen/Kanäle braucht ein Callcenter oder ein Mobilfunkmast, damit nicht ständig "besetzt" ist, aber man auch nicht unnötig viel Kapazität vorhält? Genau dafür nutzt man den Verkehrswert als Planungsgrundlage.

> - [Verkehrswert (Nachrichtentechnik) – Wikipedia](https://de.wikipedia.org/wiki/Verkehrswert_(Nachrichtentechnik))
> - [Erlang (Einheit) – Wikipedia](https://de.wikipedia.org/wiki/Erlang_(Einheit))

---

## 2. Durchsatz

Der Durchsatz (englisch *Throughput*) gibt an, **wie viele Daten tatsächlich** in einer bestimmten Zeit durch ein Netzwerk übertragen werden.

Wichtig ist die Abgrenzung zur **Bandbreite**:
- **Bandbreite** = maximale theoretische Kapazität einer Leitung (das "Rohr")
- **Durchsatz** = die Datenmenge, die tatsächlich hindurchfließt (das "Wasser" im Rohr)

Der Durchsatz ist praktisch immer niedriger als die Bandbreite, weil Faktoren wie Latenz (Verzögerung), Paketverlust, Protokoll-Overhead oder überlastete Geräte die tatsächliche Übertragung bremsen.

**Merksatz:** Bandbreite = "wie breit ist die Straße", Durchsatz = "wie viele Autos kommen tatsächlich pro Minute an".

> - [simpleclub – Netzwerkkomponenten einfach erklärt](https://simpleclub.com/lessons/fachinformatikerin-netzwerkkomponenten) (Textartikel mit Videoinhalten, guter Einstieg in Netzwerkgrundbegriffe)

---

## 3. Skalierbarkeit

Skalierbarkeit beschreibt, wie gut ein System (Server, Anwendung, Netzwerk) mit wachsender Last "mitwachsen" kann, ohne dass die Leistung einbricht. Es gibt zwei grundlegende Strategien:

### Vertikale Skalierung ("Scale up")
Man macht **eine einzelne** Maschine leistungsfähiger – mehr RAM, schnellere CPU, mehr Speicher.
- ✅ Einfach umzusetzen, oft ohne Code-Änderungen
- ❌ Es gibt eine physische/wirtschaftliche Obergrenze (irgendwann ist die beste Hardware verbaut)
- ❌ Meist Ausfallzeit nötig, während aufgerüstet wird

### Horizontale Skalierung ("Scale out")
Man fügt **weitere** Maschinen/Server hinzu und verteilt die Last auf mehrere Knoten.
- ✅ Theoretisch keine Obergrenze (man kann immer weitere Server dazustellen)
- ✅ Bessere Ausfallsicherheit (fällt ein Server aus, laufen die anderen weiter)
- ❌ Komplexer umzusetzen: Lastverteilung (Load Balancing) und Synchronisation zwischen den Servern nötig
- ❌ Nicht jede Software lässt sich gut parallelisieren

**Eselsbrücke:** Vertikal = "ein Rechner wird stärker" (nach oben wachsen), Horizontal = "es kommen mehr Rechner dazu" (in die Breite wachsen).

> - [Horizontale Skalierung und vertikale Skalierung – einfach & schnell erklärt](https://www.youtube.com/watch?v=3Xk26PS4em0)
> - [Vertikales vs. Horizontales Skalieren – Was ist der Unterschied?](https://www.youtube.com/shorts/GjbvOtczADs) (kurzes Short, gut zum schnellen Auffrischen)

---

## 4. Firewall

Eine Firewall ist ein **Schutzsystem**, das den Datenverkehr zwischen zwei Netzen (z. B. deinem internen Netzwerk und dem Internet) überwacht und nach festgelegten Regeln entscheidet, welcher Datenverkehr durchgelassen und welcher blockiert wird.

- Kann als **Hardware** (eigenes Gerät) oder **Software** (Programm auf einem Rechner) realisiert sein
- Prüft z. B. IP-Adressen, Ports oder ganze Datenpakete
- Ziel: unerwünschte Zugriffe von außen verhindern und schädlichen Datenverkehr aussperren

Man kann sich eine Firewall wie einen Türsteher vorstellen: Er prüft jeden, der rein oder raus will, anhand einer Gästeliste (den Firewall-Regeln).

> - [Die Firewall – schnell und einfach erklärt](https://www.youtube.com/watch?v=N6N2_5Rx3IE) – guter ausführlicher Einstieg inkl. der wichtigsten Firewall-Typen
> - [#51 Einfach Erklärt: "Was ist eine Firewall?"](https://www.youtube.com/watch?v=D94_m6O5vv0)
> - [Wie funktionieren Firewalls? (IHK-Prüfungsvorbereitung)](https://www.youtube.com/watch?v=gCFi06pAFqM) – etwas tiefer, behandelt Paketfilter, SPI-Firewalls, DMZ

> - [Florian Dalwigk – Playlist "Netzwerktechnik"](https://www.youtube.com/playlist?list=PLXyYF-Aksib7b8nQhS7cy377gSGSGgB2k)

---

## 5. CIA-Triade (auf Deutsch auch "VIV")

Das ist eines der wichtigsten Grundmodelle der IT-Sicherheit. **CIA** steht dabei nicht für den Geheimdienst, sondern für drei Schutzziele:

| Englisch | Deutsch | Bedeutung |
|---|---|---|
| **C**onfidentiality | **V**ertraulichkeit | Nur berechtigte Personen dürfen auf Daten zugreifen (z. B. durch Verschlüsselung, Zugriffsrechte) |
| **I**ntegrity | **I**ntegrität | Daten dürfen nicht unbemerkt verändert werden (z. B. durch Prüfsummen, digitale Signaturen) |
| **A**vailability | **V**erfügbarkeit | Systeme und Daten müssen dann verfügbar sein, wenn sie gebraucht werden (z. B. Schutz vor Ausfällen/DDoS-Angriffen) |

Deshalb im Deutschen manchmal auch **VIV-Triade** genannt, weil die Reihenfolge der Buchstaben angepasst wird.

**Merkhilfe:** Ein Passwort-Leck verletzt die **Vertraulichkeit**, eine unbemerkte Manipulation einer Überweisung verletzt die **Integrität**, ein lahmgelegter Webserver durch eine Überlastungsattacke verletzt die **Verfügbarkeit**.

> - [The CIA Triad | Ethical Hacking Lecture #003](https://www.youtube.com/watch?v=Dq75PAz731g) – Achtung: dieses Video ist auf **Englisch**, da es aus seiner internationalen Ethical-Hacking-Vorlesung stammt, aber inhaltlich sehr genau das Thema.
> - Auf Deutsch als Ergänzung: [simpleclub – Grundlagen der Daten- und Netzwerksicherheit](https://simpleclub.com/lessons/kfz-mechatronikerin-grundlagen-der-daten--und-netzwerksicherheit)

---

## Kurz zusammengefasst

- **Verkehrswert:** Wie stark ist eine Leitung/Ressource ausgelastet? (Einheit: Erlang)
- **Durchsatz:** Wie viele Daten kommen tatsächlich an? (im Gegensatz zur theoretischen Bandbreite)
- **Skalierbarkeit:** Wie wächst ein System mit? Vertikal = stärkere Einzelmaschine, Horizontal = mehr Maschinen
- **Firewall:** Türsteher zwischen Netzen, filtert Datenverkehr nach Regeln
- **CIA-Triade / VIV:** Die drei Schutzziele der IT-Sicherheit – Vertraulichkeit, Integrität, Verfügbarkeit

Wenn dir bei einem der Begriffe noch etwas unklar ist oder du gerne noch ein konkretes Rechenbeispiel (z. B. zum Verkehrswert mit Erlang-Formel) hättest, sag einfach Bescheid!