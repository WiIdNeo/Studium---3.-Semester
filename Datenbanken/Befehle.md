# SQL-Befehle – Ausführliche Referenz

Diese Referenz erklärt die wichtigsten SQL-Befehle mit allen gängigen Parametern und Klauseln. Alle Beispiele beziehen sich auf eine fiktive Datenbank namens **`firma_db`** mit folgendem Schema:

- **`abteilungen`** (`abteilung_id`, `name`, `standort`, `budget`)
- **`mitarbeiter`** (`mitarbeiter_id`, `vorname`, `nachname`, `abteilung_id`, `gehalt`, `einstellungsdatum`, `email`)
- **`projekte`** (`projekt_id`, `titel`, `abteilung_id`, `start_datum`, `end_datum`, `status`)
- **`mitarbeiter_projekte`** (`mitarbeiter_id`, `projekt_id`, `rolle`)

---

## Inhaltsverzeichnis

1. [Datenbank- und Tabellenverwaltung (DDL)](#1-datenbank--und-tabellenverwaltung-ddl)
2. [Daten abfragen: SELECT](#2-daten-abfragen-select)
3. [Daten einfügen: INSERT](#3-daten-einfügen-insert)
4. [Daten ändern: UPDATE](#4-daten-ändern-update)
5. [Daten löschen: DELETE / TRUNCATE](#5-daten-löschen-delete--truncate)
6. [Joins](#6-joins)
7. [Indizes](#7-indizes)
8. [Views](#8-views)
9. [Transaktionen (TCL)](#9-transaktionen-tcl)
10. [Rechteverwaltung (DCL)](#10-rechteverwaltung-dcl)
11. [Nützliche Zusatzfunktionen](#11-nützliche-zusatzfunktionen)

---

## 1. Datenbank- und Tabellenverwaltung (DDL)

### `CREATE DATABASE`

Erstellt eine neue Datenbank.

```sql
CREATE DATABASE firma_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

**Parameter:**
| Parameter | Bedeutung |
|---|---|
| `IF NOT EXISTS` | Verhindert Fehler, falls die Datenbank bereits existiert |
| `CHARACTER SET` | Legt den Zeichensatz fest (z. B. `utf8mb4`) |
| `COLLATE` | Legt die Sortierregeln fest (z. B. `utf8mb4_unicode_ci`) |

```sql
CREATE DATABASE IF NOT EXISTS firma_db;
```

### `CREATE TABLE`

Erstellt eine neue Tabelle mit Spalten, Datentypen und Constraints.

```sql
CREATE TABLE abteilungen (
    abteilung_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    standort VARCHAR(100) DEFAULT 'Unbekannt',
    budget DECIMAL(12,2) CHECK (budget >= 0)
);

CREATE TABLE mitarbeiter (
    mitarbeiter_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(50) NOT NULL,
    nachname VARCHAR(50) NOT NULL,
    abteilung_id INT,
    gehalt DECIMAL(10,2),
    einstellungsdatum DATE DEFAULT (CURRENT_DATE),
    email VARCHAR(150) UNIQUE,
    FOREIGN KEY (abteilung_id) REFERENCES abteilungen(abteilung_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

**Wichtige Constraints/Parameter:**
| Constraint | Bedeutung |
|---|---|
| `PRIMARY KEY` | Eindeutiger Zeilen-Identifikator |
| `AUTO_INCREMENT` | Automatisch hochzählender Wert (MySQL); Äquivalent in Postgres: `SERIAL`/`GENERATED ALWAYS AS IDENTITY` |
| `NOT NULL` | Spalte darf keine NULL-Werte enthalten |
| `UNIQUE` | Werte müssen eindeutig sein |
| `DEFAULT` | Standardwert, falls kein Wert angegeben wird |
| `CHECK` | Bedingung, die jeder Wert erfüllen muss |
| `FOREIGN KEY ... REFERENCES` | Verweist auf eine andere Tabelle |
| `ON DELETE` / `ON UPDATE` | Verhalten bei Löschen/Ändern des referenzierten Datensatzes (`CASCADE`, `SET NULL`, `RESTRICT`, `NO ACTION`) |

### `ALTER TABLE`

Verändert eine bestehende Tabellenstruktur.

```sql
-- Spalte hinzufügen
ALTER TABLE mitarbeiter ADD COLUMN telefon VARCHAR(20);

-- Spalte ändern (Datentyp)
ALTER TABLE mitarbeiter MODIFY COLUMN telefon VARCHAR(30);

-- Spalte umbenennen
ALTER TABLE mitarbeiter RENAME COLUMN telefon TO telefonnummer;

-- Spalte löschen
ALTER TABLE mitarbeiter DROP COLUMN telefonnummer;

-- Constraint hinzufügen
ALTER TABLE mitarbeiter ADD CONSTRAINT chk_gehalt CHECK (gehalt > 0);

-- Tabelle umbenennen
ALTER TABLE mitarbeiter RENAME TO angestellte;
```

### `DROP TABLE` / `DROP DATABASE`

Löscht Tabelle oder Datenbank vollständig (inkl. Struktur).

```sql
DROP TABLE IF EXISTS projekte;
DROP DATABASE IF EXISTS firma_db;
```

| Parameter | Bedeutung |
|---|---|
| `IF EXISTS` | Kein Fehler, falls Objekt nicht existiert |
| `CASCADE` | Löscht auch abhängige Objekte (z. B. Views, Foreign Keys) — v. a. in PostgreSQL |
| `RESTRICT` | Verweigert das Löschen, wenn Abhängigkeiten bestehen (Standard) |

---

## 2. Daten abfragen: SELECT

Der vollständige Aufbau eines `SELECT`-Befehls in der logischen Reihenfolge:

```sql
SELECT [DISTINCT] spalten
FROM tabelle
[JOIN ... ON ...]
[WHERE bedingung]
[GROUP BY spalten]
[HAVING bedingung]
[ORDER BY spalten [ASC|DESC]]
[LIMIT anzahl [OFFSET n]];
```

### Grundlegendes SELECT

```sql
SELECT vorname, nachname, gehalt
FROM mitarbeiter;
```

### `DISTINCT` – doppelte Zeilen entfernen

```sql
SELECT DISTINCT standort
FROM abteilungen;
```

### `WHERE` – Filtern von Zeilen

```sql
SELECT * FROM mitarbeiter
WHERE gehalt > 50000
  AND abteilung_id = 2
  AND (email LIKE '%@firma.de' OR email IS NULL);
```

**Operatoren in `WHERE`:**
| Operator | Bedeutung | Beispiel |
|---|---|---|
| `=`, `<>` / `!=` | gleich / ungleich | `abteilung_id = 2` |
| `<`, `>`, `<=`, `>=` | Vergleich | `gehalt >= 40000` |
| `BETWEEN ... AND ...` | Bereich | `gehalt BETWEEN 30000 AND 60000` |
| `IN (...)` | Liste von Werten | `abteilung_id IN (1, 2, 3)` |
| `LIKE` | Mustersuche (`%` = beliebig viele Zeichen, `_` = ein Zeichen) | `nachname LIKE 'Sch%'` |
| `IS NULL` / `IS NOT NULL` | NULL-Prüfung | `email IS NOT NULL` |
| `AND`, `OR`, `NOT` | Logische Verknüpfung | `NOT (gehalt < 30000)` |
| `EXISTS` | Prüft, ob Unterabfrage Ergebnisse liefert | siehe Beispiel unten |

```sql
-- Unterabfrage mit EXISTS
SELECT name FROM abteilungen a
WHERE EXISTS (
    SELECT 1 FROM mitarbeiter m
    WHERE m.abteilung_id = a.abteilung_id AND m.gehalt > 80000
);
```

### `GROUP BY` und Aggregatfunktionen

```sql
SELECT abteilung_id, COUNT(*) AS anzahl_mitarbeiter, AVG(gehalt) AS durchschnittsgehalt
FROM mitarbeiter
GROUP BY abteilung_id;
```

**Aggregatfunktionen:** `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`

### `HAVING` – Filtern nach der Gruppierung

```sql
SELECT abteilung_id, AVG(gehalt) AS durchschnitt
FROM mitarbeiter
GROUP BY abteilung_id
HAVING AVG(gehalt) > 45000;
```

> **Unterschied `WHERE` vs. `HAVING`:** `WHERE` filtert einzelne Zeilen *vor* der Gruppierung, `HAVING` filtert Gruppen *nach* der Aggregation.

### `ORDER BY` – Sortieren

```sql
SELECT vorname, nachname, gehalt
FROM mitarbeiter
ORDER BY gehalt DESC, nachname ASC;
```

| Parameter | Bedeutung |
|---|---|
| `ASC` | aufsteigend (Standard) |
| `DESC` | absteigend |
| Mehrere Spalten | Sortiert zuerst nach der ersten, dann nach der zweiten Spalte |

### `LIMIT` / `OFFSET` – Ergebnisse begrenzen

```sql
SELECT * FROM mitarbeiter
ORDER BY gehalt DESC
LIMIT 5 OFFSET 10;   -- die Zeilen 11 bis 15
```

*(In SQL Server: `SELECT TOP 5 ... `; in Oracle: `FETCH FIRST 5 ROWS ONLY`)*

### Unterabfragen (Subqueries)

```sql
SELECT vorname, nachname
FROM mitarbeiter
WHERE gehalt > (SELECT AVG(gehalt) FROM mitarbeiter);
```

### `UNION` / `UNION ALL`

Verbindet Ergebnismengen mehrerer `SELECT`-Abfragen.

```sql
SELECT vorname AS name FROM mitarbeiter
UNION
SELECT titel AS name FROM projekte;
```

| Variante | Bedeutung |
|---|---|
| `UNION` | Entfernt Duplikate |
| `UNION ALL` | Behält alle Zeilen (schneller) |

---

## 3. Daten einfügen: INSERT

```sql
-- Einzelne Zeile
INSERT INTO abteilungen (name, standort, budget)
VALUES ('IT', 'Chemnitz', 250000.00);

-- Mehrere Zeilen auf einmal
INSERT INTO mitarbeiter (vorname, nachname, abteilung_id, gehalt, email)
VALUES
    ('Anna', 'Berger', 1, 55000, 'anna.berger@firma.de'),
    ('Tom', 'Fischer', 1, 47000, 'tom.fischer@firma.de');

-- Einfügen aus einer anderen Abfrage
INSERT INTO archiv_mitarbeiter (vorname, nachname)
SELECT vorname, nachname FROM mitarbeiter WHERE gehalt < 30000;
```

**Parameter/Varianten:**
| Element | Bedeutung |
|---|---|
| `(spaltenliste)` | Optional, aber empfohlen – legt fest, welche Spalten befüllt werden |
| `VALUES (...)` | Werte in derselben Reihenfolge wie die Spaltenliste |
| `INSERT ... SELECT` | Fügt Ergebnisse einer Abfrage ein |
| `ON DUPLICATE KEY UPDATE` (MySQL) | Aktualisiert bei Konflikt mit UNIQUE/PRIMARY KEY |
| `ON CONFLICT ... DO UPDATE` (PostgreSQL) | Gleiche Funktion wie oben |

```sql
INSERT INTO abteilungen (abteilung_id, name, standort)
VALUES (1, 'IT', 'Dresden')
ON DUPLICATE KEY UPDATE standort = VALUES(standort);
```

---

## 4. Daten ändern: UPDATE

```sql
UPDATE mitarbeiter
SET gehalt = gehalt * 1.05,
    abteilung_id = 3
WHERE mitarbeiter_id = 7;
```

**Parameter:**
| Element | Bedeutung |
|---|---|
| `SET` | Spalten und deren neue Werte (mehrere kommagetrennt) |
| `WHERE` | **Sehr wichtig!** Ohne `WHERE` werden alle Zeilen aktualisiert |
| `UPDATE ... JOIN` (MySQL) | Update über mehrere Tabellen hinweg |

```sql
-- Update mit JOIN
UPDATE mitarbeiter m
JOIN abteilungen a ON m.abteilung_id = a.abteilung_id
SET m.gehalt = m.gehalt * 1.03
WHERE a.standort = 'Chemnitz';
```

---

## 5. Daten löschen: DELETE / TRUNCATE

### `DELETE`

Löscht einzelne Zeilen anhand einer Bedingung (protokolliert, mit Rollback möglich).

```sql
DELETE FROM mitarbeiter
WHERE einstellungsdatum < '2015-01-01';
```

| Parameter | Bedeutung |
|---|---|
| `WHERE` | Bedingung – **ohne sie werden alle Zeilen gelöscht** |
| `LIMIT` (MySQL) | Begrenzt Anzahl gelöschter Zeilen |
| `ORDER BY ... LIMIT` | Kombination zum gezielten Löschen einzelner Zeilen |

### `TRUNCATE`

Löscht **alle** Zeilen einer Tabelle sehr schnell, setzt Auto-Increment zurück, ist aber i. d. R. nicht per `WHERE` einschränkbar und schwerer rückgängig zu machen.

```sql
TRUNCATE TABLE archiv_mitarbeiter;
```

> **Merksatz:** `DELETE` = gezielt, protokolliert, langsamer. `TRUNCATE` = alles auf einmal, sehr schnell, meist nicht rücksetzbar innerhalb einer laufenden Transaktion (DB-abhängig). `DROP` = löscht die Tabelle selbst inkl. Struktur.

---

## 6. Joins

Alle Beispiele verknüpfen `mitarbeiter` und `abteilungen`.

### `INNER JOIN`

Nur Zeilen, bei denen es in beiden Tabellen eine Übereinstimmung gibt.

```sql
SELECT m.vorname, m.nachname, a.name AS abteilung
FROM mitarbeiter m
INNER JOIN abteilungen a ON m.abteilung_id = a.abteilung_id;
```

### `LEFT JOIN` (LEFT OUTER JOIN)

Alle Zeilen aus der linken Tabelle, auch ohne Treffer rechts (dann `NULL`).

```sql
SELECT m.vorname, a.name AS abteilung
FROM mitarbeiter m
LEFT JOIN abteilungen a ON m.abteilung_id = a.abteilung_id;
```

### `RIGHT JOIN` (RIGHT OUTER JOIN)

Alle Zeilen aus der rechten Tabelle, auch ohne Treffer links.

```sql
SELECT a.name, m.vorname
FROM mitarbeiter m
RIGHT JOIN abteilungen a ON m.abteilung_id = a.abteilung_id;
```

### `FULL OUTER JOIN`

Alle Zeilen aus beiden Tabellen (kombiniert LEFT + RIGHT). *(In MySQL nicht direkt unterstützt, wird über `UNION` nachgebaut.)*

```sql
SELECT m.vorname, a.name
FROM mitarbeiter m
FULL OUTER JOIN abteilungen a ON m.abteilung_id = a.abteilung_id;
```

### `CROSS JOIN`

Kartesisches Produkt – jede Zeile mit jeder.

```sql
SELECT m.vorname, p.titel
FROM mitarbeiter m
CROSS JOIN projekte p;
```

### Self Join

Verknüpfung einer Tabelle mit sich selbst (z. B. Vorgesetzte).

```sql
SELECT e.vorname AS mitarbeiter, v.vorname AS vorgesetzter
FROM mitarbeiter e
LEFT JOIN mitarbeiter v ON e.vorgesetzter_id = v.mitarbeiter_id;
```

### Join über eine Zwischentabelle (Many-to-Many)

```sql
SELECT m.vorname, p.titel, mp.rolle
FROM mitarbeiter m
JOIN mitarbeiter_projekte mp ON m.mitarbeiter_id = mp.mitarbeiter_id
JOIN projekte p ON mp.projekt_id = p.projekt_id;
```

---

## 7. Indizes

Beschleunigen Lesezugriffe, verlangsamen aber Schreiboperationen.

```sql
-- Einfacher Index
CREATE INDEX idx_nachname ON mitarbeiter (nachname);

-- Eindeutiger Index
CREATE UNIQUE INDEX idx_email ON mitarbeiter (email);

-- Zusammengesetzter (composite) Index
CREATE INDEX idx_abteilung_gehalt ON mitarbeiter (abteilung_id, gehalt);

-- Index löschen
DROP INDEX idx_nachname ON mitarbeiter;   -- MySQL-Syntax
-- DROP INDEX idx_nachname;               -- PostgreSQL-Syntax
```

| Parameter | Bedeutung |
|---|---|
| `UNIQUE` | Erzwingt Eindeutigkeit der indizierten Werte |
| Mehrere Spalten | Reihenfolge beeinflusst, für welche Abfragen der Index nützlich ist |

---

## 8. Views

Eine View ist eine gespeicherte, virtuelle Abfrage.

```sql
CREATE VIEW gut_bezahlte_mitarbeiter AS
SELECT vorname, nachname, gehalt, abteilung_id
FROM mitarbeiter
WHERE gehalt > 60000;

-- Nutzung wie eine normale Tabelle
SELECT * FROM gut_bezahlte_mitarbeiter ORDER BY gehalt DESC;

-- View aktualisieren
CREATE OR REPLACE VIEW gut_bezahlte_mitarbeiter AS
SELECT vorname, nachname, gehalt FROM mitarbeiter WHERE gehalt > 65000;

-- View löschen
DROP VIEW gut_bezahlte_mitarbeiter;
```

---

## 9. Transaktionen (TCL)

Transaktionen fassen mehrere Befehle zu einer atomaren Einheit zusammen.

```sql
START TRANSACTION;   -- oder: BEGIN;

UPDATE abteilungen SET budget = budget - 10000 WHERE abteilung_id = 1;
UPDATE abteilungen SET budget = budget + 10000 WHERE abteilung_id = 2;

-- Bei Erfolg:
COMMIT;

-- Bei Fehler:
-- ROLLBACK;
```

**Befehle:**
| Befehl | Bedeutung |
|---|---|
| `START TRANSACTION` / `BEGIN` | Startet eine Transaktion |
| `COMMIT` | Speichert alle Änderungen dauerhaft |
| `ROLLBACK` | Macht alle Änderungen seit `BEGIN` rückgängig |
| `SAVEPOINT name` | Setzt einen Wiederherstellungspunkt innerhalb der Transaktion |
| `ROLLBACK TO SAVEPOINT name` | Rollt nur bis zu diesem Punkt zurück |
| `SET TRANSACTION ISOLATION LEVEL ...` | Legt das Isolationslevel fest (`READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`) |

```sql
START TRANSACTION;
UPDATE mitarbeiter SET gehalt = gehalt + 1000 WHERE mitarbeiter_id = 1;
SAVEPOINT nach_erhoehung;

UPDATE mitarbeiter SET gehalt = gehalt - 5000 WHERE mitarbeiter_id = 2;
ROLLBACK TO SAVEPOINT nach_erhoehung;

COMMIT;
```

---

## 10. Rechteverwaltung (DCL)

```sql
-- Rechte vergeben
GRANT SELECT, INSERT, UPDATE ON firma_db.mitarbeiter TO 'anna'@'localhost';

-- Alle Rechte auf eine Datenbank vergeben
GRANT ALL PRIVILEGES ON firma_db.* TO 'admin_user'@'localhost';

-- Rechte entziehen
REVOKE INSERT, UPDATE ON firma_db.mitarbeiter FROM 'anna'@'localhost';

-- Rechteänderungen wirksam machen
FLUSH PRIVILEGES;
```

| Parameter | Bedeutung |
|---|---|
| `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `ALL PRIVILEGES` | Art der Rechte |
| `ON db.tabelle` | Zielobjekt der Rechte (`*` = alle Tabellen) |
| `TO 'user'@'host'` | Empfänger der Rechte |
| `WITH GRANT OPTION` | Erlaubt dem Nutzer, Rechte selbst weiterzugeben |

---

## 11. Nützliche Zusatzfunktionen

### `CASE WHEN` – bedingte Logik in SELECT

```sql
SELECT vorname, gehalt,
    CASE
        WHEN gehalt >= 70000 THEN 'Hoch'
        WHEN gehalt >= 45000 THEN 'Mittel'
        ELSE 'Niedrig'
    END AS gehaltsklasse
FROM mitarbeiter;
```

### Fensterfunktionen (Window Functions)

```sql
SELECT vorname, abteilung_id, gehalt,
    RANK() OVER (PARTITION BY abteilung_id ORDER BY gehalt DESC) AS rang,
    AVG(gehalt) OVER (PARTITION BY abteilung_id) AS abteilungsdurchschnitt
FROM mitarbeiter;
```

| Element | Bedeutung |
|---|---|
| `OVER (...)` | Definiert das "Fenster" für die Berechnung |
| `PARTITION BY` | Teilt die Daten in Gruppen (ähnlich `GROUP BY`, aber ohne Zeilenreduktion) |
| `ORDER BY` (innerhalb `OVER`) | Sortierung innerhalb der Partition |
| `RANK()`, `ROW_NUMBER()`, `DENSE_RANK()` | Rangfunktionen |

### Common Table Expressions (CTE)

```sql
WITH abteilungsdurchschnitt AS (
    SELECT abteilung_id, AVG(gehalt) AS durchschnitt
    FROM mitarbeiter
    GROUP BY abteilung_id
)
SELECT m.vorname, m.gehalt, a.durchschnitt
FROM mitarbeiter m
JOIN abteilungsdurchschnitt a ON m.abteilung_id = a.abteilung_id
WHERE m.gehalt > a.durchschnitt;
```

---

## Kurzübersicht: Befehlskategorien

| Kategorie | Befehle |
|---|---|
| **DDL** (Data Definition Language) | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| **DML** (Data Manipulation Language) | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| **DCL** (Data Control Language) | `GRANT`, `REVOKE` |
| **TCL** (Transaction Control Language) | `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `START TRANSACTION` |

> **Hinweis:** Die genaue Syntax kann sich je nach Datenbanksystem (MySQL, PostgreSQL, SQL Server, Oracle, SQLite) leicht unterscheiden — insbesondere bei `LIMIT`/`TOP`/`FETCH`, `AUTO_INCREMENT`/`SERIAL`, und bei Groß-/Kleinschreibung von Identifikatoren. Die obigen Beispiele orientieren sich primär an der MySQL-Syntax mit Hinweisen auf Abweichungen.