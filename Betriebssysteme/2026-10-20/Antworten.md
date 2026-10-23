# 1
## a
### a.1

- Speicherverwaltung: RAM und RAM-Zugriff wird auf die verschiedenen Prozesse verteilt. 
- Speichervirtualisierung: U. a. um die physische Speicheradresse zu verschleiern (Sicherheit)

### a.2

Der Micro-Kernel ist das Betriebssystem ohne die zusätzliche Software, nur die Basisfunktionen des Kernels.

### a.3

Ein System, dass Prozesse bestimmten Nutzern zuordnen und voneinander abschirmen kann.

### a.5

Ja, ein Pfad wie "./a/b/c/d" ist Kanonisch, da er nur am Anfang einen . und keinen .. opperator enthält. Außerdem ist er relativ, da er einen .-Opperator enthält

# 2
## a
### a.1

4

### a.2

Eine scheinbare Parallität durch schnelles durchwechseln der aktiven Prozesse.

### a.3

Wenn sie auf Daten oder andere Prozesse warten.

### a.4

Weil sie nicht im Kernmodus laufen.

### a.5

Heuristik beschreibt einen determinischtischen Prozess, bei dem per Regeln ermittelt wird, wie die Prozessabläufe an die Reihe kommen.

## b

Wenn A gerade einen Stand verändert, B diesen auch zieht und beide Hochladen überschreiben sie die Änderungen des jeweils anderen.

Race Condition

Es löst das Problem, da immer erst eine Bearbeitung fertig sein muss, bevor die zweite anfangen kann: ein Mutex.

Deadlock, wenn Q P brauch tun umgekehrt, aber zwei unterschiedliche nutzer beide Dateien gerade nutzen.

# 3 

| |5|2|4|1|0|1|2|5|2|4|1|0|
|-|-|-|-|-|-|-|-|-|-|-|-|-|
|0|5|5|5|5|0|0|0|0|0|0|1|1
|1|-|2|2|2|2|2|2|5|5|5|5|0
|2|-|-|4|4|4|4|4|4|2|2|2|2
|3|-|-|-|1|1|1|1|1|1|4|4|4

