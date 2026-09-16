# SQL-Übungen (TI25 CourseMgmt) – umgeschrieben & gelöst für MariaDB/MySQL

**Übungen 1–21 und 40–52** · Erklärt für absolute SQL-Einsteiger
Ursprünglich erstellt für Microsoft SQL Server 2022 (T-SQL) von Lutz Böttcher, DHSN Glauchau. Diese Version ist für **MariaDB (MySQL-Syntax)** umgeschrieben.

---

## Hinweis zur Vollständigkeit

In den hochgeladenen Dateien fehlen die **Übungen 22–39** komplett (kein Aufgabentext, keine Lösung). Für die **Übungen 1–21** lag eine offizielle MS-SQL-Musterlösung vor, die ich übersetzt habe. Für die **Übungen 40–52** lag **nur die Aufgabenstellung** vor (keine Lösung) – diese Lösungen habe ich selbst erstellt und kennzeichne alle Annahmen, die ich dabei treffen musste (z. B. wie ein Rabatt gespeichert ist).

---

## 1. Grundlagen, die du für alle Übungen brauchst

Bevor es losgeht, hier die wichtigsten Bausteine einer SQL-Abfrage. Auf diese Begriffe verweise ich später einfach zurück, statt sie jedes Mal neu zu erklären.

- **`SELECT spalte1, spalte2`** – legt fest, *welche Spalten* (Felder) im Ergebnis erscheinen sollen. `SELECT *` bedeutet "alle Spalten".
- **`FROM tabelle`** – legt fest, *aus welcher Tabelle* die Daten kommen.
- **Alias (`AS`)** – ein Alias ist ein Spitzname. `tbPeople p` gibt der Tabelle den Kurznamen `p`, damit man `p.person_LastName` statt `tbPeople.person_LastName` schreiben kann. `spalte AS Name` gibt einer *Spalte* im Ergebnis einen lesbaren Namen. Enthält der Alias Leerzeichen oder Sonderzeichen, muss er in Anführungszeichen/Backticks stehen.
- **`WHERE bedingung`** – filtert *Zeilen* (Datensätze), bevor sie ins Ergebnis kommen. Nur Zeilen, für die die Bedingung wahr ist, werden angezeigt.
- **`ORDER BY spalte ASC|DESC`** – sortiert das Ergebnis. `ASC` = aufsteigend (Standard, kann weggelassen werden), `DESC` = absteigend. Man kann auch mit einer *Positionsnummer* sortieren (`ORDER BY 2` = nach der 2. Spalte im SELECT).
- **`DISTINCT`** – entfernt doppelte Zeilen aus dem Ergebnis.
- **`LIKE` mit Platzhaltern** – `%` steht für "beliebig viele beliebige Zeichen" (auch keine), `_` für genau ein Zeichen. `'B%'` = beginnt mit B, `'%allee%'` = enthält "allee" irgendwo.
- **`AND` / `OR`** – verknüpfen mehrere Bedingungen in WHERE. `AND` verlangt, dass beide Seiten wahr sind, `OR` reicht eine Seite. Wichtig: `AND` bindet stärker als `OR` – deshalb bei gemischten Bedingungen **immer Klammern setzen**, sonst kommt oft ein falsches Ergebnis raus.
- **`JOIN` (genauer `INNER JOIN`)** – verbindet zwei Tabellen über eine gemeinsame Spalte (meist Primärschlüssel/Fremdschlüssel), z. B. `tbCourses.course2tbLecturer = tbLecturers.lecturer_Id`. Ohne JOIN stehen die Daten in getrennten Tabellen und man kann z. B. keinen Namen zu einem Kurs anzeigen, weil der Name in einer anderen Tabelle liegt.
- **`GROUP BY spalte`** – fasst Zeilen mit demselben Wert in dieser Spalte zu einer einzigen Ergebniszeile zusammen, meist kombiniert mit einer **Aggregatfunktion** wie `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`.
- **`UPDATE ... SET ... WHERE ...`** – ändert vorhandene Daten. Ohne WHERE würden **alle** Zeilen der Tabelle geändert – daher immer vorsichtig sein!
- **`CASE WHEN ... THEN ... ELSE ... END`** – ist ein "Wenn-Dann-Sonst" direkt in der SQL-Abfrage, ähnlich wie eine if-Anweisung in einer Programmiersprache.

---

## 2. Das Datenbankschema (vereinfacht, ohne DHSN-Schema)

MS SQL Server kennt drei Ebenen: `Datenbank.Schema.Tabelle` (hier: `TI25_CourseMgmt.DHSN.tbPeople`). **MariaDB/MySQL kennt diese Schema-Ebene nicht** – bei MySQL ist eine "Datenbank" gleichzeitig das, was in SQL Server "Schema" heißt. Deshalb fällt `DHSN` in allen Abfragen komplett weg, und wir arbeiten direkt mit der Datenbank, z. B.:

```sql
CREATE DATABASE IF NOT EXISTS ti25_coursemgmt;
USE ti25_coursemgmt;
```

Die (aus den Abfragen erschlossenen) Tabellen:

| Tabelle | Wichtige Spalten | Bedeutung |
|---|---|---|
| `tbPeople` | `person_Id`, `person_LastName`, `person_FirstName`, `person_Postcode`, `person_Location`, `person_Street`, `person_BirthDay` | Alle Personen (Teilnehmer *und* Dozenten) |
| `tbCourseSubjects` | `coursesub_Id`, `coursesub_Subject`, `coursesub_Description`, `coursesub_Duration` | Kursthemen (die "Vorlage", z. B. "SQL Grundlagen") |
| `tbCourses` | `course_Id`, `course_Identifier`, `course_DurationInHour`, `course_Price`, `course_Begin`, `course_End`, `course2tbCoursesub` (→ `tbCourseSubjects.coursesub_Id`), `course2tbLecturer` (→ `tbLecturers.lecturer_Id`) | Konkret stattfindende Kurse |
| `tbLecturers` | `lecturer_Id`, `lecturer_HourlyRate`, `lecturer2tbPeople` (→ `tbPeople.person_Id`) | Dozenten (Zusatzinfos zu einer Person) |
| `tbCourseAttendees` | `courseattendee2tbPeople` (→ `tbPeople.person_Id`), `courseattendee2tbCourse` (→ `tbCourses.course_Id`), `courseattendee_PaymentMethod`, `courseattendee_Discount`, `courseattendee_AmountPaid` | Wer nimmt an welchem Kurs teil, wie bezahlt |

Spalten mit dem Muster `xyz2tbAbc` sind **Fremdschlüssel** (Foreign Keys) – sie "zeigen" auf den Primärschlüssel (`_Id`) einer anderen Tabelle. Genau diese Spalten benutzt man in `ON ...` bei einem JOIN.

