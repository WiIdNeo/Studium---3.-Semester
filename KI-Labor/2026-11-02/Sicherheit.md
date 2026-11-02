# Datenschutz und Sicherheit – Lösungen

## Aufgabe 1: Überprüfung der eigenen KI-Umgebung

| Aussage | Antwort |
|---|---|
| Die Nutzung meiner Eingaben zum Training ist vertraglich ausgeschlossen. | **Ja.** Ministral 3 3B läuft lokal in LM Studio, die Eingaben verlassen den Rechner nicht und gehen an keinen Anbieter. |
| Konfigurations- und Schlüsseldateien sind vom KI-Kontext ausgeschlossen. | **Unklar.** Ein Coding-Assistent liest standardmäßig den ganzen Projektordner (auch `.env` und Schlüssel), sofern das nicht per Ignore-Datei oder Berechtigungen verhindert wird. |
| Lokale Modellserver sind nur lokal oder in einem geschützten Netz erreichbar. | **Unklar.** LM Studio lauscht standardmäßig nur auf localhost, bei aktivierter Netzwerkfreigabe kann aber jedes Gerät im Netz darauf zugreifen. |
| Eingebundene MCP-Server besitzen nur die notwendigen Rechte. | **Unklar.** MCP-Server haben oft mehr Rechte als nötig (z. B. Zugriff auf das ganze Dateisystem), was bei einem kleinen Modell durch Prompt Injection ausgenutzt werden kann. |
| Die Wissensbasis enthält keine Dokumente, die nicht alle Nutzenden sehen dürfen. | **Unklar.** Bei RAG können Nutzende über Fragen auch Inhalte abrufen, für die sie keine Berechtigung hätten, da Dokumente meist keine eigenen Zugriffsrechte haben. |

---

## Aufgabe 2: Eingabe datenschutzkonform bereinigen

### Problematische Inhalte

| Inhalt | Problem |
|---|---|
| `DB_URL=postgres://admin:Sommer2026!@10.20.1.15:5432/crm_prod` | Zugangsdaten zur Produktivdatenbank (Passwort, interne IP, Datenbankname) |
| Namen, E-Mail-Adressen, IBANs | Personenbezogene Daten (Art. 4 DSGVO) |
| `F32.1`, `E11.9` | Gesundheitsdaten (Art. 9 DSGVO, besondere Kategorie) |
| „Stadtwerke Musterstadt", `crm_prod` | Rückschluss auf Kunde und interne Systeme |
| Cloud-Chatbot im Verbrauchertarif | Kein AV-Vertrag, mögliches Training mit den Eingaben |

### Bereinigte Anfrage

> Ein Import-Job in eine PostgreSQL-Datenbank bricht mit folgendem Fehler ab:
>
> `ERROR: value too long for type character varying(20)`
>
> Die Zieltabelle hat u. a. die Spalten `name varchar(100)`, `email varchar(100)`, `iban varchar(20)`, `diagnose_code varchar(10)`. Die Quelldaten enthalten u. a. deutsche IBANs mit 22 Zeichen.
> Wie finde ich die auslösende Spalte bzw. den Datensatz und behebe das Problem sauber?

---

## Aufgabe 3: Einordnung nach dem EU AI Act

| Szenario | Risikoklasse | Rolle | Wichtigste Pflicht |
|---|---|---|---|
| **1** Coding-Assistent für interne Entwicklung | Minimales Risiko | Betreiber | Förderung der KI-Kompetenz (Art. 4) |
| **2** Lebenslauf-Vorsortierung und Ranking | Hohes Risiko (Art. 6, Anhang III: Bewerbungsverfahren) | Entwickelndes Unternehmen: Anbieter (Personaldienstleister: Betreiber) | Risikomanagement und Konformitätsbewertung (außerdem Datenqualität, technische Dokumentation, Protokollierung, menschliche Aufsicht) |
| **3** Webcam-Analyse von Aufmerksamkeit und Gefühlslage | Unannehmbares Risiko, verboten (Art. 5: Emotionserkennung in Bildungseinrichtungen) | Anbieter bzw. Betreiber | Nicht entwickeln, vertreiben oder einsetzen |
| **4** Sprachmodell schlägt Prüfungsnote vor | Hohes Risiko (Art. 6, Anhang III: Bewertung von Prüfungen in der Bildung) | Betreiber (Prüfungsamt) | Menschliche Aufsicht (Note nur als Vorschlag) |

---

## Aufgabe 4: Rechte an generierten Inhalten

### Fall A: Komplett generiertes CLI-Tool unter MIT-Lizenz

- Urheberrechtlich geschützt sind nur persönliche geistige Schöpfungen von Menschen. Rein KI-generierter Code ist voraussichtlich **nicht geschützt**.
- Die MIT-Lizenz läuft daher ins Leere, der Entwickler ist kein Rechteinhaber. Der Wettbewerber darf den Code meist **ohne Konsequenzen kopieren**, auch ohne Lizenzhinweis.
- Geschützt sein kann nur ein erheblicher menschlicher Anteil (eigene Architektur, Überarbeitung, eigene Teile).

### Fall B: Fast identische Funktion aus GPL-Projekt in proprietärem Produkt

- Die Funktion kann eine Vervielfältigung bzw. Bearbeitung des GPL-Werkes sein.
- Die GPL verlangt, dass abgeleitete Werke ebenfalls unter GPL stehen. In einem proprietären Produkt ist das ein **Lizenzverstoß** (Unterlassung, Schadensersatz).
- Verantwortlich ist das übernehmende Unternehmen, nicht der Assistent.

---

## Aufgabe 5: KI-Nutzungsrichtlinie

**Zugelassene Werkzeuge:**

| Datenklasse | Werkzeuge |
|---|---|
| Öffentlich | Alle freigegebenen Werkzeuge |
| Intern (z. B. Quellcode) | Lokale Modelle oder Cloud mit Business-Vertrag (Trainingsausschluss, AV-Vertrag) |
| Vertraulich / personenbezogen | Nur lokale Modelle, nur anonymisiert oder mit Freigabe |
| Besonders schutzwürdig | Keine KI-Nutzung |

Verbrauchertarife sind für Firmendaten nicht erlaubt.

**Regeln für Daten:** Nie in KI-Werkzeuge gelangen dürfen Passwörter, Schlüssel, Tokens und Connection-Strings, Kunden- und Mitarbeiterdaten, Gesundheits- und Bankdaten sowie Daten aus Produktivsystemen. Es werden synthetische oder anonymisierte Daten genutzt. Konfigurations- und Schlüsseldateien sind vom KI-Kontext ausgeschlossen.

**Codequalität und Lizenzen:** Generierter Code wird wie fremder Code behandelt: Pull Request mit Review durch eine zweite Person, Tests und Security-Scan. Lizenz-Scan und Public-Code-Filter sind aktiv, Copyleft-Code (z. B. GPL) wird nicht übernommen. Wesentlich KI-generierte Teile werden im Commit gekennzeichnet.

**Agenten:** Agenten und MCP-Server haben nur minimale Rechte. Menschliche Bestätigung ist nötig bei Schreiben und Löschen von Dateien, Shell-Befehlen, Git-Push und Deployment, Zugriff auf Datenbanken und Produktivsysteme sowie Versand von Nachrichten.
