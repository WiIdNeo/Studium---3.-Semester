# Reflexion

Ich habe ein kleines lokales Modell (qwen2.5-coder) mit Continue und Cline genutzt.

## Autovervollständigung

Der erste Vorschlag hatte nur die Formel. Es fehlten die Rundung (A1) und der ValueError unter dem absoluten Nullpunkt (A2).

## Chat

- A2 als fehlend erkannt
- A1 hat es als erfüllt gemeldet, obwohl kein `round()` im Code stand, nur abschneiden.

## Edit

Das Modell hat bereits `<` geschrieben.

## Cline

| Freigabe | Bewilligt|
|---|---|
| `pip install pytest` | +|
| `source .venv/bin/activate`   | +
| Code ändern, damit der Test passt |-: Der Test war falsch (-17,77 statt -17,78) |

## Was ich zusätzlich gefunden habe

- `nan` und `inf` werden von `float()` akzeptiert.
- `python temperatur.py -459,67` scheitert mit Exit-Code 2. argparse hält das für eine Option. Mit `--` davor geht es.

## Fazit

Am meisten geholfen hat die KI bei der Syntax. Das Gerüst für argparse, pytest und die Formatierung stand schnell.

Das Modell hat Anforderungen als erfüllt gemeldet, die nicht erfüllt waren. Ich musste alles selbst gegen A1 bis A6 prüfen. Das wäre mit einem größeren Modell sicher besser gegangen.