---

## 3. Wichtigste Unterschiede: T-SQL (MS SQL Server) vs. MariaDB/MySQL

Diese Tabelle erklärt, *warum* die Abfragen unten anders aussehen als im Original.

| Thema | MS SQL Server (T-SQL) | MariaDB / MySQL |
|---|---|---|
| Anzahl Zeilen begrenzen | `SELECT TOP 100 ...` (direkt nach SELECT) | `... LIMIT 100` (**am Ende** der Abfrage, nach ORDER BY) |
| Bezeichner (Tabellen-/Spaltennamen) klammern | `[Name]` in eckigen Klammern | `` `Name` `` in Backticks (nur nötig bei Sonderzeichen/Leerzeichen/reservierten Wörtern) |
| Text zusammenfügen | `'a' + 'b'` | `CONCAT('a','b')` – der `+`-Operator ist in MySQL eine **Zahlen-Addition**, keine Textverkettung! |
| Aktuelles Datum | `GETDATE()` | `NOW()` (Datum+Zeit) oder `CURDATE()` (nur Datum) |
| Datumsdifferenz | `DATEDIFF(Einheit, Start, Ende)` – 3 Argumente | `DATEDIFF(Ende, Start)` – nur 2 Argumente, liefert **immer Tage**. Für andere Einheiten: `TIMESTAMPDIFF(Einheit, Start, Ende)` |
| Datum verschieben | `DATEADD(Einheit, n, Datum)` | `DATE_ADD(Datum, INTERVAL n Einheit)` |
| NULL ersetzen | `ISNULL(x, ersatz)` | **Achtung, Falle:** `ISNULL(x)` existiert in MySQL auch, macht aber etwas anderes (prüft nur, ob x NULL ist, gibt 1/0 zurück)! Der Ersatz für T-SQLs `ISNULL(x,y)` heißt `IFNULL(x, y)` (oder `COALESCE(x, y)`, geht in beiden Systemen) |
| Aufrunden | `CEILING(x)` | `CEIL(x)` oder `CEILING(x)` – beide funktionieren |
| Standardabweichung | `STDEV(x)` | `STDDEV(x)` oder `STD(x)` |
| Anweisungen trennen | `GO` (Batch-Trenner) | gibt es nicht, einfach normales `;` verwenden und `GO` weglassen |
| Datenbank wählen | `USE [Name]` | `USE name;` |
| Schema-Ebene | `Datenbank.Schema.Tabelle` | keine Schema-Ebene – nur `Datenbank.Tabelle` oder direkt `Tabelle` |
| Text in Anführungszeichen | `"Text"` funktioniert oft als String | **Nur einfache Anführungszeichen** (`'Text'`) sind Strings! Doppelte Anführungszeichen (`"Text"`) sind standardmäßig ein Identifier-Escape (wie Backticks) – als String-Literal geht das nur mit einer Sondereinstellung (`ANSI_QUOTES`), auf die man sich nicht verlassen sollte |
| Zufallszahl `RAND()` | liefert **pro Abfrageaufruf** denselben Wert (für unterschiedliche Werte je Zeile braucht man Tricks) | liefert **pro Zeile** einen neuen Zufallswert – praktisch z. B. für Würfel-Simulationen |

---

## 4. Übungen 1–21 (mit Original-Lösung)

Zur Erinnerung: Zu Beginn jeder Sitzung steht implizit:

```sql
USE ti25_coursemgmt;
```

### Übung 1
**Aufgabe:** Es sind aus den Kursthemen alle Felder anzuzeigen.

**Original (T-SQL):**
```sql
SELECT * FROM TI25_CourseMgmt.DHSN.tbCourseSubjects
```

**MariaDB:**
```sql
SELECT * FROM tbCourseSubjects;
```

**Erklärung:** `SELECT *` heißt "zeig mir alle Spalten". Die dreistufige Adressierung `Datenbank.Schema.Tabelle` gibt es in MySQL nicht – nach dem `USE`-Befehl reicht der reine Tabellenname.

---

### Übung 2
**Aufgabe:** Thema, Beschreibung und Dauer aller Kursthemen, Tabellen-Alias `cs`, alle Feldnamen qualifiziert.

**Original (T-SQL):**
```sql
SELECT cs.coursesub_Subject, cs.coursesub_Description, cs.coursesub_Duration
FROM [DHSN].[tbCourseSubjects] cs;
```

**MariaDB:**
```sql
SELECT cs.coursesub_Subject, cs.coursesub_Description, cs.coursesub_Duration
FROM tbCourseSubjects cs;
```

**Erklärung:** `tbCourseSubjects cs` vergibt den Alias `cs`. "Qualifiziert" heißt: vor jeden Spaltennamen wird `cs.` geschrieben, damit klar ist, aus welcher Tabelle die Spalte stammt (wichtig, sobald mehrere Tabellen im Spiel sind).

---

### Übung 3
**Aufgabe:** Thema als "Thema", Beschreibung als "Beschreibung", Dauer als "Dauer geplant".

**Original (T-SQL):**
```sql
SELECT cs.coursesub_Subject AS Thema, cs.coursesub_Description AS Beschreibung, cs.coursesub_Duration AS "Dauer geplant"
FROM [DHSN].[tbCourseSubjects] cs;
```

**MariaDB:**
```sql
SELECT cs.coursesub_Subject AS Thema,
       cs.coursesub_Description AS Beschreibung,
       cs.coursesub_Duration AS `Dauer geplant`
FROM tbCourseSubjects cs;
```

**Erklärung:** Aliase ohne Leerzeichen (`Thema`, `Beschreibung`) brauchen keine Anführungszeichen. Sobald ein Leerzeichen im Alias vorkommt (`Dauer geplant`), muss er in MariaDB in **Backticks** stehen – doppelte Anführungszeichen würden hier nicht als Identifier erkannt.

---

### Übung 4
**Aufgabe:** Welche unterschiedlichen geplanten Kursdauern gibt es?

**Original (T-SQL):**
```sql
SELECT DISTINCT cs.coursesub_Duration AS "Dauer geplant"
FROM [DHSN].[tbCourseSubjects] cs;
```

**MariaDB:**
```sql
SELECT DISTINCT cs.coursesub_Duration AS `Dauer geplant`
FROM tbCourseSubjects cs;
```

**Erklärung:** `DISTINCT` entfernt doppelte Werte. Kommt z. B. die Dauer "60" in 20 Kursthemen vor, taucht sie im Ergebnis trotzdem nur **einmal** auf.

---

### Übung 5
**Aufgabe:** 100 Personen mit Familienname, Vorname, Geburtsdatum – jüngste zuerst.

