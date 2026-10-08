# 1

## Prompt

```
Du bist ein sorgfältiger Rechercheassistent. Du hast Zugriff auf einen DuckDuckGo-MCP-Server (Websuche und Seitenabruf). Nutze ihn aktiv; beantworte die Rechtsfrage nicht allein aus deinem Gedächtnis.

AUSGANGSANTWORT:
„Wer mit einem Mietwagen einen Steinschlag verursacht, muss wahrscheinlich die Reparatur oder zumindest die Selbstbeteiligung bezahlen. Das hängt aber vom Mietvertrag und der Versicherung ab."

Gehe in genau diesen Schritten vor und kennzeichne sie mit Überschriften:

SCHRITT 1 – Kritische Bewertung
Bewerte die Ausgangsantwort: Was ist daran unscharf, ungenau oder möglicherweise irreführend? Beachte insbesondere, dass ein Steinschlag in der Regel nicht vom Mieter „verursacht" wird, sondern meist durch ein anderes Fahrzeug entsteht, und dass die Aussage „muss wahrscheinlich zahlen" nicht belegt ist. Liste die offenen Fragen auf.

SCHRITT 2 – Suchanfragen
Formuliere 2 bis 3 konkrete Suchanfragen auf Deutsch für den DuckDuckGo-MCP-Server (z. B. zu Steinschlag/Windschutzscheibe beim Mietwagen, Selbstbeteiligung, Haftungsfreistellung bei Vollkasko/Teilkasko im Mietvertrag, Rechtsprechung). Nenne die Anfragen im Wortlaut, bevor du sie ausführst.

SCHRITT 3 – Recherche
Führe die Suchen über das Tool aus. Rufe bei Bedarf mit dem Seitenabruf-Tool 1 bis 3 der relevantesten Seiten vollständig ab. Bevorzuge Quellen wie Verbraucherzentralen, Gerichts- und Gesetzesseiten, Automobilclubs, Fachanwaltskanzleien, Versicherer und Vermieter-AGB. Gib zu jedem verwendeten Treffer URL und Titel an.

SCHRITT 4 – Auswertung mit Trennung der Ebenen
Ordne die gefundenen Informationen getrennt in diese vier Kategorien ein. Wenn es zu einer Kategorie keine belastbare Quelle gibt, schreibe ausdrücklich „Dazu wurde keine belastbare Information gefunden":
  a) Allgemeine Rechtslage (Gesetz, z. B. Mietrecht/Haftungsgrundsätze)
  b) Gerichtsentscheidungen (nur nennen, wenn konkret belegt; Gericht, Datum, Aktenzeichen soweit auffindbar)
  c) Mietvertragsbedingungen (typische Regelungen von Vermietern, Selbstbeteiligung, Glasschäden-Klauseln)
  d) Versicherungsumfang (Haftpflicht, Teilkasko, Vollkasko, Haftungsreduzierung, Ausschlüsse)

SCHRITT 5 – Überarbeitete Antwort
Formuliere eine vorsichtige, quellenbasierte Antwort in maximal 250 Wörtern. Regeln:
- Jede wesentliche Aussage trägt einen Quellenverweis [1], [2] ...
- Keine Aussage ohne Beleg als Tatsache darstellen; Unsicheres als „laut Quelle X" oder „nach Angaben von ..." kennzeichnen.
- Keine Erfindung von Urteilen, Paragraphen oder Aktenzeichen.
- Weise auf Grenzen hin (Einzelfall, AGB des konkreten Vermieters, keine Rechtsberatung).
- Am Ende: Quellenverzeichnis (Nummer, Titel, URL).

SCHRITT 6 – Selbstprüfung
Nenne in 2 bis 3 Sätzen, welche Teile der Antwort am wenigsten abgesichert sind.
```

## Überprüfung der Modellantwort zum Steinschlag am Mietwagen

### Gesamteindruck

