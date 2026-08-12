# Datenbanken

*Modulcode 4TI-DB-34, 8 ECTS, läuft über 2 Semester (3.+4.), Klausur 180 Min. im 4. Theoriesemester, keine Zugangsvoraussetzung.*

Fokus liegt auf relationalem Datenbankentwurf (ER-Modell, Normalisierung) und SQL als Abfragesprache. SQL solltest du parallel intensiv üben, da hier praktische Klausuraufgaben (Query schreiben) sehr wahrscheinlich sind.

> **Hinweis:** Die vertiefende Literatur des Moduls bezieht sich stark auf **Oracle** (u. a. "Oracle. Die umfassende Referenz"). Falls euer Praxislabor mit Oracle statt PostgreSQL/MySQL arbeitet, lohnt es sich, dich zusätzlich mit der Oracle-SQL-Syntax (z. B. `DUAL`-Tabelle, `ROWNUM`, PL/SQL) vertraut zu machen – frag am besten frühzeitig bei deinem Praxispartner nach dem eingesetzten DBMS.

## Offizielle Lerninhalte (lt. Modulbeschreibung)
- Einführung und Basiskonzepte Datenbanken, Abstraktionsebenen und Architekturmodelle
- Daten- und Datenbankmodelle, Konzepte relationaler Datenbanken
- Einführung SQL-Sprachstandard, Anfrage- und Änderungsoperationen mit SQL
- Entwurf relationaler Datenbanken, Normalisierung
- Datendefinition und Zugriffssteuerung mit SQL
- Geschichte und Standardisierung von Datenbanken und SQL

## Inhaltliche Schwerpunkte
- Entity-Relationship-Modell (ER-Modell) und ER-Diagramme
- Überführung ER-Modell → relationales Modell (Tabellen, Schlüssel, Fremdschlüssel)
- Normalisierung: 1., 2., 3. Normalform (ggf. BCNF)
- Relationale Algebra (Selektion, Projektion, Join, Vereinigung, Differenz)
- SQL: DDL (CREATE, ALTER), DML (SELECT, INSERT, UPDATE, DELETE), Joins, Aggregatfunktionen, Gruppierungen, Subqueries
- Transaktionen und ACID-Eigenschaften
- Indizes und grundlegende Optimierung

## YouTube – Playlists & Vorlesungen

| Ressource | Beschreibung | Link |
|---|---|---|
| SQL Tutorial deutsch – Grundlagen von SQL in 2 Stunden | Kompakter, praxisnaher Einstieg inkl. Übungsdatenbank zum Download | https://www.youtube.com/watch?v=P-iHxxj7heE |
| SQL Tutorial für Anfänger – Grundkurs Deutsch | Komplette Einführung in die Abfragesprache SQL | https://www.youtube.com/watch?v=7HZbGReAi5s |
| SQL Tutorial Deutsch – Komplettkurs für Anfänger | Ausführlicher Kurs mit eigener Übungsdatenbank | https://www.youtube.com/watch?v=6XH5hAEqE4k |
| Normalisierung in Datenbanken (1. bis 3. Normalform) | Schritt-für-Schritt-Erklärung der Normalformen, sehr klausurrelevant | https://www.youtube.com/watch?v=aCXKT4ycAbQ |
| Normalisierung einer relationalen Datenbank – Normalformen 1 bis 3 | Alternative Erklärung, Lehrgespräch-Format, gut zum Wiederholen | https://www.youtube.com/watch?v=wznoISlyMf0 |

## Dokumentationen & Skripte
- Datenbanken-verstehen.de – SQL-Tutorial mit Kapiteln zu ER-Modell und Normalisierung: https://www.datenbanken-verstehen.de/sql-tutorial/
- PostgreSQL-Dokumentation (offiziell, sehr gutes Nachschlagewerk für SQL-Syntax): https://www.postgresql.org/docs/current/
- W3Schools SQL Tutorial (schnelles Nachschlagen von Syntax, interaktiv testbar): https://www.w3schools.com/sql/
- SQLBolt – interaktive SQL-Übungen direkt im Browser: https://sqlbolt.com
- Oracle Live SQL – kostenlose Möglichkeit, Oracle-SQL direkt im Browser zu testen (falls im Praxisbetrieb Oracle genutzt wird): https://livesql.oracle.com

## Basisliteratur laut Modulbeschreibung (prüfungsrelevant)
- HEUER, A.; SAAKE, G.: *Datenbanken: Konzepte und Sprachen*, MITP-Verlag
- KEMPER, A.; EICKLER, A.: *Datenbanksysteme. Eine Einführung*, Oldenbourg Verlag
- Vertiefend: PETKOVIĆ, D.: *SQL – die Datenbanksprache*, McGraw-Hill; MARSCH/FRITZE: *SQL: Eine praxisorientierte Einführung*, Vieweg

## Empfohlene Vorgehensweise
1. Zuerst ER-Modellierung üben: aus einer Textaufgabe (z. B. "Bibliothek", "Universität") ein ER-Diagramm erstellen.
2. Das ER-Modell manuell in Tabellen mit Primär-/Fremdschlüsseln überführen.
3. Normalisierung an eigenen Beispielen durchziehen (bewusst unnormalisierte Tabelle nehmen und normalisieren).
4. Parallel SQL praktisch üben – am besten mit einer lokalen SQLite- oder PostgreSQL-Installation und einer Beispieldatenbank.
5. Joins sind erfahrungsgemäß der größte Stolperstein – gezielt INNER/LEFT/RIGHT JOIN mit eigenen Testtabellen durchspielen.

## SQL gezielt auffrischen
- SQLBolt (interaktiv, kostenlos): https://sqlbolt.com
- SQL Tutorial deutsch – Grundlagen von SQL in 2 Stunden: https://www.youtube.com/watch?v=P-iHxxj7heE

**Tipp:** Installiere dir frühzeitig ein DB-Tool wie DBeaver oder pgAdmin und probiere alle Beispiele aus den Videos selbst aus – SQL lernt man fast ausschließlich durch Tippen, nicht durch Zuschauen.