**Original (T-SQL):**
```sql
SELECT TOP 100 p.person_LastName, p.person_FirstName ,p.person_BirthDay
FROM [DHSN].[tbPeople] p  ORDER BY p.person_BirthDay  DESC;
```

**MariaDB:**
```sql
SELECT p.person_LastName, p.person_FirstName, p.person_BirthDay
FROM tbPeople p
ORDER BY p.person_BirthDay DESC
LIMIT 100;
```

**Erklärung:** `TOP 100` gibt es in MySQL nicht – stattdessen steht `LIMIT 100` ganz am Ende der Abfrage, **nach** `ORDER BY`. `DESC` bei einem Datum sortiert die *größten* (= spätesten = jüngsten) Datumswerte zuerst, deshalb stehen die jüngsten Personen oben.

---

### Übung 6
**Aufgabe:** Beide Namen, PLZ, Ort, Straße – sortiert nach Ort, innerhalb des Orts aufsteigend.

**Original (T-SQL):**
```sql
SELECT  p.person_LastName, p.person_FirstName, p.person_Postcode, p.person_Location, p.person_Street
FROM [DHSN].[tbPeople] p
ORDER BY p.person_Location ASC, p.person_Postcode ASC;
```

**MariaDB:**
```sql
SELECT p.person_LastName, p.person_FirstName, p.person_Postcode, p.person_Location, p.person_Street
FROM tbPeople p
ORDER BY p.person_Location ASC, p.person_Postcode ASC;
```

**Erklärung:** Bei mehreren Sortierkriterien wird zuerst nach dem ersten Kriterium sortiert (`person_Location`), und nur innerhalb gleicher Orte wird das zweite Kriterium (`person_Postcode`) angewendet. Hier gab es keine T-SQL-spezifischen Elemente – das Original läuft unverändert in MariaDB.

---

### Übung 7
**Aufgabe:** Kursthema und Dauer, längste zuerst – kann der Alias zur Sortierung verwendet werden?

**Original (T-SQL):**
```sql
SELECT p.coursesub_Subject,p.[coursesub_Duration] AS "geplante Kursdauer"
FROM [DHSN].[tbCourseSubjects] p
ORDER BY "geplante Kursdauer" DESC
```

**MariaDB:**
```sql
SELECT cs.coursesub_Subject, cs.coursesub_Duration AS `geplante Kursdauer`
FROM tbCourseSubjects cs
ORDER BY `geplante Kursdauer` DESC;
```

*(Ich habe den Tabellen-Alias von `p` auf `cs` umbenannt, um ihn nicht mit `tbPeople` zu verwechseln – inhaltlich identisch zum Original.)*

**Erklärung:** Die Antwort auf die Frage in der Aufgabe: **Ja**, ein Spalten-Alias kann in `ORDER BY` verwendet werden (anders als in `WHERE`, dort funktioniert das nicht, weil `WHERE` vor der Benennung der Spalten ausgewertet wird). Da der Alias ein Leerzeichen enthält, muss er in Backticks stehen.

---

### Übung 8
**Aufgabe:** Alle Kursteilnehmer, alle Felder, zunächst aufsteigend nach Kurs-ID, innerhalb des Kurses so sortiert, dass die höchsten Rabatte oben stehen.

**Original (T-SQL):**
```sql
SELECT  *
FROM [DHSN].[tbCourseAttendees] ca
ORDER BY 2, 7,8 DESC;
```

**MariaDB:**
```sql
SELECT *
FROM tbCourseAttendees ca
ORDER BY 2, 7, 8 DESC;
```

**Erklärung:** `ORDER BY 2, 7, 8` sortiert nach der 2., 7. und 8. Spalte des Ergebnisses (Positionsnummern statt Namen) – das funktioniert in MariaDB genauso wie in T-SQL. **Wichtige Falle:** `DESC` bezieht sich hier **nur auf die letzte** angegebene Spalte (Nr. 8)! Die Spalten 2 und 7 werden trotzdem aufsteigend (`ASC`, Standard) sortiert. Wenn man mehrere Spalten absteigend sortieren möchte, muss man `DESC` bei jeder einzeln hinschreiben, z. B. `ORDER BY 2, 7 DESC, 8 DESC`.

---

### Übung 9
**Aufgabe:** Personen aus Glauchau: Nachname, Vorname, PLZ, Ort, Geburtsdatum.

**Original (T-SQL):**
```sql
SELECT p.person_LastName, p.person_FirstName,p.person_Postcode,p.person_Location,p.person_BirthDay
FROM [DHSN].[tbPeople] p
WHERE [person_Location] ='Glauchau'
```

**MariaDB:**
```sql
SELECT p.person_LastName, p.person_FirstName, p.person_Postcode, p.person_Location, p.person_BirthDay
FROM tbPeople p
WHERE p.person_Location = 'Glauchau';
```

**Erklärung:** `WHERE` filtert Zeilen. Nur Personen, bei denen `person_Location` exakt `'Glauchau'` ist, kommen ins Ergebnis. (Ich habe die Spalte im WHERE zusätzlich mit `p.` qualifiziert – guter Stil, auch wenn es hier, da nur eine Tabelle beteiligt ist, nicht zwingend nötig wäre.)

---

### Übung 10
**Aufgabe:** Personen aus Orten, die mit "B" beginnen – sortiert alphabetisch über die Positionsnummer.

**Original (T-SQL):**
```sql
SELECT  p.person_LastName, p.person_FirstName,p.person_Postcode,p.person_Location,p.person_BirthDay
FROM [DHSN].[tbPeople] p
WHERE [person_Location]  LIKE ('B%')
ORDER BY 4
```

**MariaDB:**
```sql
SELECT p.person_LastName, p.person_FirstName, p.person_Postcode, p.person_Location, p.person_BirthDay
FROM tbPeople p
WHERE p.person_Location LIKE 'B%'
ORDER BY 4;
```

**Erklärung:** `LIKE 'B%'` bedeutet: der Wert muss mit "B" beginnen, danach ist beliebig viel Text (`%`) erlaubt. `ORDER BY 4` sortiert nach der 4. Spalte im SELECT, das ist `person_Location`.

---

### Übung 11
**Aufgabe:** Personen mit PLZ < 25000 und Straße enthält "allee", sortiert nach PLZ aufsteigend, PLZ-Alias "kleiner 25000".

**Original (T-SQL):**
```sql
SELECT  p.person_LastName, p.person_FirstName,p.person_Postcode AS"kleiner 25000",p.person_Location,p.person_Street
FROM [DHSN].[tbPeople] p
WHERE p.person_Postcode < '25000'  AND p.person_Street LIKE '%allee%'
ORDER BY 3
```