Die inhaltliche Richtung stimmt: Nach den gefundenen Quellen haftet der Mieter für einen Steinschlag grundsätzlich nicht. Die Antwort verstößt aber an mehreren Stellen gegen die Vorgaben der Aufgabe, vor allem gegen das Verbot, Urteile oder Paragraphen zu erfinden. In dieser Form wäre sie nicht verwendbar.

### Konkrete Fehler

#### Erfundene oder nicht belegte Angaben

- **„Landgericht Hamburg, 2019"** (Schritt 4b): Das steht in keiner der Quellen. Der ADAC-Ausschnitt spricht nur von „dem Gericht". Das ist eine Erfindung eines Urteils.
- **„§ 280 BGB [1]"** (Schritt 4a): Der Paragraph steht nicht in der Quelle. Außerdem ist § 280 BGB die allgemeine Anspruchsgrundlage für Schadensersatz bei Pflichtverletzung und keine Norm, die eine Haftung für Steinschläge ausschließt.
- **„Typische Klauseln zur Selbstbeteiligung sind oft ungültig"** (Schritt 4c): Der Ausschnitt von RA Kotz betrifft nur Klauseln zur *verschuldensunabhängigen Haftung für Steinschläge*, nicht Selbstbeteiligungsklauseln allgemein.
- **„Mieter erhalten bereits gezahlte Beträge zurück, wenn Schäden durch Dritte entstehen"**: Das verallgemeinert einen Einzelfall. Laut Ausschnitt zahlte die Vermietung in dem konkreten Fall zurück.
- **„Gerichte haben klargestellt"** (Schritt 5): Belegt ist nur ein berichteter Fall.

#### Widersprüche und falsche Quellenverweise

- Kategorie d lautet „keine belastbare Information", trotzdem steht in der Endantwort, die Selbstbeteiligung hänge „von den Versicherungsbedingungen ab", mit Verweis auf [3]. Diese Aussage ist durch [3] nicht gedeckt.
- „[d]" ist keine Quelle, und „Versicherungskasko" ist kein gängiger Begriff.
- Die Aussage „Gerichtsurteil bestätigt, dass der Mieter keinen Schadenersatzanspruch trägt" ist verdreht. Gemeint ist, dass die *Vermietung* keinen Anspruch gegen den Mieter hat.

#### Verfahrensfehler

- Die in Schritt 2 genannten drei Suchanfragen wurden nie ausgeführt. Tatsächlich lief nur „Steinschlag Mietwagen Haftung", und zwar zweimal. Außerdem wurden die Anfragen erst nach der Suche „genannt".
- Der Seitenabruf scheiterte an einem ungültigen Token und wurde nicht wiederholt. Alle Aussagen stützen sich daher nur auf Suchausschnitte, was die Antwort nirgends offenlegt.
- Die Einschränkungen (Einzelfall, AGB, keine Rechtsberatung) fehlen in der Endantwort fast vollständig.
- Die Selbstprüfung (Schritt 6) benennt die schwächsten Punkte nicht: Sie erwähnt weder den erfundenen Gerichtsfall noch den falschen Paragraphen noch die fehlenden Seitenabrufe.

#### Zu absolut formuliert

„Der Mieter haftet nicht" ist unqualifiziert. Die Quellen sagen „grundsätzlich" und knüpfen an fehlendes Verschulden an. Ein Verschulden des Mieters, etwa bei unangemessener Fahrweise, ist damit nicht ausgeschlossen.

### Korrigierte Fassung

#### Schritt 4 – Auswertung (nur belegt, aus Suchausschnitten)

