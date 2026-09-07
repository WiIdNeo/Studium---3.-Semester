"""
Einfaches Beispiel-Skript zur Verbindung mit einer MariaDB-Datenbank.

Voraussetzung:
    pip install mariadb python-dotenv
    (Systempakete libmariadb3 / libmariadb-dev müssen installiert sein)

Zugangsdaten werden aus einer .env-Datei im selben Ordner gelesen.
Diese .env-Datei NIEMALS in Git committen (siehe .gitignore)!
"""

import os
import sys

import mariadb
from dotenv import load_dotenv

# Lädt die Variablen aus der .env-Datei ins Environment
load_dotenv()

# --- Verbindungsdaten aus Umgebungsvariablen ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# Prüfen, ob alle nötigen Werte vorhanden sind
if not all([DB_CONFIG["user"], DB_CONFIG["password"], DB_CONFIG["database"]]):
    print("Fehler: DB_USER, DB_PASSWORD oder DB_NAME fehlt in der .env-Datei.")
    sys.exit(1)


def get_connection():
    """Baut eine Verbindung zur MariaDB-Datenbank auf und gibt sie zurück."""
    try:
        conn = mariadb.connect(**DB_CONFIG)
        print("Verbindung zu MariaDB erfolgreich hergestellt.")
        return conn
    except mariadb.Error as e:
        print(f"Fehler beim Verbinden zu MariaDB: {e}")
        sys.exit(1)


def main():
    conn = get_connection()
    cursor = conn.cursor()

    # Beispiel-Query: einfache Testabfrage
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"MariaDB-Serverversion: {version[0]}")

    # Beispiel: eigene Abfrage ausführen
    # cursor.execute("SELECT * FROM meine_tabelle")
    # for row in cursor.fetchall():
    #     print(row)

    cursor.close()
    conn.close()
    print("Verbindung geschlossen.")


if __name__ == "__main__":
    main()