**MariaDB:**
```sql
SELECT p.person_LastName, p.person_FirstName,
       p.person_Postcode AS `kleiner 25000`,
       p.person_Location, p.person_Street
FROM tbPeople p
WHERE p.person_Postcode < '25000'
  AND p.person_Street LIKE '%allee%'
ORDER BY 3;
```

**Erklärung:** `person_Postcode < '25000'` vergleicht hier **Text** (deshalb die Anführungszeichen um 25000) – das funktioniert nur zuverlässig, wenn alle PLZ gleich lang (5-stellig) gespeichert sind, da Textvergleiche zeichenweise erfolgen. `LIKE '%allee%'` findet "allee" an beliebiger Stelle im Straßennamen. Beide Bedingungen müssen mit `AND` gleichzeitig erfüllt sein.

---

### Übung 12
**Aufgabe:** Kursthemen, deren Beschreibung "SQL", "C++" oder "Datenbank" enthält und deren Dauer 60 oder 90 Stunden ist.

**Original (T-SQL):**
```sql
SELECT cs.coursesub_Subject
FROM [DHSN].[tbCourseSubjects] cs
WHERE (cs.coursesub_Description LIKE '%SQL%' OR cs.coursesub_Description LIKE'%C++%' OR cs.coursesub_Description LIKE '%Datenbank%') AND (cs.coursesub_Duration =60 OR cs.coursesub_Duration = 90)
```

**MariaDB:**
```sql
SELECT cs.coursesub_Subject
FROM tbCourseSubjects cs
WHERE (
        cs.coursesub_Description LIKE '%SQL%'
        OR cs.coursesub_Description LIKE '%C++%'
        OR cs.coursesub_Description LIKE '%Datenbank%'
      )
  AND (cs.coursesub_Duration = 60 OR cs.coursesub_Duration = 90);
```

**Erklärung:** Hier zeigt sich, warum Klammern bei gemischten `AND`/`OR` so wichtig sind: Ohne die Klammern um die drei `OR`-Bedingungen würde `AND` stärker binden und die Abfrage würde etwas anderes berechnen als gemeint. Mit Klammern liest sich das wie: "(SQL ODER C++ ODER Datenbank enthalten) UND (60 ODER 90 Stunden)".

---

### Übung 13
**Aufgabe:** Teilnehmer-ID, Zahlweise, Rabatt, Anzahlung – Kurs "GL05", die entweder per Gutschein zahlen oder mindestens 250 € angezahlt haben (wenn nicht Gutschein). Sortiert nach Anzahlung absteigend.

**Original (T-SQL):**
```sql
SELECT [courseattendee2tbPeople] , [courseattendee_PaymentMethod],[courseattendee_Discount] ,[courseattendee_AmountPaid]
FROM [DHSN].[tbCourseAttendees]
WHERE ( [courseattendee2tbCourse]= 'GL05') AND
    (([courseattendee_PaymentMethod] = 'Voucher') OR
    (([courseattendee_PaymentMethod] != 'Voucher') AND
    ([courseattendee_AmountPaid] >= 250.0)))
ORDER BY[courseattendee_AmountPaid]  DESC;
```

**MariaDB:**
```sql
SELECT courseattendee2tbPeople,
       courseattendee_PaymentMethod,
       courseattendee_Discount,
       courseattendee_AmountPaid
FROM tbCourseAttendees
WHERE courseattendee2tbCourse = 'GL05'
  AND (
        courseattendee_PaymentMethod = 'Voucher'
        OR (courseattendee_PaymentMethod <> 'Voucher'
            AND courseattendee_AmountPaid >= 250.0)
      )
ORDER BY courseattendee_AmountPaid DESC;
```

**Erklärung:** `!=` und `<>` bedeuten beide "ungleich" und funktionieren in MariaDB identisch – `<>` ist der SQL-Standard, `!=` eine weit verbreitete Erweiterung. Die verschachtelte Klammerlogik: Zeile passt, wenn (Kurs = GL05) UND (Gutschein ODER (nicht Gutschein UND ≥250€ angezahlt)).

---

### Übung 14
**Aufgabe:** Für alle Kurse: Kennung, Kursthema, geplante und tatsächliche Kursdauer – sinnvolle Aliase, sortiert nach Kurskennung.

**Original (T-SQL):**
```sql
SELECT c.course_Identifier AS "Kennung", cs.coursesub_Subject AS "Thema", c.course_DurationInHour "Tatsächliche Kursdauer", cs.coursesub_Duration  AS "Geplante Kursdauer"
FROM [DHSN].[tbCourses] c INNER JOIN [DHSN].[tbCourseSubjects] cs ON c.course2tbCoursesub = cs.coursesub_Id
ORDER BY c.course_Identifier ASC;
```

**MariaDB:**
```sql
SELECT c.course_Identifier AS Kennung,
       cs.coursesub_Subject AS Thema,
       c.course_DurationInHour AS `Tatsächliche Kursdauer`,
       cs.coursesub_Duration AS `Geplante Kursdauer`
FROM tbCourses c
INNER JOIN tbCourseSubjects cs ON c.course2tbCoursesub = cs.coursesub_Id
ORDER BY c.course_Identifier ASC;
```

**Erklärung – der erste JOIN, ausführlich:** `tbCourses` weiß nicht, wie das Kursthema heißt, sondern nur die ID (`course2tbCoursesub`). `tbCourseSubjects` hat den Klartext-Namen. Der `INNER JOIN ... ON c.course2tbCoursesub = cs.coursesub_Id` sagt: "verknüpfe jede Zeile aus `tbCourses` mit genau der Zeile aus `tbCourseSubjects`, deren `coursesub_Id` zur `course2tbCoursesub`-Nummer passt." Danach kann man aus beiden Tabellen gleichzeitig Spalten auswählen, als wären sie eine einzige Tabelle. `INNER JOIN` zeigt dabei nur Zeilen, für die es auf **beiden** Seiten einen Treffer gibt.

---

### Übung 15
**Aufgabe:** Alphabetische Liste aller Dozenten: Nachname, Vorname, PLZ, Ort, Stundensatz.

**Original (T-SQL):**
```sql
SELECT p.person_LastName, p.person_FirstName, p.person_Postcode, p.person_Location, l.lecturer_HourlyRate
FROM [DHSN].[tbLecturers] l INNER JOIN [DHSN].[tbPeople] p ON l.lecturer2tbPeople = p.person_Id
ORDER BY p.person_LastName ASC, p.person_FirstName ASC;
```

**MariaDB:**
```sql
SELECT p.person_LastName, p.person_FirstName, p.person_Postcode, p.person_Location, l.lecturer_HourlyRate
FROM tbLecturers l
INNER JOIN tbPeople p ON l.lecturer2tbPeople = p.person_Id
ORDER BY p.person_LastName ASC, p.person_FirstName ASC;
```

