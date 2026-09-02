#!/usr/bin/env python3
"""
2_sql_befehle_erklaert.py
==========================

Dieses Skript zeigt und erklärt die wichtigsten SQL-Befehle für MariaDB,
jeweils zusammen mit der passenden Python-Syntax.

Voraussetzung:
    pip install mariadb

    (Das ist der offizielle MariaDB-Connector für Python. Alternativ
    funktioniert auch 'mysql-connector-python' fast identisch, da MariaDB
    protokollkompatibel zu MySQL ist.)

Grundprinzip in Python:
    1. Verbindung zum Server aufbauen  -> mariadb.connect(...)
    2. Cursor erzeugen                 -> conn.cursor()
    3. SQL-Befehl ausführen            -> cursor.execute(...)
    4. Ergebnisse abholen (bei SELECT) -> cursor.fetchall() / fetchone()
    5. Änderungen speichern            -> conn.commit()
    6. Verbindung schließen            -> conn.close()
"""

import mariadb


# ---------------------------------------------------------------------------
# 1. VERBINDUNG AUFBAUEN
# ---------------------------------------------------------------------------
def verbindung_aufbauen():
    """
    mariadb.connect() öffnet eine Verbindung zum Datenbankserver.

    Parameter:
    - user:     Datenbank-Benutzername
    - password: Passwort des Benutzers
    - host:     Adresse des Servers (z.B. 'localhost' oder '127.0.0.1')
    - port:     Port des Servers (Standard bei MariaDB: 3306)
    - database: Name der Datenbank, mit der man sich sofort verbinden will
                (optional, kann auch später mit USE gewechselt werden)
    """
    try:
        conn = mariadb.connect(
            user="mein_benutzer",
            password="mein_passwort",
            host="127.0.0.1",
            port=3306,
            database="meine_datenbank",
        )
        print("Verbindung erfolgreich hergestellt.")
        return conn
    except mariadb.Error as fehler:
        print(f"Fehler beim Verbindungsaufbau: {fehler}")
        raise


# ---------------------------------------------------------------------------
# 2. DATENBANK ERSTELLEN
# ---------------------------------------------------------------------------
def datenbank_erstellen(conn):
    """
    CREATE DATABASE erstellt eine neue Datenbank.

    - IF NOT EXISTS verhindert einen Fehler, falls die Datenbank
      bereits existiert.
    - cursor.execute() führt einen einzelnen SQL-Befehl als String aus.
    """
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS meine_datenbank")
    print("Datenbank 'meine_datenbank' erstellt (falls noch nicht vorhanden).")


