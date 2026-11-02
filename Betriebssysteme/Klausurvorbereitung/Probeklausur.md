# 1

Down-Top: Ressourcenverwalter für CPU-Zeit und RAM-Platz
Top-Down: Virtualisierung, damit die Programme eine Abstrahierte vereinfachte Schnittstelle zum ansprechen haben

# 2

Der Micro Kernel ist der Kern des Betriebssystems und beschreibt den Ressourcenverwalter und Visualisierer, also ohne die Zusatzsoftware.

# 3

Ein Mehrnutzer-Betriebssystem erlaubt, dass das System von mehreren Nnutzern Zeitgleich genutzt werden kann.

# 4

Ja, ein Pfad kann kanonisch und relativ sein, dad ein kanonischer Pfad nur das verwenden des . und ..-operators innerhalb des Pfades. Das erste Glied des Pfades kann aber relativ sein. Darum sähe ein kanonischer relativer pfad zum beispiel so aus: "./abc"

# 5

Jeder Kern kann zeitgleich nur einen Prozess bedienen, also bei 4 Kernen 4 gleichzeitige Prozesse.

# 6

Quasiparallelität beschreibt das schnelle wechseln der aktiven Prozesse, so dass es so scheint, als würden mehr Prozesse als Kerne gleichzeitig laufen.

# 7

Ein Prozess welchselt in den Blockiert-Zusatend, wenn er auf einen anderen Prozess oder eine Information zum Beispiel vond er festplatte wartet.

# 8

Da der Prozess nicht rechnet, kann er sich auch nicht selbst starten.

# 9

heuristik beschreibt ein Verfahren, das aufgrund von Statistiken oder Regeln deterministisch schätzt, was der beste Weg ist, um den Prozessablauf zu Planen.

# 10

Wenn zwei Mitarbeiter (A, B oder C) das Dokument herunterladen und bearbeiten, und sie hochladen, überschreibt entweder der eine die Hochgeladene Datei des anderen oder im Ungünstigsten Fall vermischen sich beide Uploads (bei gleichzeitigkeit) und beide Arbeiten sind zerstört. Eine Klassische Race Condition.

# 11

Ja, denn so kann es nicht zu fällen kommen, bei denen die Änderungen des anderen unabsichtlich überschrieben werden. Es handelt sich u einem Mutex.

# 12

Wenn A den Mutex auf P hält und Q anfordert. Dieses Dokument Q aber von B gehalten wird, welcher P anfordert, kommt es zu Deadlocks in denen kein Prozess durchlaufen kann.

# 13