**Erklärung:** `tbLecturers` enthält nur dozentenspezifische Daten (Stundensatz), die persönlichen Daten (Name, Adresse) stehen in `tbPeople`. Der JOIN führt beides zusammen.

---

### Übung 16
**Aufgabe:** Für alle Dozenten: ID, Stundensatz, Kurskennung, Kursbeginn, Kursende der von ihnen geleiteten Kurse. Sortiert nach Kursbeginn.

**Original (T-SQL):**
```sql
SELECT l.lecturer_Id, l.lecturer_HourlyRate, c.course_Identifier, c.course_Begin, c.course_End
FROM  [DHSN].[tbLecturers] l INNER JOIN [DHSN].[tbCourses] c ON (l.lecturer_Id = c.course2tbLecturer)
ORDER BY c.course_Begin ASC;
```

**MariaDB:**
```sql
SELECT l.lecturer_Id, l.lecturer_HourlyRate, c.course_Identifier, c.course_Begin, c.course_End
FROM tbLecturers l
INNER JOIN tbCourses c ON l.lecturer_Id = c.course2tbLecturer
ORDER BY c.course_Begin ASC;
```

**Erklärung:** Diesmal wird `tbCourses` über den Fremdschlüssel `course2tbLecturer` mit `tbLecturers` verknüpft – Leserichtung ist egal, `A = B` ist dasselbe wie `B = A`.

---

### Übung 17
**Aufgabe:** Eindeutige Kursthemen, deren Beschreibung "Datenbank", "C++" oder "C#" enthält und die 60 Stunden dauern (tatsächliche Dauer).

**Original (T-SQL):**
```sql
SELECT /* DISTINCT*/ cs.coursesub_Subject
FROM [DHSN].[tbCourseSubjects] cs INNER JOIN  [DHSN].[tbCourses] c
    ON cs.coursesub_Id = c.course2tbCoursesub
WHERE (
    (cs.coursesub_Description LIKE '%Datenbank%') OR
    (cs.coursesub_Description LIKE '%C++%') OR
    (cs.coursesub_Description LIKE '%C#%') ) AND (c.course_DurationInHour = 60);
```

**MariaDB:**
```sql
SELECT DISTINCT cs.coursesub_Subject
FROM tbCourseSubjects cs
INNER JOIN tbCourses c ON cs.coursesub_Id = c.course2tbCoursesub
WHERE (
        cs.coursesub_Description LIKE '%Datenbank%'
        OR cs.coursesub_Description LIKE '%C++%'
        OR cs.coursesub_Description LIKE '%C#%'
      )
  AND c.course_DurationInHour = 60;
```

**Erklärung:** Im Original war `DISTINCT` auskommentiert – die Aufgabe verlangt aber ausdrücklich "eindeutige" Kursthemen, deshalb habe ich `DISTINCT` aktiviert. Ohne `DISTINCT` würde ein Kursthema mehrfach erscheinen, wenn es mehrere passende Kurstermine mit 60 Stunden dazu gibt.

---

### Übung 18
**Aufgabe:** Eindeutig sortierte Liste (Nachname, Vorname) aller Teilnehmer, die an einem Kurs zum Thema "C++" teilnehmen.

**Original (T-SQL, zwei gleichwertige Varianten im Original):**
```sql
SELECT /*DISTINCT*/ p.person_LastName AS Familienname, p.person_FirstName AS Vorname
FROM [DHSN].[tbPeople] p
            INNER JOIN  [DHSN].[tbCourseAttendees] ca
            ON p.person_Id= ca.courseattendee2tbPeople
            INNER JOIN [DHSN].[tbCourses] c
            ON ca.courseattendee2tbCourse= c.course_Id
            INNER JOIN [DHSN].[tbCourseSubjects] cs
            ON cs.coursesub_Id= c.course2tbCoursesub
WHERE cs.coursesub_Description LIKE '%C++%'
ORDER BY Familienname ASC, Vorname ASC;
```

**MariaDB:**
```sql
SELECT DISTINCT p.person_LastName AS Familienname, p.person_FirstName AS Vorname
FROM tbPeople p
INNER JOIN tbCourseAttendees ca ON p.person_Id = ca.courseattendee2tbPeople
INNER JOIN tbCourses c ON ca.courseattendee2tbCourse = c.course_Id
INNER JOIN tbCourseSubjects cs ON cs.coursesub_Id = c.course2tbCoursesub
WHERE cs.coursesub_Description LIKE '%C++%'
ORDER BY Familienname ASC, Vorname ASC;
```

**Erklärung – Verkettung mehrerer JOINs:** Um von einer Person zum Kursthema zu kommen, müssen **drei** Tabellen nacheinander verbunden werden: Person → Teilnahme (`tbCourseAttendees`) → Kurs (`tbCourses`) → Kursthema (`tbCourseSubjects`). Jeder `JOIN` fügt eine weitere Tabelle "an die Kette". Auch hier wieder `DISTINCT`, weil die Aufgabe "eindeutig" verlangt – sonst würde eine Person mehrfach erscheinen, wenn sie mehrere C++-Kurse besucht.

---

### Übung 19
**Aufgabe:** Für alle Lehrkräfte: Nachname, Vorname, Stundensatz und Gebühr der aktuell betreuten Kurse.

**Original (T-SQL):**
```sql
SELECT p.person_LastName, p.person_FirstName, l.lecturer_HourlyRate, c.course_Price
FROM [DHSN].[tbPeople] p
    INNER JOIN [DHSN].[tbLecturers] l
    INNER JOIN [DHSN].[tbCourses] c
    ON c.course2tbLecturer= l.lecturer_Id
    ON l.lecturer2tbPeople = p.person_Id;
```

**MariaDB:**
```sql
SELECT p.person_LastName, p.person_FirstName, l.lecturer_HourlyRate, c.course_Price
FROM tbPeople p
INNER JOIN tbLecturers l ON l.lecturer2tbPeople = p.person_Id
INNER JOIN tbCourses c ON c.course2tbLecturer = l.lecturer_Id;
```

**Erklärung:** Inhaltlich identisch zum Original, nur habe ich die `ON`-Klauseln direkt hinter das jeweilige `JOIN` geschrieben (in T-SQL stehen sie am Ende in umgekehrter Reihenfolge, was funktioniert, aber schwerer zu lesen ist). Lesart: Person → Dozent (über `lecturer2tbPeople`) → Kurse dieses Dozenten (über `course2tbLecturer`).

---

### Übung 20
**Aufgabe:** Zu jedem Kursthema die leitenden Dozenten: Thema, Kurskennung, Nachname, Vorname – sortiert nach Nachname.

