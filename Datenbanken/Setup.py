"""
Erstellt eine Testdatenbank für das Thema Studenten / Dozenten / Studiengänge.

Voraussetzung:
    pip install mariadb python-dotenv
    (Systempakete libmariadb3 / libmariadb-dev müssen installiert sein)

Nutzt die Zugangsdaten aus der .env-Datei (DB_HOST, DB_PORT, DB_USER, DB_PASSWORD).
DB_NAME wird hier fest auf "uni_testdb" gesetzt, kann aber unten angepasst werden.

Das Skript ist idempotent: bereits vorhandene Datenbank/Tabellen werden
gelöscht und neu angelegt, damit man es gefahrlos mehrfach ausführen kann.
"""

import os
import sys

import mariadb
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "uni_testdb"  # eigener Name für diese Testdatenbank

if not all([DB_USER, DB_PASSWORD]):
    print("Fehler: DB_USER oder DB_PASSWORD fehlt in der .env-Datei.")
    sys.exit(1)


def get_server_connection():
    """Verbindung zum MariaDB-Server (ohne konkrete Datenbank)."""
    try:
        return mariadb.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD
        )
    except mariadb.Error as e:
        print(f"Fehler beim Verbinden zu MariaDB: {e}")
        sys.exit(1)


def create_database(cursor):
    print(f"Erstelle Datenbank '{DB_NAME}' (falls nicht vorhanden) ...")
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cursor.execute(
        f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )


def create_tables(cursor):
    print("Erstelle Tabellen ...")

    cursor.execute(
        """
        CREATE TABLE studiengaenge (
            studiengang_id INT AUTO_INCREMENT PRIMARY KEY,
            name           VARCHAR(100) NOT NULL,
            abschluss      VARCHAR(20)  NOT NULL,
            regelstudienzeit_semester INT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE dozenten (
            dozent_id   INT AUTO_INCREMENT PRIMARY KEY,
            vorname     VARCHAR(50) NOT NULL,
            nachname    VARCHAR(50) NOT NULL,
            email       VARCHAR(100) UNIQUE NOT NULL,
            fachbereich VARCHAR(100)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE studenten (
            matrikelnummer   INT AUTO_INCREMENT PRIMARY KEY,
            vorname          VARCHAR(50) NOT NULL,
            nachname         VARCHAR(50) NOT NULL,
            email            VARCHAR(100) UNIQUE NOT NULL,
            studiengang_id   INT,
            einschreibedatum DATE NOT NULL,
            FOREIGN KEY (studiengang_id) REFERENCES studiengaenge(studiengang_id)
                ON DELETE SET NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE module (
            modul_id       INT AUTO_INCREMENT PRIMARY KEY,
            name           VARCHAR(100) NOT NULL,
            ects           INT NOT NULL,
            semester       INT NOT NULL,
            dozent_id      INT,
            studiengang_id INT,
            FOREIGN KEY (dozent_id) REFERENCES dozenten(dozent_id)
                ON DELETE SET NULL,
            FOREIGN KEY (studiengang_id) REFERENCES studiengaenge(studiengang_id)
                ON DELETE SET NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE pruefungen (
            pruefung_id    INT AUTO_INCREMENT PRIMARY KEY,
            matrikelnummer INT NOT NULL,
            modul_id       INT NOT NULL,
            note           DECIMAL(2,1) NOT NULL,
            pruefungsdatum DATE NOT NULL,
            FOREIGN KEY (matrikelnummer) REFERENCES studenten(matrikelnummer)
                ON DELETE CASCADE,
            FOREIGN KEY (modul_id) REFERENCES module(modul_id)
                ON DELETE CASCADE
        )
        """
    )


def insert_sample_data(cursor):
    print("Fülle Beispieldaten ein ...")

    cursor.executemany(
        "INSERT INTO studiengaenge (name, abschluss, regelstudienzeit_semester) "
        "VALUES (?, ?, ?)",
        [
            ("Informatik", "Bachelor", 6),
            ("Wirtschaftsinformatik", "Bachelor", 7),
            ("Data Science", "Master", 4),
        ],
    )

    cursor.executemany(
        "INSERT INTO dozenten (vorname, nachname, email, fachbereich) "
        "VALUES (?, ?, ?, ?)",
        [
            ("Anna", "Schneider", "a.schneider@hochschule.de", "Datenbanken"),
            ("Markus", "Weber", "m.weber@hochschule.de", "Softwaretechnik"),
            ("Lena", "Fischer", "l.fischer@hochschule.de", "Mathematik"),
        ],
    )

    cursor.executemany(
        "INSERT INTO studenten (vorname, nachname, email, studiengang_id, einschreibedatum) "
        "VALUES (?, ?, ?, ?, ?)",
        [
            ("Max", "Mustermann", "max.mustermann@stud.de", 1, "2023-10-01"),
            ("Julia", "Klein", "julia.klein@stud.de", 1, "2022-10-01"),
            ("Tim", "Becker", "tim.becker@stud.de", 2, "2023-10-01"),
            ("Sophie", "Wolf", "sophie.wolf@stud.de", 3, "2024-04-01"),
        ],
    )

    cursor.executemany(
        "INSERT INTO module (name, ects, semester, dozent_id, studiengang_id) "
        "VALUES (?, ?, ?, ?, ?)",
        [
            ("Datenbanksysteme", 5, 3, 1, 1),
            ("Softwareentwicklung 1", 6, 1, 2, 1),
            ("Lineare Algebra", 5, 1, 3, 1),
            ("Data Mining", 6, 2, 1, 3),
        ],
    )

    cursor.executemany(
        "INSERT INTO pruefungen (matrikelnummer, modul_id, note, pruefungsdatum) "
        "VALUES (?, ?, ?, ?)",
        [
            (1, 1, 2.3, "2024-02-15"),
            (1, 2, 1.7, "2023-02-10"),
            (2, 1, 1.3, "2023-02-15"),
            (3, 3, 2.7, "2024-02-20"),
            (4, 4, 1.0, "2024-07-15"),
        ],
    )


def main():
    conn = get_server_connection()
    cursor = conn.cursor()

    create_database(cursor)
    conn.commit()

    # Verbindung neu aufbauen, diesmal direkt mit der Ziel-Datenbank
    cursor.close()
    conn.close()

    conn = mariadb.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()

    create_tables(cursor)
    insert_sample_data(cursor)
    conn.commit()

    print(f"Fertig! Datenbank '{DB_NAME}' wurde erstellt und befüllt.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()