# ---------------------------------------------------------------------------
# 3. TABELLE ERSTELLEN
# ---------------------------------------------------------------------------
def tabelle_erstellen(conn):
    """
    CREATE TABLE definiert die Struktur einer Tabelle.

    Erklärung der Spalten-Definitionen:
    - id INT AUTO_INCREMENT PRIMARY KEY:
        'id' ist eine Ganzzahl, wird automatisch hochgezählt (1, 2, 3, ...)
        und dient als eindeutiger Primärschlüssel (Primary Key), über den
        jede Zeile eindeutig identifiziert werden kann.
    - name VARCHAR(100) NOT NULL:
        Textfeld mit maximal 100 Zeichen, darf nicht leer (NULL) sein.
    - email VARCHAR(150) UNIQUE:
        Textfeld, das in der gesamten Tabelle nur einmal vorkommen darf.
    - alter INT:
        Ganzzahlfeld für das Alter.
    - erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP:
        Speichert automatisch das Datum/die Uhrzeit der Erstellung,
        falls kein Wert angegeben wird.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS benutzer (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE,
            alter_ INT,
            erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Hinweis: 'alter_' statt 'alter', da ALTER ein reserviertes SQL-Wort ist.
    print("Tabelle 'benutzer' erstellt (falls noch nicht vorhanden).")


# ---------------------------------------------------------------------------
# 4. DATEN EINFÜGEN (INSERT) MIT PARAMETERN
# ---------------------------------------------------------------------------
def daten_einfuegen(conn):
    """
    INSERT INTO fügt eine neue Zeile in eine Tabelle ein.

    WICHTIG - Parametrisierte Abfragen (Platzhalter '?'):
    Statt Werte direkt per String-Formatierung in den SQL-Befehl
    einzusetzen (z.B. f-Strings), verwendet man Platzhalter ('?').
    Die eigentlichen Werte werden als zweites Argument an execute()
    übergeben (als Tuple).

    Warum ist das wichtig?
    - Sicherheit: Verhindert SQL-Injection-Angriffe, bei denen
      bösartiger Code über Benutzereingaben eingeschleust wird.
    - Korrektheit: Der Treiber kümmert sich automatisch um korrektes
      Escaping von Sonderzeichen (z.B. Anführungszeichen in Namen).

    cursor.execute(sql, parameter) -> führt EINEN Datensatz ein.
    cursor.executemany(sql, liste) -> führt MEHRERE Datensätze auf
      einmal ein (effizienter als eine Schleife mit execute()).

    conn.commit(): Speichert die Änderungen dauerhaft in der Datenbank.
    Ohne commit() werden INSERT/UPDATE/DELETE-Änderungen bei Verbindungen
    mit Transaktionsunterstützung nicht endgültig übernommen.
    """
    cursor = conn.cursor()

    # Einzelnen Datensatz einfügen
    sql = "INSERT INTO benutzer (name, email, alter_) VALUES (?, ?, ?)"
    werte = ("Anna Muster", "anna@example.com", 29)
    cursor.execute(sql, werte)

    # Mehrere Datensätze auf einmal einfügen
    sql_mehrere = "INSERT INTO benutzer (name, email, alter_) VALUES (?, ?, ?)"
    mehrere_werte = [
        ("Max Beispiel", "max@example.com", 34),
        ("Lisa Test", "lisa@example.com", 22),
    ]
    cursor.executemany(sql_mehrere, mehrere_werte)

    conn.commit()
    print(f"{cursor.rowcount} Zeile(n) zuletzt eingefügt/verändert.")


# ---------------------------------------------------------------------------
# 5. DATEN ABFRAGEN (SELECT)
# ---------------------------------------------------------------------------
def daten_abfragen(conn):
    """
    SELECT liest Daten aus einer Tabelle.

    Bestandteile:
    - SELECT spalte1, spalte2   -> welche Spalten gewünscht sind
      SELECT *                 -> alle Spalten (nur zum Testen sinnvoll,
                                   in Produktion besser explizit angeben)
    - FROM tabelle              -> aus welcher Tabelle gelesen wird
    - WHERE bedingung           -> filtert Zeilen (z.B. alter_ > 25)
    - ORDER BY spalte [ASC|DESC] -> sortiert das Ergebnis
    - LIMIT n                   -> begrenzt die Anzahl zurückgegebener Zeilen

    Nach execute() liest man das Ergebnis mit:
    - cursor.fetchone()  -> genau eine Zeile (oder None)
    - cursor.fetchall()  -> alle Zeilen als Liste von Tuples
    - cursor.fetchmany(n) -> die nächsten n Zeilen
    """
    cursor = conn.cursor()

    sql = """
        SELECT id, name, email, alter_
        FROM benutzer
        WHERE alter_ > ?
        ORDER BY alter_ DESC
        LIMIT 10
    """
    cursor.execute(sql, (20,))  # Platzhalter '?' wird durch 20 ersetzt

    zeilen = cursor.fetchall()
    print("Gefundene Benutzer:")
    for zeile in zeilen:
        id_, name, email, alter_ = zeile
        print(f"  ID={id_}, Name={name}, Email={email}, Alter={alter_}")


# ---------------------------------------------------------------------------
# 6. DATEN AKTUALISIEREN (UPDATE)
# ---------------------------------------------------------------------------
def daten_aktualisieren(conn):
    """
    UPDATE ändert bestehende Zeilen.

    - SET spalte = neuer_wert   -> welche Spalte(n) geändert werden
    - WHERE bedingung           -> WICHTIG! Ohne WHERE werden ALLE
                                    Zeilen der Tabelle verändert.

    cursor.rowcount gibt an, wie viele Zeilen vom letzten Befehl
    betroffen waren.
    """
    cursor = conn.cursor()
    sql = "UPDATE benutzer SET alter_ = ? WHERE email = ?"
    cursor.execute(sql, (30, "anna@example.com"))
    conn.commit()
    print(f"{cursor.rowcount} Zeile(n) aktualisiert.")


# ---------------------------------------------------------------------------
# 7. DATEN LÖSCHEN (DELETE)
# ---------------------------------------------------------------------------
def daten_loeschen(conn):
    """
    DELETE FROM entfernt Zeilen aus einer Tabelle.

    - WHERE bedingung ist auch hier entscheidend: ohne WHERE werden
      ALLE Zeilen der Tabelle gelöscht (die Tabelle selbst bleibt
      aber bestehen, im Gegensatz zu DROP TABLE oder TRUNCATE TABLE).
    """
    cursor = conn.cursor()
    sql = "DELETE FROM benutzer WHERE email = ?"
    cursor.execute(sql, ("lisa@example.com",))
    conn.commit()
    print(f"{cursor.rowcount} Zeile(n) gelöscht.")


# ---------------------------------------------------------------------------
# 8. TABELLEN VERKNÜPFEN (JOIN) - BEISPIEL MIT ZWEITER TABELLE
# ---------------------------------------------------------------------------
def beispiel_join(conn):
    """
    JOIN verbindet Zeilen aus zwei (oder mehr) Tabellen anhand einer
    gemeinsamen Spalte.

    Hier: Jeder 'benutzer' kann mehrere 'bestellungen' haben. Verbunden
    wird über benutzer.id = bestellungen.benutzer_id.

    - INNER JOIN: nur Zeilen, bei denen es in BEIDEN Tabellen eine
      passende Verknüpfung gibt.
    - LEFT JOIN: alle Zeilen der linken Tabelle, auch wenn es in der
      rechten Tabelle keine Übereinstimmung gibt (dann NULL-Werte).
    """
    cursor = conn.cursor()

    # Zweite Tabelle für das Beispiel anlegen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bestellungen (
            id INT AUTO_INCREMENT PRIMARY KEY,
            benutzer_id INT,
            produkt VARCHAR(100),
            FOREIGN KEY (benutzer_id) REFERENCES benutzer(id)
        )
    """)

    sql = """
        SELECT benutzer.name, bestellungen.produkt
        FROM benutzer
        INNER JOIN bestellungen
            ON benutzer.id = bestellungen.benutzer_id
    """
    cursor.execute(sql)
    for name, produkt in cursor.fetchall():
        print(f"  {name} hat '{produkt}' bestellt.")