**Original (T-SQL):**
```sql
SELECT cs.coursesub_Subject, c.course_Identifier,p.person_LastName, p.person_FirstName
FROM  [DHSN].[tbPeople] p
    INNER JOIN [DHSN].[tbLecturers] l
    INNER JOIN [DHSN].[tbCourses] c
    INNER JOIN [DHSN].[tbCourseSubjects] cs
    ON cs.coursesub_Id = c.course2tbCoursesub
    ON c.course2tbLecturer= l.lecturer_Id
    ON p.person_Id= l.lecturer2tbPeople
ORDER BY p.person_LastName
```

**MariaDB:**
```sql
SELECT cs.coursesub_Subject, c.course_Identifier, p.person_LastName, p.person_FirstName
FROM tbPeople p
INNER JOIN tbLecturers l ON p.person_Id = l.lecturer2tbPeople
INNER JOIN tbCourses c ON c.course2tbLecturer = l.lecturer_Id
INNER JOIN tbCourseSubjects cs ON cs.coursesub_Id = c.course2tbCoursesub
ORDER BY p.person_LastName;
```

**Erklärung:** Vier Tabellen in einer Kette: Person → Dozent → Kurs → Kursthema. Auch hier habe ich nur die Reihenfolge der `ON`-Bedingungen an die jeweiligen JOINs angepasst (inhaltlich gleich, aber leichter nachzuvollziehen als T-SQLs Variante mit den `ON`-Zeilen am Schluss).

---

### Übung 21
**Aufgabe:** Personen, die gleichzeitig Kursteilnehmer *und* Dozent (in irgendeinem Kurs) sind.

**Original (T-SQL, unvollständig/auskommentiert im Quellfile):**
```sql
SELECT DISTINCT p.person_LastName, p.person_FirstName
FROM [DHSN].[tbPeople] p
    INNER JOIN [DHSN].[tbCourseAttendees] ca
    ON p.person_Id=ca.courseattendee2tbPeople
    INNER JOIN [DHSN].[tbLecturers] l
    ON l.lecturer2tbPeople = p.person_Id
    --AND  l.lecturer2tbPeople = ca.courseattendee2tbPeople
--WHERE l.lecturer2tbPeople = ca.courseattendee2tbPeople
GO
```

**MariaDB (vervollständigt):**
```sql
SELECT DISTINCT p.person_LastName, p.person_FirstName
FROM tbPeople p
INNER JOIN tbCourseAttendees ca ON p.person_Id = ca.courseattendee2tbPeople
INNER JOIN tbLecturers l ON p.person_Id = l.lecturer2tbPeople;
```

**Erklärung:** Die im Original auskommentierten Zeilen deuten darauf hin, dass hier zunächst experimentiert wurde. Die korrekte, fertige Abfrage braucht keine zusätzliche Bedingung: Eine Person landet automatisch nur dann im Ergebnis, wenn ihre `person_Id` **sowohl** in `tbCourseAttendees` (als Teilnehmer) **als auch** in `tbLecturers` (als Dozent) vorkommt – denn ein `INNER JOIN` liefert nur Zeilen, bei denen auf beiden Seiten ein Treffer existiert. `DISTINCT` verhindert, dass eine Person mehrfach erscheint, falls sie mehrere Kurse besucht oder leitet.

---

## 5. Übungen 40–52 (eigene Lösung – im Original nur Aufgabentext)

Für diese Übungen gab es **keine Musterlösung** in deinen Dateien. Ich habe sie anhand der Aufgabenstellung und des oben beschriebenen Schemas selbst gelöst und dabei getroffene **Annahmen ausdrücklich markiert**, damit du sie mit deinem Dozenten abgleichen kannst.

### Übung 40
**Aufgabe:** Übersicht über alle Kursbesuche mit Teilnehmer-ID, Kursgebühr und Rabatt, zusätzlich eine berechnete Spalte "Reduzierte Gebühr" (Betrag abzüglich Rabatt).

> **Annahme:** `courseattendee_Discount` ist eine **Prozentzahl** (z. B. `10` = 10 % Rabatt).

```sql
SELECT ca.courseattendee2tbPeople AS Kursteilnehmer_ID,
       c.course_Price AS Kursgebuehr,
       ca.courseattendee_Discount AS Rabatt,
       ROUND(c.course_Price - (c.course_Price * ca.courseattendee_Discount / 100), 2) AS `Reduzierte Gebühr`
FROM tbCourseAttendees ca
INNER JOIN tbCourses c ON ca.courseattendee2tbCourse = c.course_Id;
```

**Erklärung:** In `SELECT` kann man rechnen, nicht nur Spalten anzeigen. `Kursgebühr * Rabatt / 100` berechnet den Rabattbetrag, den man von der vollen Gebühr abzieht. `ROUND(x, 2)` rundet auf 2 Nachkommastellen (Cent-genau).

---

### Übung 41
**Aufgabe:** Für alle Kurse: Gebühr, Dozentenkosten, benötigte Teilnehmerzahl zur Kostendeckung (Dozentenkosten werden verdoppelt, da nochmal derselbe Betrag für "sonstige Kosten" anfällt). Teilnehmerzahl aufgerundet.

> **Annahme:** Dozentenkosten = Stundensatz × tatsächliche Kursdauer in Stunden.

```sql
SELECT c.course_Id,
       c.course_Price AS Kursgebuehr,
       (l.lecturer_HourlyRate * c.course_DurationInHour) AS Dozentenkosten,
       CEIL((l.lecturer_HourlyRate * c.course_DurationInHour * 2) / c.course_Price) AS `Benötigte Teilnehmer`
FROM tbCourses c
INNER JOIN tbLecturers l ON c.course2tbLecturer = l.lecturer_Id;
```

**Erklärung:** `CEIL()` (in MS SQL Server hieße die Funktion `CEILING()`, in MariaDB gehen **beide** Namen) rundet immer **auf**, nie ab – genau das braucht man, wenn "3,2 Teilnehmer" in Wahrheit "mindestens 4 Teilnehmer" bedeutet.

---

### Übung 42
**Aufgabe:** Für die Kursthemen-ID: Exponentialfunktion sowie Quadratwurzelfunktion.

```sql
SELECT coursesub_Id,
       EXP(coursesub_Id) AS Exponentialfunktion,
       SQRT(coursesub_Id) AS Quadratwurzel
FROM tbCourseSubjects;
```

**Erklärung:** `EXP(x)` berechnet e^x, `SQRT(x)` die Quadratwurzel von x. Beide Funktionen heißen in MariaDB genauso wie in T-SQL – hier gibt es keinen Unterschied.

---

### Übung 43
**Aufgabe:** Mit den Kursthemen 16 mal "würfeln" (Zufallszahl 1–6).

