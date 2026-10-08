## 1. Umgebung vorbereiten

### 1.1 Virtuelle Umgebung und Installation (PowerShell)

```powershell
py -3.11 -m venv C:\rag\venv
C:\rag\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install open-webui
```

Falls die Ausführung von Skripten blockiert ist:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 1.2 PostgreSQL mit pgvector (Docker)

```powershell
docker run -d --name pgvector `
  -e POSTGRES_USER=openwebui `
  -e POSTGRES_PASSWORD=openwebui_pw `
  -e POSTGRES_DB=openwebui `
  -p 5432:5432 `
  -v pgvector_data:/var/lib/postgresql/data `
  pgvector/pgvector:pg16
```

Optional prüfen, ob die Extension verfügbar ist:

```powershell
docker exec -it pgvector psql -U openwebui -d openwebui -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 1.3 LM Studio

1. Modell laden (z. B. Llama 3.1 8B Instruct oder Mistral 7B Instruct).
2. Reiter **Developer / Local Server** → Server starten (Port `1234`).
3. Test:

```powershell
curl http://localhost:1234/v1/models
```

> **Embeddings:** Open WebUI nutzt standardmäßig ein lokales Sentence-Transformers-Modell für Embeddings. Der erste Start lädt dieses Modell herunter (Internet nötig, dauert etwas). Alternativ kann in LM Studio ein Embedding-Modell geladen und über die OpenAI-API genutzt werden.

---

## 2. Schritt 1: Start-Skript `start-rag.ps1`

```powershell
# start-rag.ps1 - Startet Open WebUI mit RAG-Konfiguration
# Voraussetzung: LM Studio Server läuft auf Port 1234, pgvector-Container läuft

param(
    [switch]$UseChroma   # Alternative: SQLite + ChromaDB (nur Testzwecke)
)

# --- virtuelle Umgebung aktivieren ---
& "C:\rag\venv\Scripts\Activate.ps1"

# --- LM Studio als OpenAI-kompatibles Backend ---
$env:ENABLE_OLLAMA_API          = "False"
$env:ENABLE_OPENAI_API          = "True"
$env:OPENAI_API_BASE_URL        = "http://localhost:1234/v1"
$env:OPENAI_API_KEY             = "lm-studio"   # Platzhalter, LM Studio prüft den Key nicht

# --- Datenbank / Vektorspeicher ---
if ($UseChroma) {
    # SQLite (Standard) + ChromaDB (Standard) - nur Test
    Remove-Item Env:DATABASE_URL  -ErrorAction SilentlyContinue
    Remove-Item Env:VECTOR_DB     -ErrorAction SilentlyContinue
    Write-Host "Modus: SQLite + ChromaDB (Test)"
} else {
    $env:DATABASE_URL      = "postgresql://openwebui:openwebui_pw@localhost:5432/openwebui"
    $env:VECTOR_DB         = "pgvector"
    $env:PGVECTOR_DB_URL   = "postgresql://openwebui:openwebui_pw@localhost:5432/openwebui"
    Write-Host "Modus: PostgreSQL + pgvector"
}

# --- RAG-Einstellungen ---
$env:RAG_TOP_K                  = "5"
$env:RAG_RELEVANCE_THRESHOLD    = "0.7"

# --- Sonstiges ---
$env:WEBUI_AUTH                 = "True"
$env:DATA_DIR                   = "C:\rag\data"
$env:PORT                       = "8080"

Write-Host "RAG_TOP_K=$env:RAG_TOP_K, RAG_RELEVANCE_THRESHOLD=$env:RAG_RELEVANCE_THRESHOLD"
open-webui serve --port $env:PORT
```

Start: `.\start-rag.ps1` (bzw. `.\start-rag.ps1 -UseChroma` für die Test-Alternative). Aufruf im Browser: <http://localhost:8080>

> **Hinweis zu den RAG-Variablen:** In Open WebUI sind `RAG_TOP_K` und `RAG_RELEVANCE_THRESHOLD` sogenannte *persistente* Konfigurationswerte. Werden sie später in *Admin Panel → Settings → Documents* geändert, haben die UI-Werte Vorrang vor den Umgebungsvariablen (diese gelten nur beim ersten Start). Prüfe nach dem Start in der UI, dass die Werte wie gewünscht angezeigt werden, und dokumentiere das per Screenshot.
>
> **Hinweis zum Threshold:** Der Threshold wirkt nur bei aktivierter Relevanz-Bewertung (z. B. Hybrid Search mit Reranker). Sieht man bei Threshold 0.7 häufig „keine Treffer", ist das ein erwartbares Verhalten und ein guter Reflexionspunkt.

**Abgabe:** Code-Snippet oben einfügen. ⟦Screenshot: laufendes Terminal / Login-Seite⟧

---

## 3. Schritt 2: Knowledge Base erstellen

1. Ersten Benutzer registrieren → dieser ist automatisch **Admin**.
2. **Workspace → Knowledge → „+"**.
3. Name: `Alexander Vogel – Netzwerk-Dokumentation`
4. Beschreibung (Vorschlag): `Administrations-Skripte, Checklisten und Dokumentation von Alexander Vogel (Netzwerk-Migration, VLAN, IP-Planung).`
5. Dokumente hochladen: `Vogel_Netzwerk_Skript.pdf` sowie die übrigen bereitgestellten Dateien.
6. Warten, bis alle Dokumente indiziert sind („Ready").
7. Im Chat: `#` eingeben bzw. über das „+"-Menü die Collection auswählen, damit sie beim Prompt als Kontext verwendet wird.

