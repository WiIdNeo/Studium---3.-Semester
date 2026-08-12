# Betriebssysteme und Verteilte Systeme

*Modulcode 4TI-BSVS-30, 5 ECTS, Klausur 120 Min. im 4. Theoriesemester, keine Zugangsvoraussetzung.*

Kombiniert zwei Bereiche: klassische Betriebssystemkonzepte (Prozesse, Speicher, Dateisysteme) und die Erweiterung auf mehrere kooperierende Rechner (verteilte Systeme).

> **Korrektur zur ursprünglichen Einordnung:** Laut Modulbeschreibung liegt der praktische Schwerpunkt hier auf **Linux-Konzepten und Shell-Programmierung** (die Studierenden sollen u. a. "Shell-Programme schreiben" können) – nicht auf C oder Assembler. Assembler-Programmierung ist offiziell Teil des Moduls **Rechnerarchitektur (4TI-RA-40)**, das im 4./5. Semester folgt ("Lösung von Übungsaufgaben in der Assemblerprogrammierung"). C-Kenntnisse bleiben trotzdem sinnvoll, weil das Modul "Grundlagen der Programmierungstechnik" (1. Semester) ausdrücklich C als empfohlene Sprache nennt und viele OS-Konzepte darauf aufbauen. Ich habe die Ressourcen unten entsprechend angepasst: C bleibt drin, Bash/Shell kommt neu dazu, Assembler ist nur noch als Ausblick auf das spätere Modul Rechnerarchitektur markiert.

## Offizielle Lerninhalte (lt. Modulbeschreibung)
**Betriebssysteme:** historische Entwicklung, Schichtenmodell, Klassifikation, Architekturmodelle, Betriebsmittel als Abstraktionskonzept, Prozesse und ihre Verwaltung, Scheduling, Speicherverwaltung (Real-/virtueller Speicher), Dateiverwaltung, Prozesskommunikation und -synchronisation, Deadlocks, Virtualisierung.
**Verteilte Systeme:** verteilte Betriebssysteme und Anwendungen, Client-Server-Systeme, Cloud Computing.

## Inhaltliche Schwerpunkte – Betriebssysteme
- Prozesse und Threads, Kontextwechsel, Zustandsdiagramme
- CPU-Scheduling (FCFS, SJF, Round Robin, Priority Scheduling)
- Synchronisation: Race Conditions, Mutex, Semaphore, Monitore, Deadlocks
- Speicherverwaltung: Paging, Segmentierung, virtueller Speicher
- Dateisysteme und Massenspeicherverwaltung
- Systemaufrufe (Syscalls), Kernel- vs. User-Mode

## Inhaltliche Schwerpunkte – Verteilte Systeme
- Client-Server- vs. Peer-to-Peer-Architekturen
- Kommunikation: RPC, Message Passing, REST
- Uhrensynchronisation und logische Zeit (Lamport-Zeitstempel)
- Konsistenzmodelle und Replikation (sequentielle, kausale, eventuelle Konsistenz)
- Konsensverfahren (2-Phasen-Commit, Paxos/Raft als Ausblick)
- Fehlertoleranz in verteilten Systemen

## YouTube – Playlists & Vorlesungen

| Ressource | Beschreibung | Link |
|---|---|---|
| Neso Academy – Operating System (Playlist) | Sehr klar strukturierte, englische Komplettreihe (ca. 17 Std.), deckt fast alle Klausurthemen ab | https://www.youtube.com/playlist?list=PLBlnK6fEyqRiVhbXDGLXDk_OQAeuVcp2O |
| Vorlesung Betriebssysteme und Sicherheit (TU Dresden) – Prozesse und Threads | Deutschsprachige Vorlesungsaufzeichnung mit Fokus auf Prozess-/Thread-Konzepte | https://www.youtube.com/watch?v=XqC6cipShxc |
| Vorlesung Betriebssysteme und Sicherheit – Scheduling | Fortsetzung der TU-Dresden-Reihe, Scheduling-Verfahren | https://www.youtube.com/watch?v=R2gpzugpPjU |
| "Betriebssysteme #14" – Threads einfach erklärt (deutsch) | Kurzes, verständliches Erklärvideo zu Thread-Konzepten | https://www.youtube.com/watch?v=PnE7xdMKwc4 |