```sql
SELECT coursesub_Id,
       FLOOR(RAND() * 6) + 1 AS Wuerfelwurf
FROM tbCourseSubjects
LIMIT 16;
```

**Erklärung:** `RAND()` liefert eine Zufallszahl zwischen 0 (inklusive) und 1 (exklusive). Multipliziert man mit 6, bekommt man einen Wert zwischen 0 und knapp unter 6. `FLOOR()` schneidet die Nachkommastellen ab (rundet ab) → Werte 0 bis 5. `+ 1` verschiebt den Bereich auf 1 bis 6. **Wichtig laut Cheatsheet oben:** In MariaDB liefert `RAND()` bei jeder Zeile einen neuen Zufallswert – deshalb reicht `LIMIT 16`, um 16 verschiedene "Würfe" zu bekommen. In MS SQL Server müsste man dafür tricksen (z. B. `RAND(CHECKSUM(NEWID()))`), weil `RAND()` dort sonst pro Abfrage nur einmal berechnet wird.

---

### Übung 44
**Aufgabe:** Neuer numerischer Schlüssel: ASCII-Code des ersten Zeichens der Kurs-ID, multipliziert mit einer Zufallszahl, gerundet auf eine ganze Zahl.

```sql
SELECT course_Id,
       course_Identifier,
       ROUND(ASCII(LEFT(course_Identifier, 1)) * RAND()) AS `Neuer Schlüssel`
FROM tbCourses;
```

**Erklärung:** `LEFT(text, 1)` liefert das erste Zeichen eines Textes. `ASCII(zeichen)` wandelt ein einzelnes Zeichen in seinen Zahlencode um (z. B. 'A' → 65). Multipliziert mit `RAND()` (Zufallszahl zwischen 0 und 1) und mit `ROUND()` ohne zweites Argument wird auf die nächste ganze Zahl gerundet (0 Nachkommastellen ist der Standard).

---

### Übung 45
**Aufgabe:** Kurs "DE-DB2" → "DE-DB3" umbenennen, Kursthema "Datenbank II" → "Datenbank MariaDB", in der Beschreibung "SQL Server 2022" durch "Maria DB" ersetzen. Danach Ausgabe: Kurskennung, Kursthema, Beschreibung, Kursbeginn, Kursende, Dauer mit Zusatz "xxxx Stunden".

```sql
-- Schritt 1: Kurskennung ändern
UPDATE tbCourses
SET course_Identifier = 'DE-DB3'
WHERE course_Identifier = 'DE-DB2';

-- Schritt 2: Kursthema umbenennen
UPDATE tbCourseSubjects
SET coursesub_Subject = 'Datenbank MariaDB'
WHERE coursesub_Subject = 'Datenbank II';

-- Schritt 3: Teilstring in der Beschreibung ersetzen
UPDATE tbCourseSubjects
SET coursesub_Description = REPLACE(coursesub_Description, 'SQL Server 2022', 'Maria DB');

-- Schritt 4: Ergebnis anzeigen
SELECT c.course_Identifier AS Kurskennung,
       cs.coursesub_Subject AS Kursthema,
       cs.coursesub_Description AS `Kursthema Beschreibung`,
       c.course_Begin AS Kursbeginn,
       c.course_End AS Kursende,
       CONCAT(cs.coursesub_Duration, ' Stunden') AS Dauer
FROM tbCourses c
INNER JOIN tbCourseSubjects cs ON c.course2tbCoursesub = cs.coursesub_Id;
```

**Erklärung:** `UPDATE tabelle SET spalte = neuerWert WHERE bedingung` ändert bestehende Zeilen. **Ohne** `WHERE` würden alle Zeilen der Tabelle geändert – deshalb hier unbedingt die Bedingung nicht vergessen! `REPLACE(text, gesucht, ersatz)` sucht innerhalb eines Textes nach einem Teilstring und ersetzt ihn (funktioniert in T-SQL und MariaDB identisch). Für "Dauer + Stunden" wird **nicht** `+` benutzt (das würde MySQL als Zahlen-Addition interpretieren und einen Fehler werfen, da 'Stunden' keine Zahl ist), sondern `CONCAT()`.

---

### Übung 46
**Aufgabe:** Kurse mit Kennung "GL" umbenennen: statt "GL" soll "DHSN" in der Kennung stehen, ergänzt um den Kursbeginn.

```sql
UPDATE tbCourses
SET course_Identifier = CONCAT(REPLACE(course_Identifier, 'GL', 'DHSN'), '-', course_Begin)
WHERE course_Identifier LIKE 'GL%';
```

**Erklärung:** `REPLACE(course_Identifier, 'GL', 'DHSN')` tauscht "GL" gegen "DHSN". `CONCAT(..., '-', course_Begin)` hängt anschließend einen Bindestrich und das Kursbeginn-Datum an – `CONCAT()` wandelt das Datum dabei automatisch in Text um. Die `WHERE`-Zeile sorgt dafür, dass **nur** Kurse geändert werden, deren Kennung mit "GL" beginnt.

---

### Übung 47
**Aufgabe:** Für alle umsatzsteuerpflichtigen Kurse zusätzlich zum Nettopreis die Umsatzsteuer (19 %) und den Bruttopreis anzeigen.

> **Annahme:** Es gibt in den vorliegenden Daten kein erkennbares Merkmal "umsatzsteuerpflichtig ja/nein" (keine entsprechende Spalte in `tbCourses` sichtbar) – ich berechne die Werte daher für **alle** Kurse. Falls es in deiner Datenbank tatsächlich eine Spalte wie `course_TaxLiable` gibt, ergänze die Zeile `WHERE course_TaxLiable = 1`.

```sql
SELECT course_Id,
       course_Price AS Nettopreis,
       ROUND(course_Price * 0.19, 2) AS Umsatzsteuer,
       ROUND(course_Price * 1.19, 2) AS Bruttopreis
FROM tbCourses;
```

**Erklärung:** Umsatzsteuer = Nettopreis × 19 %. Bruttopreis = Nettopreis + Umsatzsteuer, was man abkürzend als Nettopreis × 1,19 schreiben kann.

---

### Übung 48
**Aufgabe:** Vor- und Nachname aller Personen, dazu Geburtsmonat und -tag, sortiert nach Monat und Tag aufsteigend.

```sql
SELECT person_FirstName, person_LastName,
       MONTH(person_BirthDay) AS Geburtsmonat,
       DAY(person_BirthDay) AS Tag
FROM tbPeople
ORDER BY Geburtsmonat ASC, Tag ASC;
```