**Dokumentation:** ⟦Screenshot des Knowledge-Panels mit allen Dokumenten (Status Ready)⟧

| Nr. | Dateiname | Typ | Status |
|---|---|---|---|
| 1 | Vogel_Netzwerk_Skript.pdf | PDF | ⟦Ready⟧ |
| 2 | ⟦...⟧ | ⟦...⟧ | ⟦...⟧ |
| 3 | ⟦...⟧ | ⟦...⟧ | ⟦...⟧ |
| 4 | ⟦...⟧ | ⟦...⟧ | ⟦...⟧ |
| 5 | ⟦...⟧ | ⟦...⟧ | ⟦...⟧ |

---

## 4. Schritt 3: Prompts (12 Stück)

**Vorgehen:** Jeden Prompt in einem **neuen Chat** mit ausgewählter Collection stellen (sonst beeinflusst der Chatverlauf das Ergebnis). Prompt wortwörtlich kopieren, Antwort vollständig übernehmen, Quellen aus den Quellen-Chips aufklappen.

> Die Prompts sind so formuliert, dass sie eine **Quellenangabe** erzwingen und **Erfundenes** vermeiden.

### Prompt #1 – VLAN-Konfiguration (Grundlagen)
```
Welche Schritte beschreibt die Dokumentation von Alexander Vogel für die Einrichtung eines neuen VLANs? Nenne die Schritte in der richtigen Reihenfolge und gib an, aus welchem Abschnitt sie stammen.
```

### Prompt #2 – IP-Planung
```
Wie sieht laut Dokumentation das IP-Adressschema für die verschiedenen Netzsegmente aus? Gib Subnetze, VLAN-IDs und Zweck der Segmente möglichst als Tabelle an und nenne die Quelle.
```

### Prompt #3 – Netzwerk-Migration (Ablauf)
```
Beschreibe den empfohlenen Ablauf einer Netzwerk-Migration nach Alexander Vogel: Vorbereitung, Durchführung, Verifikation und Rollback. Was soll vor Beginn der Migration geprüft werden?
```

### Prompt #4 – Rollback / Fehlerfall
```
Was soll ich tun, wenn während der Netzwerk-Migration nach der Umstellung eines Segments Clients keine IP-Adresse mehr bekommen? Gibt es dazu ein Rollback- oder Troubleshooting-Vorgehen in der Dokumentation?
```

### Prompt #5 – Switch-Konfiguration (Trunk/Access)
```
Wie konfiguriere ich laut Skript einen Trunk-Port und einen Access-Port für ein bestimmtes VLAN? Gib mir die Konfigurationsbefehle exakt so wieder, wie sie im Dokument stehen, und nenne den Abschnitt.
```

### Prompt #6 – DHCP / Adressbereiche
```
Welche DHCP-Bereiche und statischen Adressen (z. B. für Server, Drucker, Management) sind im Dokument vorgesehen, und wie sollen Reservierungen gehandhabt werden?
```

### Prompt #7 – Checkliste
```
Erstelle aus der Dokumentation eine Checkliste für die Migration eines Standorts in ein neues IP-Konzept, die ein neuer Mitarbeiter Punkt für Punkt abarbeiten kann. Verwende nur Informationen aus der Knowledge Base.
```