## Dokumentationen & Skripte
- **Operating Systems: Three Easy Pieces** (OSTEP) – kostenloses Standardlehrbuch, sehr verständlich, viele Uni-Vorlesungen (u. a. KIT) basieren direkt darauf: https://pages.cs.wisc.edu/~remzi/OSTEP/
- KIT-Vorlesungsseite "Betriebssysteme" (Themenüberblick, Literaturempfehlungen): https://ilias.studium.kit.edu (Suche: "Betriebssysteme KIT")
- TUM-Vorlesungsskript "Grundlagen Rechnernetze und Verteilte Systeme", Kapitel 9 (Verteilte Systeme): https://www.net.in.tum.de
- Foliensatz Verteilte Systeme – Replikation & Konsistenz (HTWG Konstanz, gut für Konsistenzmodelle): http://www-home.htwg-konstanz.de/~haase/lehre/versy/

## Basisliteratur laut Modulbeschreibung (prüfungsrelevant)
- TANENBAUM, A. S.: *Moderne Betriebssysteme*, Pearson Studium
- MANDL, P.: *Grundkurs Betriebssysteme: Architekturen, Betriebsmittelverwaltung, Synchronisation, Prozesskommunikation*, Vieweg
- BENGEL, G.: *Verteilte Systeme: Client-Server-Computing für Studenten und Praktiker*, Vieweg
- Vertiefend: TANENBAUM/van STEEN: *Verteilte Systeme: Grundlagen und Paradigmen*; COULOURIS/DOLLIMORE/KINDBERG: *Verteilte Systeme: Konzepte und Design*

## Empfohlene Vorgehensweise
1. Zuerst Prozess-/Thread-Grundlagen und Scheduling verstehen – das baut auf sich selbst auf.
2. Synchronisationsprobleme (Erzeuger-Verbraucher, Leser-Schreiber) selbst in C mit POSIX-Threads nachprogrammieren.
3. Speicherverwaltung (Paging/Segmentierung) mit Diagrammen üben, da hier viele Rechenaufgaben in Klausuren vorkommen.
4. Erst danach zu Verteilten Systemen wechseln – die Konzepte (Nebenläufigkeit, Zustände, Fehler) bauen direkt auf dem BS-Teil auf.
5. Konsistenzmodelle anhand konkreter Beispiele (verteilte Mailbox, Replikation) durchdenken statt nur auswendig lernen.

## C auffrischen (weiterhin sinnvoll als Grundlage)
- C Tutorial Deutsch – Lerne C in 90 Minuten: https://www.youtube.com/watch?v=BSaF8KxnoLY
- C Programmieren lernen – Einführung und Installation (deutsch): https://www.youtube.com/watch?v=-QPkcLshYC0
- Kurs C-Programmierung (TU Chemnitz, textbasiertes Skript – praktisch, da an deiner eigenen Uni): https://www.tu-chemnitz.de/urz/archiv/kursunterlagen/C/index.htm

**Tipp:** Für das Verständnis von Betriebssystemen hilft es enorm, ein einfaches C-Programm mit `fork()` zu schreiben und dessen Verhalten (Prozess-IDs, Speichertrennung) selbst zu beobachten.

## Bash/Shell-Programmierung (neu, da laut Modulbeschreibung Praxisinhalt)
- Bash Scripting Tutorial für Anfänger (deutsch): https://www.youtube.com/results?search_query=bash+scripting+tutorial+deutsch
- Linux Journey – interaktives, kostenloses Lern-Tool für Linux/Shell-Grundlagen: https://linuxjourney.com
- ExplainShell – erklärt jeden Bash-Befehl Wort für Wort: https://explainshell.com

## Assembler – Ausblick auf das spätere Modul "Rechnerarchitektur"
Assembler ist offiziell erst im Modul *Rechnerarchitektur* (4TI-RA-40) Thema. Wenn du trotzdem schon reinschnuppern willst:
- Assembler Programmierung Tutorial – Grundlagen (deutsch, NASM, Einstieg): https://www.youtube.com/watch?v=kBzZRZ0XYq4
- Einführung in die moderne Assembler-Programmierung von Scot W. Stevenson (deutsch, aktuell): https://www.youtube.com/watch?v=Hdyxe_B75ks
- Learn Assembly for Beginners – x86-64 Tutorials (englisch, Playlist): https://www.youtube.com/playlist?list=PL9o2C-4xGfjHl5PF-Xt-yWH2zc4wjJ3AW