- **a) Allgemeine Rechtslage:** Laut Hofauer haftet der Mieter nicht für einen Steinschlag, da dieser bei bestimmungsgemäßem Gebrauch jederzeit eintreten kann und grundsätzlich nicht vom Mieter zu vertreten ist [1]. Paragraphen wurden nicht ermittelt.
- **b) Gerichtsentscheidungen:** Der ADAC berichtet von einem Urteil, nach dem die Vermietung keinen Schadenersatzanspruch hatte, weil der Mieter den Steinschlag nicht verschuldet hatte [2]. Gericht, Datum und Aktenzeichen wurden nicht ermittelt.
- **c) Mietvertragsbedingungen:** Nach Angaben von RA Kotz sind Klauseln zur verschuldensunabhängigen Haftung für Steinschläge unwirksam [3].
- **d) Versicherungsumfang:** Dazu wurde keine belastbare Information gefunden.

#### Schritt 5 – Überarbeitete Antwort

Nach den ausgewerteten Quellen (nur Suchausschnitte, Seiten nicht vollständig gelesen) haftet ein Mieter für einen Steinschlag grundsätzlich nicht. Laut Hofauer ist das ein Schaden, der bei bestimmungsgemäßem Gebrauch jederzeit eintreten kann und nicht vom Mieter zu vertreten ist [1]. Der ADAC berichtet von einem Fall, in dem die Vermietung keinen Schadenersatzanspruch hatte, weil der Mieter den Steinschlag nicht verschuldet hatte. Solche Schäden entstünden oft durch von anderen Fahrzeugen hochgeschleuderte Steinchen [2]. Nach Angaben der Kanzlei RA Kotz sind Vertragsklauseln, die den Mieter verschuldensunabhängig für Steinschläge haften lassen, unwirksam. In dem dort geschilderten Fall zahlte die Vermietung bereits eingezogene Beträge zurück [3]. Zum Versicherungsumfang (Teil-/Vollkasko, Selbstbeteiligung) wurde keine belastbare Information gefunden.

**Grenzen:** Es handelt sich um Einzelfälle und Meinungen von Dritten. Gericht und Aktenzeichen wurden nicht ermittelt. Maßgeblich bleiben der konkrete Mietvertrag und die AGB des Vermieters. Dies ist keine Rechtsberatung.

**Quellen:**
[1] Steinschlag am Mietfahrzeug – wer haftet? – Hofauer: https://hofauer.com/steinschlag-am-mietfahrzeug-wer-haftet
[2] Steinschlag am Mietwagen: Muss man die Selbstbeteiligung zahlen? – ADAC: https://www.adac.de/news/steinschlag-mietwagen/
[3] Haftung für einen Steinschlag: Mietwagen-Klausel gekippt – RA Kotz: https://www.ra-kotz.de/haftung-fuer-einen-steinschlag-wann-mieter-beim-mietwagen-nicht-zahlen-muessen.htm

#### Schritt 6 – Selbstprüfung

Am wenigsten abgesichert ist alles, was über die Suchausschnitte hinausgeht. Die Seiten wurden nicht vollständig gelesen, daher sind Details des berichteten Urteils und der Umfang der Klauselunwirksamkeit offen. Der Versicherungsumfang ist gar nicht belegt. Die Verallgemeinerung von einem berichteten Fall auf „Mieter haften grundsätzlich nicht" sollte vor einer Verwendung anhand der Volltexte geprüft werden.

## Kurze Bewertung (Vorlage)