# ---------------------------------------------------------------------------
# 9. TABELLE / DATENBANK LÖSCHEN
# ---------------------------------------------------------------------------
def aufraeumen(conn):
    """
    DROP TABLE entfernt eine Tabelle inklusive aller Daten und der
    Struktur vollständig.

    DROP DATABASE entfernt eine ganze Datenbank inklusive aller
    enthaltenen Tabellen. Beides ist NICHT rückgängig zu machen -
    daher in echten Projekten mit äußerster Vorsicht verwenden!
    """
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS bestellungen")
    cursor.execute("DROP TABLE IF EXISTS benutzer")
    conn.commit()
    print("Tabellen wurden aufgeräumt (gelöscht).")


# ---------------------------------------------------------------------------
# HAUPTPROGRAMM
# ---------------------------------------------------------------------------
def main():
    conn = verbindung_aufbauen()
    try:
        datenbank_erstellen(conn)
        tabelle_erstellen(conn)
        daten_einfuegen(conn)
        daten_abfragen(conn)
        daten_aktualisieren(conn)
        beispiel_join(conn)
        daten_loeschen(conn)
        # aufraeumen(conn)  # Nur einkommentieren, wenn wirklich alles
        #                   # gelöscht werden soll.
    finally:
        # conn.close() sollte immer aufgerufen werden, um die
        # Verbindung ordentlich zu schließen - auch wenn ein Fehler
        # aufgetreten ist (deshalb 'finally').
        conn.close()
        print("Verbindung geschlossen.")


if __name__ == "__main__":
    main()