### Prompt #8 – Firewall & Security (Kategorie aus Aufgabe)
```
Welche Ports müssen für RDP-Access freigeschaltet werden, und welche Sicherheitsvorgaben gelten dafür laut Dokumentation?
```
*(Je nach Dokumentenlage kann hier „nicht gefunden" die richtige Antwort sein.)*

### Prompt #9 – VPN (Kategorie aus Aufgabe)
```
Wie richte ich eine Site-to-Site-VPN-Verbindung mit WireGuard ein? Beantworte nur anhand der bereitgestellten Dokumente und sage klar, wenn dazu nichts enthalten ist.
```

### Prompt #10 – Zusammenhang VLAN ↔ Firewall/Routing
```
Welche Auswirkungen hat die Einführung eines neuen VLANs auf Routing und Zugriffsregeln zwischen den Segmenten, und was sollte ich laut Dokumentation dabei zusätzlich beachten?
```

### Prompt #11 – Negativtest (Halluzinationsprüfung)
```
Welche Backup-Strategie für den Exchange-Server empfiehlt Alexander Vogel in seiner Dokumentation?
```
*Erwartung: Das Modell sollte angeben, dass dazu nichts in der Knowledge Base steht. Bewerte, ob es das tut oder etwas erfindet.*

### Prompt #12 – Quellenpräzision / Wortlaut
```
Zitiere die Passage, in der die Vorgehensweise zur Verifikation nach einer Migration beschrieben wird (maximal 5 Sätze), und nenne Dokument sowie Seite oder Abschnitt.
```

---

### 4.1 Protokollvorlage (pro Prompt kopieren)

```markdown
#### Prompt #⟦N⟧
**Prompt (wörtlich):**
> ⟦...⟧

**Antwort (vollständig):**
> ⟦...⟧

**Angezeigte Quellen:**
- ⟦Dokument, Abschnitt/Seite, ggf. [cite:knowledge:N]⟧

**Bewertung:** ⟦x/5⟧ ⭐
- Technisch korrekt? ⟦ja/teilweise/nein, Begründung. Abgleich mit dem Originaldokument!⟧
- Quellenangaben hilfreich? ⟦...⟧
- Würde ich die Antwort im NOC weitergeben? ⟦ja/nein, warum⟧
```

### 4.2 Übersichtstabelle (am Ende der Abgabe)

| # | Kategorie | Technisch korrekt | Quellen hilfreich | NOC-tauglich | Gesamt (1–5) |
|---|---|---|---|---|---|
| 1 | VLAN | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 2 | IP-Planung | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 3 | Migration | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 4 | Rollback | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 5 | Switch-Config | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 6 | DHCP | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 7 | Checkliste | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 8 | Firewall | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 9 | VPN | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 10 | VLAN+Security | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 11 | Negativtest | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 12 | Zitat | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |

---

## 5. Schritt 4 (Bonus): RAG-Parameter vergleichen

### 5.1 Vorgehen

1. **Variante A:** `RAG_TOP_K = 3`, `RAG_RELEVANCE_THRESHOLD = 0.8`
2. **Variante B:** `RAG_TOP_K = 10`, `RAG_RELEVANCE_THRESHOLD = 0.5`

Umstellen entweder in *Admin Panel → Settings → Documents* (Top K / Relevance Threshold) **oder** über das Start-Skript:

```powershell
# Variante A
$env:RAG_TOP_K = "3";  $env:RAG_RELEVANCE_THRESHOLD = "0.8"
# Variante B
$env:RAG_TOP_K = "10"; $env:RAG_RELEVANCE_THRESHOLD = "0.5"
```

> Achtung: Wegen der persistenten Konfiguration (siehe Hinweis oben) die Werte **in der UI kontrollieren**, sonst testest du unbemerkt zweimal dieselbe Einstellung.

3. Dieselben **vier Testprompts** in beiden Varianten stellen, je in neuem Chat:

| Testprompt | Zweck |
|---|---|
| #2 (IP-Schema als Tabelle) | Präzisions-/Fakten-Abfrage (Quick-Fix) |
| #5 (Switch-Befehle exakt) | Exakte Befehle, Gefahr von Vermischung |
| #3 (Migrationsablauf komplett) | Deep-Dive, benötigt viel Kontext |
| #11 (Negativtest Exchange) | Halluzinations-/Rauschverhalten bei niedrigem Threshold |

### 5.2 Ergebnistabelle

| Testprompt | Variante A: Quellenanzahl | A: Qualität (1–5) | Variante B: Quellenanzahl | B: Qualität (1–5) | Auffälligkeiten |
|---|---|---|---|---|---|
| #2 | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| #5 | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| #3 | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| #11 | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |

### 5.3 Reflexion (100–200 Wörter) – Gerüst zum Ausformulieren

Beantworte mit deinen eigenen Beobachtungen:

- **Welche Variante war technisch präziser?** *(Hypothese zum Überprüfen: Variante A liefert wenige, hochrelevante Chunks und damit weniger Rauschen, riskiert aber, relevante Passagen ganz zu verpassen. Bei strengem Threshold kann auch „keine Treffer" auftreten.)*
- **Welche Variante lieferte mehr Kontext / vollständigere Skripte?** *(Hypothese: Variante B, da mehr Chunks, aber evtl. mit irrelevanten Abschnitten und höherem Verbrauch des Kontextfensters eines 8B-Modells.)*
- **Empfehlung:** *Quick-Fix* (z. B. „Welcher Port/Befehl?") → eher A; *Deep-Dive* (z. B. kompletter Migrationsablauf, Checkliste) → eher B. Begründe das mit **deinen** Messungen. Falls sie der Hypothese widersprechen, ist das ein wertvolleres Ergebnis. Gib auch an, wenn das Kontextfenster des lokalen Modells bei Variante B ein Limit war.

⟦Dein Text, 100–200 Wörter⟧

---

## 6. Reflexion zur Gesamtqualität (Vorschlag für die Abgabe)

Gehe auf diese Punkte ein, gestützt auf deine Protokolle:

1. **Korrektheit:** Wie oft stimmte die Antwort nachweislich mit dem Originaldokument überein? Wo wurden Details vermischt oder ergänzt?
2. **Halluzinationen:** Verhalten bei Prompt #8, #9, #11 (Inhalt nicht im Dokument). Wurde „nicht gefunden" gesagt oder aus allgemeinem Modellwissen geantwortet, und wurde dies kenntlich gemacht?
3. **Quellenqualität:** Waren Chunks sinnvoll abgegrenzt? Wurden Tabellen und Codeblöcke aus dem PDF korrekt extrahiert (typische Schwäche bei PDFs)?
4. **Modellgröße:** Einfluss des lokalen 8B-Modells auf Reasoning und Formatierung.
5. **Praxistauglichkeit:** Eignung für neue Mitarbeiter, Risiken bei sicherheitskritischen Konfigurationen (immer gegen das Original prüfen), mögliche Verbesserungen (Chunk-Größe, Hybrid Search, Reranker, bessere Dokumentstruktur, Markdown statt PDF).

---

## 7. Abgabe-Checkliste

- [ ] `start-rag.ps1` als Code-Snippet
- [ ] Screenshot Knowledge-Panel (alle Dokumente „Ready")
- [ ] ≥ 10 Prompts im Protokollformat (wörtlicher Prompt, vollständige Antwort, Quellen, Bewertung)
- [ ] Übersichtstabelle
- [ ] Bonus: Varianten A/B, Ergebnistabelle, Reflexion (100–200 Wörter)
- [ ] Gesamtreflexion

---

## 8. Troubleshooting

| Problem | Lösung |
|---|---|
| Kein Modell in Open WebUI sichtbar | LM Studio Server läuft? `curl http://localhost:1234/v1/models`; in Open WebUI unter *Admin → Settings → Connections* die URL `http://localhost:1234/v1` prüfen |
| Dokument bleibt auf „Processing" | Erster Start lädt Embedding-Modell herunter; Terminal beobachten |
| Verbindung zu PostgreSQL schlägt fehl | `docker ps`, Port 5432 frei? Zugangsdaten in `DATABASE_URL` prüfen |
| Antworten ohne Quellen | Collection im Chat nicht ausgewählt (`#` bzw. „+") |
| Immer „keine Treffer" | Threshold zu hoch; testweise 0.5 setzen und beobachten |
| PDF-Text unleserlich | PDF evtl. gescannt → OCR nötig oder Inhalt als Markdown/TXT bereitstellen |

# Hausaufgabe: RAG-System für Netzwerkadministration (Open WebUI) – Linux-Mint-Version

> **Legende:** Alles in `⟦ ... ⟧` ist von dir nach dem Test auszufüllen (Screenshots, Antworten, Quellen, Bewertung).
> Alles andere ist fertig und kann direkt verwendet werden.
> Diese Fassung ersetzt die Windows-/PowerShell-Teile der ursprünglichen Anleitung durch Linux-Mint-/Bash-Varianten. Prompts, Protokollvorlagen und Reflexion sind identisch.

---

## 0. Wichtige Hinweise vorab

- **Plattform:** Die Aufgabe nennt Windows 11 und PowerShell. Du bearbeitest sie unter Linux Mint, vermerke das in der Abgabe (statt `start-rag.ps1` heißt das Skript hier `start-rag.sh`). Falls die Abgabe zwingend ein `.ps1`-Skript verlangt, kläre das kurz mit dem Dozenten oder gib zusätzlich die Windows-Fassung ab.
- **Dokumentenlage:** Die Aufgabe spricht von 5 Dokumenten, aufgelistet ist aber nur `Vogel_Netzwerk_Skript.pdf` (Netzwerk-Migrationen, VLAN-Konfiguration, IP-Planung). Prüfe, ob du alle 5 Dateien erhalten hast. Falls nicht, lade nur hoch, was vorliegt, und vermerke das in der Abgabe. Die Prompts sind auf **Migration / VLAN / IP-Planung** ausgerichtet, ergänzt um Firewall und VPN als „Negativtests".
- **Python-Version:** Open WebUI verlangt in der Regel **Python 3.11**. Linux Mint 22 bringt Python 3.12, Mint 21 bringt 3.10 mit, beides passt nicht. Deshalb wird Python 3.11 unten über **uv** bereitgestellt, ohne das System-Python anzutasten (wichtig, Mint-Tools hängen daran).
- **Reihenfolge:** LM Studio starten → Modell laden → Local Server starten → erst dann Open WebUI.

---

## 1. Umgebung vorbereiten

### 1.1 Basispakete und uv

```bash
sudo apt update
sudo apt install -y curl git build-essential

curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc          # oder neues Terminal öffnen
uv --version
```

### 1.2 Virtuelle Umgebung mit Python 3.11 und Open WebUI

```bash
mkdir -p ~/rag && cd ~/rag
uv venv venv --python 3.11          # lädt Python 3.11 automatisch
source ~/rag/venv/bin/activate
python --version                     # muss 3.11.x anzeigen
uv pip install open-webui
```

Alternative ohne uv: `sudo apt install python3.11 python3.11-venv` (ist auf Mint nicht in jedem Release verfügbar, daher ist uv der verlässlichere Weg).

### 1.3 PostgreSQL mit pgvector (Docker, empfohlen)

Docker installieren (einfacher Weg über die Mint-Paketquellen):

```bash
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker                        # oder einmal ab- und wieder anmelden
docker --version
```

pgvector-Container starten:

```bash
docker run -d --name pgvector \
  -e POSTGRES_USER=openwebui \
  -e POSTGRES_PASSWORD=openwebui_pw \
  -e POSTGRES_DB=openwebui \
  -p 5432:5432 \
  -v pgvector_data:/var/lib/postgresql/data \
  pgvector/pgvector:pg16
```

Optional prüfen, ob die Extension verfügbar ist:

```bash
docker exec -it pgvector psql -U openwebui -d openwebui -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

Nach einem Neustart des Rechners startet der Container mit `docker start pgvector` wieder (oder bei Anlage `--restart unless-stopped` ergänzen).

> **Alternative ohne Docker:** Auf Mint 22 geht auch `sudo apt install postgresql postgresql-16-pgvector`, anschließend Benutzer und Datenbank per `sudo -u postgres psql` anlegen. Auf Mint 21 ist das pgvector-Paket meist nicht verfügbar, dort Docker verwenden.

### 1.4 LM Studio

1. AppImage von <https://lmstudio.ai> herunterladen.
2. Ausführbar machen und starten:

```bash
sudo apt install -y libfuse2          # falls der AppImage-Start an FUSE scheitert (ggf. libfuse2t64)
chmod +x ~/Downloads/LM-Studio-*.AppImage
~/Downloads/LM-Studio-*.AppImage
```

   Startet die Oberfläche nicht (Sandbox-Fehler, typisch bei neueren Ubuntu-Basen), hilft das Flag `--no-sandbox`.
3. Modell laden (z. B. Llama 3.1 8B Instruct oder Mistral 7B Instruct).
4. Reiter **Developer / Local Server** → Server starten (Port `1234`).
5. Test:

```bash
curl http://localhost:1234/v1/models
```

> **Embeddings:** Open WebUI nutzt standardmäßig ein lokales Sentence-Transformers-Modell für Embeddings. Der erste Start lädt dieses Modell herunter (Internet nötig, dauert etwas). Alternativ kann in LM Studio ein Embedding-Modell geladen und über die OpenAI-API genutzt werden.

---

## 2. Schritt 1: Start-Skript `start-rag.sh`

```bash
#!/usr/bin/env bash
# start-rag.sh - Startet Open WebUI mit RAG-Konfiguration (Linux Mint)
# Voraussetzung: LM Studio Server läuft auf Port 1234, pgvector-Container läuft
# Aufruf:  ./start-rag.sh            (PostgreSQL + pgvector)
#          ./start-rag.sh --chroma   (SQLite + ChromaDB, nur Testzwecke)
set -euo pipefail

# --- virtuelle Umgebung aktivieren ---
source "$HOME/rag/venv/bin/activate"

# --- LM Studio als OpenAI-kompatibles Backend ---
export ENABLE_OLLAMA_API="False"
export ENABLE_OPENAI_API="True"
export OPENAI_API_BASE_URL="http://localhost:1234/v1"
export OPENAI_API_KEY="lm-studio"      # Platzhalter, LM Studio prüft den Key nicht

# --- Datenbank / Vektorspeicher ---
if [[ "${1:-}" == "--chroma" ]]; then
    # SQLite (Standard) + ChromaDB (Standard) - nur Test
    unset DATABASE_URL VECTOR_DB PGVECTOR_DB_URL
    echo "Modus: SQLite + ChromaDB (Test)"
else
    export DATABASE_URL="postgresql://openwebui:openwebui_pw@localhost:5432/openwebui"
    export VECTOR_DB="pgvector"
    export PGVECTOR_DB_URL="postgresql://openwebui:openwebui_pw@localhost:5432/openwebui"
    echo "Modus: PostgreSQL + pgvector"
fi

# --- RAG-Einstellungen ---
export RAG_TOP_K="5"
export RAG_RELEVANCE_THRESHOLD="0.7"

# --- Sonstiges ---
export WEBUI_AUTH="True"
export DATA_DIR="$HOME/rag/data"
export PORT="8080"

echo "RAG_TOP_K=$RAG_TOP_K, RAG_RELEVANCE_THRESHOLD=$RAG_RELEVANCE_THRESHOLD"
exec open-webui serve --port "$PORT"
```

Einrichten und starten:

```bash
cd ~/rag
nano start-rag.sh            # Inhalt einfügen, speichern
chmod +x start-rag.sh
./start-rag.sh               # bzw. ./start-rag.sh --chroma
```

Aufruf im Browser: <http://localhost:8080>

> **Hinweis zu den RAG-Variablen:** In Open WebUI sind `RAG_TOP_K` und `RAG_RELEVANCE_THRESHOLD` sogenannte *persistente* Konfigurationswerte. Werden sie später in *Admin Panel → Settings → Documents* geändert, haben die UI-Werte Vorrang vor den Umgebungsvariablen (diese gelten nur beim ersten Start). Prüfe nach dem Start in der UI, dass die Werte wie gewünscht angezeigt werden, und dokumentiere das per Screenshot.
>
> **Hinweis zum Threshold:** Der Threshold wirkt nur bei aktivierter Relevanz-Bewertung (z. B. Hybrid Search mit Reranker). Sieht man bei Threshold 0.7 häufig „keine Treffer", ist das ein erwartbares Verhalten und ein guter Reflexionspunkt.

**Abgabe:** Code-Snippet oben einfügen. ⟦Screenshot: laufendes Terminal / Login-Seite⟧

---

## 3. Schritt 2: Knowledge Base erstellen

1. Ersten Benutzer registrieren → dieser ist automatisch **Admin**.
2. **Workspace → Knowledge → „+"**.
3. Name: `Alexander Vogel – Netzwerk-Dokumentation`
4. Beschreibung (Vorschlag): `Administrations-Skripte, Checklisten und Dokumentation von Alexander Vogel (Netzwerk-Migration, VLAN, IP-Planung).`
5. Dokumente hochladen: `Vogel_Netzwerk_Skript.pdf` sowie die übrigen bereitgestellten Dateien.
6. Warten, bis alle Dokumente indiziert sind („Ready").
7. Im Chat: `#` eingeben bzw. über das „+"-Menü die Collection auswählen, damit sie beim Prompt als Kontext verwendet wird.

**Dokumentation:** ⟦Screenshot des Knowledge-Panels mit allen Dokumenten (Status Ready)⟧

| Nr. | Dateiname | Typ | Status |
|---|---|---|---|
| 1 | Vogel_Netzwerk_Skript.pdf | PDF | ⟦Ready⟧ |
| 2 | ⟦...⟧ | ⟦...⟧ | ⟦...⟧ |
| 3 | ⟦...⟧ | ⟦...⟧ | ⟦...⟧ |
| 4 | ⟦...⟧ | ⟦...⟧ | ⟦...⟧ |
| 5 | ⟦...⟧ | ⟦...⟧ | ⟦...⟧ |

---

## 4. Schritt 3: Prompts (12 Stück)

**Vorgehen:** Jeden Prompt in einem **neuen Chat** mit ausgewählter Collection stellen (sonst beeinflusst der Chatverlauf das Ergebnis). Prompt wortwörtlich kopieren, Antwort vollständig übernehmen, Quellen aus den Quellen-Chips aufklappen.

> Die Prompts sind so formuliert, dass sie eine **Quellenangabe** erzwingen und **Erfundenes** vermeiden.

### Prompt #1 – VLAN-Konfiguration (Grundlagen)
```
Welche Schritte beschreibt die Dokumentation von Alexander Vogel für die Einrichtung eines neuen VLANs? Nenne die Schritte in der richtigen Reihenfolge und gib an, aus welchem Abschnitt sie stammen.
```

### Prompt #2 – IP-Planung
```
Wie sieht laut Dokumentation das IP-Adressschema für die verschiedenen Netzsegmente aus? Gib Subnetze, VLAN-IDs und Zweck der Segmente möglichst als Tabelle an und nenne die Quelle.
```

### Prompt #3 – Netzwerk-Migration (Ablauf)
```
Beschreibe den empfohlenen Ablauf einer Netzwerk-Migration nach Alexander Vogel: Vorbereitung, Durchführung, Verifikation und Rollback. Was soll vor Beginn der Migration geprüft werden?
```

### Prompt #4 – Rollback / Fehlerfall
```
Was soll ich tun, wenn während der Netzwerk-Migration nach der Umstellung eines Segments Clients keine IP-Adresse mehr bekommen? Gibt es dazu ein Rollback- oder Troubleshooting-Vorgehen in der Dokumentation?
```

### Prompt #5 – Switch-Konfiguration (Trunk/Access)
```
Wie konfiguriere ich laut Skript einen Trunk-Port und einen Access-Port für ein bestimmtes VLAN? Gib mir die Konfigurationsbefehle exakt so wieder, wie sie im Dokument stehen, und nenne den Abschnitt.
```

### Prompt #6 – DHCP / Adressbereiche
```
Welche DHCP-Bereiche und statischen Adressen (z. B. für Server, Drucker, Management) sind im Dokument vorgesehen, und wie sollen Reservierungen gehandhabt werden?
```

### Prompt #7 – Checkliste
```
Erstelle aus der Dokumentation eine Checkliste für die Migration eines Standorts in ein neues IP-Konzept, die ein neuer Mitarbeiter Punkt für Punkt abarbeiten kann. Verwende nur Informationen aus der Knowledge Base.
```

### Prompt #8 – Firewall & Security (Kategorie aus Aufgabe)
```
Welche Ports müssen für RDP-Access freigeschaltet werden, und welche Sicherheitsvorgaben gelten dafür laut Dokumentation?
```
*(Je nach Dokumentenlage kann hier „nicht gefunden" die richtige Antwort sein.)*

### Prompt #9 – VPN (Kategorie aus Aufgabe)
```
Wie richte ich eine Site-to-Site-VPN-Verbindung mit WireGuard ein? Beantworte nur anhand der bereitgestellten Dokumente und sage klar, wenn dazu nichts enthalten ist.
```

### Prompt #10 – Zusammenhang VLAN ↔ Firewall/Routing
```
Welche Auswirkungen hat die Einführung eines neuen VLANs auf Routing und Zugriffsregeln zwischen den Segmenten, und was sollte ich laut Dokumentation dabei zusätzlich beachten?
```

### Prompt #11 – Negativtest (Halluzinationsprüfung)
```
Welche Backup-Strategie für den Exchange-Server empfiehlt Alexander Vogel in seiner Dokumentation?
```
*Erwartung: Das Modell sollte angeben, dass dazu nichts in der Knowledge Base steht. Bewerte, ob es das tut oder etwas erfindet.*

### Prompt #12 – Quellenpräzision / Wortlaut
```
Zitiere die Passage, in der die Vorgehensweise zur Verifikation nach einer Migration beschrieben wird (maximal 5 Sätze), und nenne Dokument sowie Seite oder Abschnitt.
```

---

### 4.1 Protokollvorlage (pro Prompt kopieren)

```markdown
#### Prompt #⟦N⟧
**Prompt (wörtlich):**
> ⟦...⟧

**Antwort (vollständig):**
> ⟦...⟧

**Angezeigte Quellen:**
- ⟦Dokument, Abschnitt/Seite, ggf. [cite:knowledge:N]⟧

**Bewertung:** ⟦x/5⟧ ⭐
- Technisch korrekt? ⟦ja/teilweise/nein, Begründung. Abgleich mit dem Originaldokument!⟧
- Quellenangaben hilfreich? ⟦...⟧
- Würde ich die Antwort im NOC weitergeben? ⟦ja/nein, warum⟧
```

### 4.2 Übersichtstabelle (am Ende der Abgabe)

| # | Kategorie | Technisch korrekt | Quellen hilfreich | NOC-tauglich | Gesamt (1–5) |
|---|---|---|---|---|---|
| 1 | VLAN | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 2 | IP-Planung | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 3 | Migration | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 4 | Rollback | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 5 | Switch-Config | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 6 | DHCP | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 7 | Checkliste | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 8 | Firewall | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 9 | VPN | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 10 | VLAN+Security | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 11 | Negativtest | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| 12 | Zitat | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |

---

## 5. Schritt 4 (Bonus): RAG-Parameter vergleichen

### 5.1 Vorgehen

1. **Variante A:** `RAG_TOP_K = 3`, `RAG_RELEVANCE_THRESHOLD = 0.8`
2. **Variante B:** `RAG_TOP_K = 10`, `RAG_RELEVANCE_THRESHOLD = 0.5`

Umstellen entweder in *Admin Panel → Settings → Documents* (Top K / Relevance Threshold) **oder** über das Start-Skript:

```bash
# Variante A
export RAG_TOP_K="3"; export RAG_RELEVANCE_THRESHOLD="0.8"
# Variante B
export RAG_TOP_K="10"; export RAG_RELEVANCE_THRESHOLD="0.5"
```

> Achtung: Wegen der persistenten Konfiguration (siehe Hinweis oben) die Werte **in der UI kontrollieren**, sonst testest du unbemerkt zweimal dieselbe Einstellung.

3. Dieselben **vier Testprompts** in beiden Varianten stellen, je in neuem Chat:

| Testprompt | Zweck |
|---|---|
| #2 (IP-Schema als Tabelle) | Präzisions-/Fakten-Abfrage (Quick-Fix) |
| #5 (Switch-Befehle exakt) | Exakte Befehle, Gefahr von Vermischung |
| #3 (Migrationsablauf komplett) | Deep-Dive, benötigt viel Kontext |
| #11 (Negativtest Exchange) | Halluzinations-/Rauschverhalten bei niedrigem Threshold |

### 5.2 Ergebnistabelle

| Testprompt | Variante A: Quellenanzahl | A: Qualität (1–5) | Variante B: Quellenanzahl | B: Qualität (1–5) | Auffälligkeiten |
|---|---|---|---|---|---|
| #2 | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| #5 | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| #3 | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| #11 | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ | ⟦⟧ |

### 5.3 Reflexion (100–200 Wörter) – Gerüst zum Ausformulieren

Beantworte mit deinen eigenen Beobachtungen:

- **Welche Variante war technisch präziser?** *(Hypothese zum Überprüfen: Variante A liefert wenige, hochrelevante Chunks und damit weniger Rauschen, riskiert aber, relevante Passagen ganz zu verpassen. Bei strengem Threshold kann auch „keine Treffer" auftreten.)*
- **Welche Variante lieferte mehr Kontext / vollständigere Skripte?** *(Hypothese: Variante B, da mehr Chunks, aber evtl. mit irrelevanten Abschnitten und höherem Verbrauch des Kontextfensters eines 8B-Modells.)*
- **Empfehlung:** *Quick-Fix* (z. B. „Welcher Port/Befehl?") → eher A; *Deep-Dive* (z. B. kompletter Migrationsablauf, Checkliste) → eher B. Begründe das mit **deinen** Messungen. Falls sie der Hypothese widersprechen, ist das ein wertvolleres Ergebnis. Gib auch an, wenn das Kontextfenster des lokalen Modells bei Variante B ein Limit war.

⟦Dein Text, 100–200 Wörter⟧

---

## 6. Reflexion zur Gesamtqualität (Vorschlag für die Abgabe)

Gehe auf diese Punkte ein, gestützt auf deine Protokolle:

1. **Korrektheit:** Wie oft stimmte die Antwort nachweislich mit dem Originaldokument überein? Wo wurden Details vermischt oder ergänzt?
2. **Halluzinationen:** Verhalten bei Prompt #8, #9, #11 (Inhalt nicht im Dokument). Wurde „nicht gefunden" gesagt oder aus allgemeinem Modellwissen geantwortet, und wurde dies kenntlich gemacht?
3. **Quellenqualität:** Waren Chunks sinnvoll abgegrenzt? Wurden Tabellen und Codeblöcke aus dem PDF korrekt extrahiert (typische Schwäche bei PDFs)?
4. **Modellgröße:** Einfluss des lokalen 8B-Modells auf Reasoning und Formatierung.
5. **Praxistauglichkeit:** Eignung für neue Mitarbeiter, Risiken bei sicherheitskritischen Konfigurationen (immer gegen das Original prüfen), mögliche Verbesserungen (Chunk-Größe, Hybrid Search, Reranker, bessere Dokumentstruktur, Markdown statt PDF).

---

## 7. Abgabe-Checkliste

- [ ] `start-rag.sh` als Code-Snippet
- [ ] Screenshot Knowledge-Panel (alle Dokumente „Ready")
- [ ] ≥ 10 Prompts im Protokollformat (wörtlicher Prompt, vollständige Antwort, Quellen, Bewertung)
- [ ] Übersichtstabelle
- [ ] Bonus: Varianten A/B, Ergebnistabelle, Reflexion (100–200 Wörter)
- [ ] Gesamtreflexion

---

## 8. Troubleshooting (Linux Mint)

| Problem | Lösung |
|---|---|
| `uv: command not found` | Neues Terminal öffnen oder `source ~/.bashrc`; uv liegt in `~/.local/bin` |
| `python --version` zeigt nicht 3.11 | venv nicht aktiviert (`source ~/rag/venv/bin/activate`) oder ohne `--python 3.11` angelegt |
| Kein Modell in Open WebUI sichtbar | LM Studio Server läuft? `curl http://localhost:1234/v1/models`; in Open WebUI unter *Admin → Settings → Connections* die URL `http://localhost:1234/v1` prüfen |
| LM Studio AppImage startet nicht | `sudo apt install libfuse2` (bzw. `libfuse2t64`); sonst mit `--no-sandbox` starten |
| `permission denied` bei Docker | Benutzer nicht in Gruppe `docker`: `sudo usermod -aG docker $USER`, danach neu anmelden |
| Verbindung zu PostgreSQL schlägt fehl | `docker ps`, Port 5432 belegt? (`ss -tlnp \| grep 5432`); Zugangsdaten in `DATABASE_URL` prüfen |
| Port 8080 belegt | `PORT` im Skript ändern, z. B. auf `3000` |
| Dokument bleibt auf „Processing" | Erster Start lädt Embedding-Modell herunter; Terminal beobachten |
| Antworten ohne Quellen | Collection im Chat nicht ausgewählt (`#` bzw. „+") |
| Immer „keine Treffer" | Threshold zu hoch; testweise 0.5 setzen und beobachten |
| PDF-Text unleserlich | PDF evtl. gescannt → OCR nötig oder Inhalt als Markdown/TXT bereitstellen |