**Erklärung:** `MONTH(datum)` und `DAY(datum)` extrahieren den Monat bzw. Tag aus einem Datumswert – diese Funktionen heißen in T-SQL und MariaDB gleich. Die Sortierung nach Monat und dann Tag ergibt eine Art "Geburtstagskalender".

---

### Übung 49
**Aufgabe:** Für alle Personen mit bekanntem Geburtsdatum, die noch **diesen Monat** Geburtstag haben: Nachname, Vorname, aktuelles Datum, Geburtsdatum, Anzahl Tage bis zum Geburtstag.

```sql
SELECT person_LastName, person_FirstName,
       CURDATE() AS Heute,
       person_BirthDay AS Geburtsdatum,
       DATEDIFF(
         DATE(CONCAT(YEAR(CURDATE()), '-', MONTH(person_BirthDay), '-', DAY(person_BirthDay))),
         CURDATE()
       ) AS `Tage bis Geburtstag`
FROM tbPeople
WHERE person_BirthDay IS NOT NULL
  AND MONTH(person_BirthDay) = MONTH(CURDATE())
  AND DAY(person_BirthDay) >= DAY(CURDATE());
```

**Erklärung:** Das ist die komplexeste Übung bisher, Schritt für Schritt:
1. `CONCAT(YEAR(CURDATE()), '-', MONTH(person_BirthDay), '-', DAY(person_BirthDay))` baut einen Text wie `"2026-9-15"` – also das Geburtsdatum, aber mit dem **aktuellen** Jahr.
2. `DATE(...)` wandelt diesen Text in einen echten Datumswert um.
3. `DATEDIFF(dieses_jahr_geburtstag, CURDATE())` berechnet die Differenz in Tagen. **Achtung, wichtiger Unterschied zu T-SQL:** In MariaDB/MySQL hat `DATEDIFF()` nur **zwei** Argumente (`DATEDIFF(spätesDatum, frühesDatum)`) und liefert immer die Differenz in Tagen. In T-SQL bräuchte man `DATEDIFF(day, startdatum, enddatum)` mit drei Argumenten.
4. Die `WHERE`-Zeile filtert auf Personen mit bekanntem Geburtsdatum, deren Geburtsmonat dem aktuellen Monat entspricht und deren Tag noch nicht überschritten ist.

---

### Übung 50
**Aufgabe:** Kurslänge in Tagen für alle Kurse.

```sql
SELECT course_Id, course_Identifier,
       DATEDIFF(course_End, course_Begin) AS `Kurslänge in Tagen`
FROM tbCourses;
```

**Erklärung:** `DATEDIFF(Ende, Anfang)` liefert die Anzahl Tage zwischen zwei Daten. In T-SQL müsste man hierfür `DATEDIFF(day, course_Begin, course_End)` schreiben (mit Einheit als erstem Argument und Start vor Ende) – die Reihenfolge der Argumente ist also genau vertauscht, das ist eine typische Stolperfalle beim Umsteigen.

---

### Übung 51
**Aufgabe:** Für jede Person: hat sie im aktuellen Jahr schon Geburtstag gehabt ("Ja"/"nein")? Geburtsdatum und aktuelles Datum mit ausgeben. Personen ohne Vornamen bekommen ein Leerzeichen statt eines leeren Feldes.

```sql
SELECT person_LastName,
       IFNULL(NULLIF(person_FirstName, ''), ' ') AS Vorname,
       person_BirthDay AS Geburtsdatum,
       CURDATE() AS Heute,
       CASE
         WHEN DATE(CONCAT(YEAR(CURDATE()), '-', MONTH(person_BirthDay), '-', DAY(person_BirthDay))) <= CURDATE()
         THEN 'Ja'
         ELSE 'nein'
       END AS `Geburtstag gehabt`
FROM tbPeople;
```

**Erklärung:**
- `CASE WHEN bedingung THEN 'Ja' ELSE 'nein' END` ist ein Wenn-Dann-Sonst direkt in SQL: Ist die diesjährige "Kopie" des Geburtstags bereits vorbei oder heute, kommt "Ja" raus, sonst "nein".
- `NULLIF(person_FirstName, '')` gibt `NULL` zurück, falls der Vorname ein leerer Text `''` ist (sonst den Vornamen selbst).
- `IFNULL(x, ' ')` ersetzt danach ein `NULL` (egal ob ursprünglich `NULL` in der Datenbank oder gerade durch `NULLIF` erzeugt) durch ein einzelnes Leerzeichen `' '`. **Falle beim Umstieg:** In T-SQL heißt diese Ersatz-Funktion `ISNULL(x, ersatzwert)`. `ISNULL` gibt es in MariaDB zwar auch, sie tut dort aber etwas komplett anderes (sie prüft nur, ob `x` NULL ist und liefert `1` oder `0`) – der korrekte Ersatz ist `IFNULL()` (oder `COALESCE()`, die in beiden Systemen gleich funktioniert).

---

### Übung 52
**Aufgabe:** Wie viele Kursteilnehmer zahlen mit Gutschein, Bar oder per Überweisung? Sortiert nach Häufigkeit absteigend.

```sql
SELECT courseattendee_PaymentMethod AS Zahlweise,
       COUNT(*) AS Anzahl
FROM tbCourseAttendees
GROUP BY courseattendee_PaymentMethod
ORDER BY Anzahl DESC;
```

**Erklärung – GROUP BY zum ersten Mal ausführlich:** `GROUP BY courseattendee_PaymentMethod` fasst alle Zeilen mit demselben Wert in dieser Spalte (z. B. alle "Voucher"-Zeilen) zu **einer** Ergebniszeile zusammen. `COUNT(*)` zählt dabei, wie viele einzelne Zeilen in jeder Gruppe zusammengefasst wurden – hier also: wie viele Teilnehmer diese Zahlweise gewählt haben. `ORDER BY Anzahl DESC` sortiert die Zahlweisen danach, welche am häufigsten vorkommt.

---

## 6. Kurz-Zusammenfassung

- Alle Original-T-SQL-Elemente wurden ersetzt: `TOP` → `LIMIT`, `[..]` → `` ` .. ` `` / entfernt, `GO` entfernt, 3-Ebenen-Namen (`DB.Schema.Tabelle`) → 2-Ebenen (`DB.Tabelle`), `DATEDIFF`/`ISNULL`/String-Verkettung an die MySQL-Syntax angepasst.
- Übungen 22–39 fehlen in deinen Unterlagen – wenn du sie nachreichst (z. B. als Foto/PDF vom Dozenten), kann ich sie in derselben Struktur ergänzen.
- Für Übungen 40–52 habe ich eigene Lösungen erstellt, da keine Musterlösung vorlag – markierte Annahmen (z. B. Rabatt als Prozentwert) unbedingt mit dem tatsächlichen Tabellenschema/Dozenten abgleichen.