| Kriterium | Ursprüngliche Antwort | Überarbeitete Antwort |
|---|---|---|
| Belegbarkeit / Quellen | keine Quellen | ⟦...⟧ |
| Präzision (Haftungsgrundlage, Rolle von Vertrag/Versicherung) | vage („wahrscheinlich") | ⟦...⟧ |
| Trennung Gesetz / Rechtsprechung / Vertrag / Versicherung | nicht vorhanden | ⟦...⟧ |
| Vorsicht / Hinweis auf Einzelfall | teilweise | ⟦...⟧ |

---

# Aufgabe 2: MCP-Server des DHSN-Serviceportals verwenden

## 2.2 Prompt

```
Du bist ein Assistent für Studierende der DHSN Glauchau. Du hast Zugriff auf das Tool “DHSN-Umfragen”. Verwende AUSSCHLIESSLICH diesen Server, um die folgende Frage zu beantworten; nutze keine anderen Quellen und kein eigenes Vorwissen über die DHSN.

FRAGE:
Ich möchte im Rahmen meines Studiums ein Studierendenprojekt umsetzen. Wie läuft die Projektverwaltung dafür am Serviceportal ab? Welche Schritte, Zuständigkeiten, Formulare, Fristen und Ansprechpersonen sind relevant, von der Projektidee bis zum Abschluss?

VORGEHEN (genau einhalten):
1. Prüfe zuerst, welche Tools und Ressourcen der Server bereitstellt. Liste sie kurz auf (Name, Zweck).
2. Wähle das Tool bzw. die Ressource, die für Projektverwaltung zuständig ist, und begründe die Wahl in einem Satz. Wenn mehrere in Frage kommen, nutze die passenden nacheinander.
3. Richte eine gezielte Anfrage an das zuständige Portal. Formuliere die Parameter präzise (z. B. Stichwörter wie „Projekt", „Studierendenprojekt", „Projektverwaltung") und nenne sie vor dem Aufruf.
4. Wenn der Server keine oder unvollständige Informationen liefert, versuche eine alternative Formulierung (maximal 2 weitere Versuche). Erfinde nichts. Wenn weiterhin nichts gefunden wird, sage das ausdrücklich.
5. Erfinde keine Informationen. Alles, was nicht im Tool-Ergebnis steht, ist als „nicht im Portal gefunden" zu kennzeichnen. Trenne klar zwischen „Angabe des Portals" und „eigene Einordnung".

AUSGABEFORMAT:
- **Verwendete Tools/Ressourcen:** Liste mit Name und verwendeten Parametern
- **Antwort (strukturiert):** Überschriften je Themenblock (z. B. Ablauf, Zuständigkeiten, Formulare/Dokumente, Fristen, Kontakte); zu jedem Punkt ein Verweis wie [Quelle: Tool/Ressource, Titel/ID des Eintrags]
- **Nicht gefunden / offen:** Liste der Punkte, zu denen das Portal nichts geliefert hat
- **Hinweise:** Maximal 3 Sätze zu Unsicherheiten
```

## 2.3 Antwort

> Da das Modell selbst nach vielen Versuchen das Tool nicht identifizieren konnte, obwohl alle anderen MCP-Server problemlos ansprechbar sind, gehe ich von einem Problem mit dem Toolsatz aus.

---

# Aufgabe 3: Modulhandbücher von TI und WI mit RAG vergleichen

## 3.1 Dokumente im RAG-Ordner

Lege beide Modulhandbücher im Dokumentenordner des RAG-MCP-Servers ab (Pfade anpassen):

```
⟦C:\rag-mcp\documents\⟧
├── ⟦Modulhandbuch_Technische_Informatik.pdf⟧
└── ⟦Modulhandbuch_Wirtschaftsinformatik.pdf⟧
```

> Verwende die **aktuellen** Fassungen und notiere Version/Stand und Studienordnungsjahr der Handbücher, weil Vergleiche über unterschiedliche Stände irreführen. ⟦Stand TI: ... / Stand WI: ...⟧

## 3.2 RAG-Konfiguration

Je nach verwendetem RAG-MCP-Server (z. B. ein eigener Python-Server mit FastMCP, Embeddings und Vektorspeicher) variieren die Parameternamen. Dokumentiere die **tatsächlichen** Werte. Beispielhafte Vorlage:

```json
{
  "mcpServers": {
    "rag-modulhandbuecher": {
      "command": "⟦python⟧",
      "args": ["⟦C:\\rag-mcp\\server.py⟧"],
      "env": {
        "DOCS_DIR": "⟦C:\\rag-mcp\\documents⟧",
        "EMBEDDING_MODEL": "⟦z. B. nomic-embed-text / multilingual-e5⟧",
        "CHUNK_SIZE": "⟦z. B. 800⟧",
        "CHUNK_OVERLAP": "⟦z. B. 100⟧",
        "TOP_K": "⟦z. B. 8⟧",
        "VECTOR_STORE": "⟦z. B. Chroma / FAISS / pgvector⟧"
      }
    }
  }
}
```

| Parameter | Wert | Begründung |
|---|---|---|
| Embedding-Modell | ⟦⟧ | ⟦mehrsprachig/deutsch geeignet?⟧ |
| Chunk-Größe / Overlap | ⟦⟧ | ⟦Modulbeschreibungen sind tabellarisch und strukturiert, daher moderat große Chunks⟧ |
| Top-K | ⟦⟧ | ⟦für Vergleich zweier Dokumente eher höher (z. B. 8–10)⟧ |
| Chat-Modell in LM Studio | ⟦⟧ | ⟦Kontextfenster beachten⟧ |
| Indexierungsstatus | ⟦Anzahl Chunks pro Dokument⟧ | ⟦⟧ |

## 3.3 Prompt

```
Du bist ein Studienberatungs-Analyst. Du hast Zugriff auf einen RAG-MCP-Server, der die Modulhandbücher der Studiengänge „Technische Informatik (TI)" und „Wirtschaftsinformatik (WI)" der DHSN Glauchau enthält. Vergleiche beide Studiengänge ausschließlich auf Basis der Treffer dieses Servers. Verwende kein eigenes Vorwissen über die Studiengänge.

ARBEITSWEISE:
1. Prüfe zuerst, welche Tools der RAG-Server anbietet, und teste mit einer kurzen Suche, ob beide Dokumente auffindbar sind (TI und WI). Nenne, welches Dokument du für welche Aussage herangezogen hast.
2. Führe für JEDE der folgenden Fragen mindestens eine eigene, gezielte Suche pro Studiengang durch (also getrennte Suchen für TI und WI), statt eine einzige allgemeine Suche zu machen. Nenne vor jeder Suche die Suchanfrage.
3. Erfinde keine Module, Credits (ECTS), Semester oder Inhalte. Wenn etwas nicht in den Treffern steht, schreibe „nicht in den Treffern gefunden". Gib Modulnamen exakt wie in den Dokumenten an.
4. Kennzeichne bei jeder Aussage, aus welchem Studiengang und welchem Modul/Abschnitt sie stammt.

FRAGEN:
1. Welche gemeinsamen Grundlagenmodule gibt es (z. B. Mathematik, Grundlagen der Informatik)? Tabelle mit Modulname TI, Modulname WI, ggf. ECTS/Semester.
2. Welche Programmier-, Softwareentwicklungs- und Informatikinhalte überschneiden sich? Nenne Module und inhaltliche Gemeinsamkeiten sowie Unterschiede in Tiefe oder Programmiersprachen.
3. Welche Module sind für Technische Informatik spezifisch (z. B. Elektronik, Hardware, eingebettete Systeme, Rechnerarchitektur, Signale, Regelungstechnik, soweit in den Treffern vorhanden)?
4. Welche Module sind für Wirtschaftsinformatik spezifisch (z. B. BWL, Rechnungswesen, Geschäftsprozesse, ERP, Projekt-/IT-Management, soweit in den Treffern vorhanden)?
5. Wie unterscheiden sich technische, betriebswirtschaftliche und organisatorische Inhalte? Nenne grob den jeweiligen Anteil, nur wenn er aus den Modulen/ECTS belegbar ist. Keine geschätzten Prozentzahlen ohne Beleg.
6. Welche Unterschiede bestehen bei den Praxisphasen und der Theorie-Praxis-Verzahnung (Praxismodule, Praxisphasen, Projekt- und Bachelorarbeit, Umfang, Lage im Studienverlauf)?
7. Welche unterschiedlichen Kompetenzprofile ergeben sich aus den Modulschwerpunkten (fachlich, methodisch, sozial/überfachlich)? Begründe jede Zuschreibung mit konkreten Modulen.

AUSGABEFORMAT:
- Kurzüberblick (max. 5 Sätze)
- Je Frage ein Abschnitt mit Tabelle oder Aufzählung und Quellenangaben (Studiengang, Modul)
- Abschnitt „Lücken und Unsicherheiten": Welche Fragen konnten nicht oder nur teilweise belegt werden?
- Abschnitt „Verwendete Suchanfragen": Liste aller Suchanfragen mit Anzahl der Treffer
- Schlussfolgerung: Für welche Interessenprofile eignet sich TI, für welche WI (max. 6 Sätze, nur aus den belegten Befunden abgeleitet)
```

> **Praxistipp:** Lokale Modelle verlieren bei sehr langen Aufträgen oft Teilfragen. Wenn die Antwort lückenhaft ist, stelle die Fragen 1–7 **einzeln nacheinander** im selben Chat (Prompt unverändert als Systemrahmen davor) und dokumentiere das. Das ist legitim, solange du es angibst.

## 3.4 Abzugebende Ergebnisse

### Verwendete Modulhandbücher / Pfade
⟦Dateinamen, Pfade, Stand/Version⟧

### RAG-Konfiguration
Siehe 3.2 (ausgefüllt).

### Prompt
Siehe 3.3.

### Verwendete Tool-Aufrufe (RAG-Suchen)
⟦Aufrufe laut Protokollvorlage: Suchanfrage, Parameter, Trefferliste unverändert⟧

### Finale Vergleichsanalyse
⟦Vollständige Ausgabe des Modells, unverändert⟧

### Reflexion zur Qualität der gefundenen Treffer (Gerüst)

Beantworte anhand der Tool-Rückgaben:

1. **Abdeckung:** Wurden für alle 7 Fragen Treffer aus **beiden** Dokumenten gefunden, oder dominierte ein Dokument?
2. **Relevanz:** Welcher Anteil der Treffer war inhaltlich passend? Beispiele für irrelevante oder redundante Chunks.
3. **Chunk-Qualität:** Wurden Modultabellen (ECTS, Semester, Prüfungsform) zerrissen oder falsch gelesen? Gingen Modulnamen von den zugehörigen Inhalten verloren?
4. **Vollständigkeit:** Fehlen Module, die du im Original-Handbuch findest? (Stichprobe: mindestens 5 Module im PDF gegenprüfen.)
5. **Korrektheit:** Stimmen Modulnamen, ECTS und Praxisphasen mit den Originaldokumenten überein? Gab es Halluzinationen oder Vermischungen zwischen TI und WI?
6. **Einfluss der Parameter:** Wie würden andere Chunk-Größen, ein höherer Top-K oder getrennte Indizes pro Studiengang das Ergebnis verbessern?
7. **Gesamtfazit:** Eignung von RAG für Dokumentenvergleiche und typische Grenzen (Vergleich erfordert Abdeckung statt nur Ähnlichkeitssuche).

⟦Dein Text⟧

---

## Abgabe-Checkliste

- [ ] Aufgabe 1: Prompt, Tool-Aufrufe (search/fetch), überarbeitete Antwort, Bewertung
- [ ] Aufgabe 2: MCP-Konfiguration (Tokens geschwärzt), Prompt, vollständiger Tool-Aufruf, Server-Ausgabe, Modellantwort, Bewertung
- [ ] Aufgabe 3: Dokumentpfade, RAG-Konfiguration, Prompt, Tool-Aufrufe, Vergleichsanalyse, Reflexion
- [ ] Fehlermeldungen und nicht gefundene Informationen unverändert protokolliert
- [ ] Tool-Ergebnisse nicht redaktionell verändert
