#!/usr/bin/env python3
"""
1_mariadb_server_starten.py
============================

Dieses Skript startet einen lokal installierten MariaDB-Server über Python.

WICHTIG:
- MariaDB muss bereits auf dem System installiert sein (z.B. via
  `sudo apt install mariadb-server` unter Debian/Ubuntu oder
  `sudo dnf install mariadb-server` unter Fedora/CentOS).
- Python startet hier NICHT MariaDB "von Grund auf", sondern ruft im
  Hintergrund den System-Dienst bzw. den mysqld-Prozess auf.
- Je nach Betriebssystem/Distribution kann der Befehl zum Starten
  variieren (systemctl, service, mysqld_safe, brew services, etc.).
  Unten sind die gängigsten Varianten enthalten.
"""

import subprocess
import sys
import time


def starte_mariadb_via_systemctl() -> bool:
    """
    Startet MariaDB über systemd (typisch für die meisten modernen
    Linux-Distributionen wie Ubuntu, Debian, Fedora, CentOS...).

    subprocess.run() führt einen Shell-Befehl aus, ähnlich wie man ihn
    im Terminal eingeben würde.

    Parameter:
    - Erstes Argument: Liste mit dem Befehl und seinen Argumenten
      (kein zusammengesetzter String, das ist sicherer und vermeidet
      Shell-Injection-Probleme).
    - check=True: Löst eine Exception (CalledProcessError) aus, falls
      der Befehl einen Fehlercode zurückgibt.
    - capture_output=True: Fängt stdout/stderr ab, damit wir sie
      auswerten oder anzeigen können.
    - text=True: Gibt die Ausgabe als String zurück (statt als Bytes).
    """
    try:
        ergebnis = subprocess.run(
            ["sudo", "systemctl", "start", "mariadb"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("MariaDB wurde über systemctl gestartet.")
        print(ergebnis.stdout)
        return True
    except subprocess.CalledProcessError as fehler:
        print("Fehler beim Starten über systemctl:")
        print(fehler.stderr)
        return False
    except FileNotFoundError:
        # Wird ausgelöst, wenn 'systemctl' auf dem System nicht existiert
        # (z.B. macOS oder ein minimales Docker-Image ohne systemd).
        print("systemctl ist auf diesem System nicht verfügbar.")
        return False


def starte_mariadb_via_service() -> bool:
    """
    Alternative für ältere Systeme ohne systemd, die noch den
    klassischen 'service'-Befehl verwenden (z.B. SysVinit-basierte
    Distributionen oder manche Docker-Container).
    """
    try:
        ergebnis = subprocess.run(
            ["sudo", "service", "mariadb", "start"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("MariaDB wurde über 'service' gestartet.")
        print(ergebnis.stdout)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as fehler:
        print(f"Fehler beim Starten über 'service': {fehler}")
        return False


def starte_mariadb_via_mysqld_safe() -> subprocess.Popen | None:
    """
    Startet den MariaDB-Server-Prozess direkt über 'mysqld_safe'
    (nützlich in Containern oder wenn kein Init-System vorhanden ist).

    subprocess.Popen() startet einen Prozess IM HINTERGRUND, ohne auf
    dessen Beendigung zu warten (im Gegensatz zu subprocess.run()).
    Das ist wichtig, weil ein Datenbankserver dauerhaft laufen soll
    und nicht sofort wieder terminiert.

    stdout/stderr = subprocess.DEVNULL: Unterdrückt die Ausgaben des
    Server-Prozesses in der Konsole (optional, kann auch auf eine
    Log-Datei umgeleitet werden).
    """
    try:
        prozess = subprocess.Popen(
            ["mysqld_safe", "--datadir=/var/lib/mysql"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"mysqld_safe gestartet, Prozess-ID (PID): {prozess.pid}")
        return prozess
    except FileNotFoundError:
        print("mysqld_safe wurde nicht gefunden. Ist MariaDB installiert?")
        return None


def warte_bis_server_bereit(host: str = "127.0.0.1", port: int = 3306,
                             timeout: int = 15) -> bool:
    """
    Prüft wiederholt, ob der MariaDB-Server auf dem angegebenen Port
    erreichbar ist, bevor man versucht, sich zu verbinden.

    Parameter:
    - host: Adresse, unter der der Server erreichbar sein soll
    - port: Standardport von MariaDB/MySQL ist 3306
    - timeout: maximale Wartezeit in Sekunden

    Wir nutzen hier das Modul 'socket', um einfach zu testen, ob der
    Port offen ist (ohne eine vollständige DB-Verbindung aufzubauen).
    """
    import socket

    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            ergebnis = sock.connect_ex((host, port))
            if ergebnis == 0:
                print(f"MariaDB ist auf {host}:{port} erreichbar.")
                return True
        time.sleep(1)

    print(f"Timeout: MariaDB antwortet nach {timeout} Sekunden nicht.")
    return False


def main():
    """
    Hauptfunktion: probiert die verschiedenen Startmethoden nacheinander
    durch, bis eine davon erfolgreich ist.
    """
    print("Versuche, MariaDB zu starten...\n")

    erfolgreich = starte_mariadb_via_systemctl()

    if not erfolgreich:
        erfolgreich = starte_mariadb_via_service()

    if not erfolgreich:
        prozess = starte_mariadb_via_mysqld_safe()
        erfolgreich = prozess is not None

    if not erfolgreich:
        print("MariaDB konnte mit keiner der Methoden gestartet werden.")
        sys.exit(1)

    # Kurz warten und prüfen, ob der Server tatsächlich erreichbar ist
    warte_bis_server_bereit()


if __name__ == "__main__":
    main()
