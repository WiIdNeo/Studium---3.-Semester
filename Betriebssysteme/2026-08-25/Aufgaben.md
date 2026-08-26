# 1
## a

- Benutzeroberfläche
- Ausführungsoberfläche für Programme

## b


## c

Kann das Stapelsystem keine Paralellität?

## d

## e

- Der Kernel ist das eigentliche Betriebssystem abzüglich der Zusatzsoftware. Er macht die Abstrahierung der Hardware und übernimmt die Kommunikation mit ihr.

## f

# 2

## a

## b

open() übernimmt das erkennen des Dateityps, der größe und das starten der geeigneten Darstellungssoftware. Ansonsten müsste je nach Dateityp ein anderer Befehl genutzt werden.

## c

## d

In C#, kann man in einem Subprocess die Bash öffnen und die Befehle direkt dort ausführen. Es existieren jedoch auch Funktionen, die über eine Biblioteksfunktion die Aufrufe an das Betriebssystem stellen.

## e

```csharp
using System;
using System.IO;

class Program {
    static void Main(string[] args) {
        Directory.CreateDirectory("./mittagessen");
        File.WriteAllText("./mittagessen/ramen.txt", "noodles meat shrooms")
    }
}
```

## f

```csharp
using System;

class Program {
    static async Task Main(string[] args) {
        await StartScript();
        Environment.Exit(0);
    }

    public static async Task StartScript() {
        var startInfo = new ProcessStartInfo
        {
            FileName = "/bin/bash",
            Arguments = $"-c \"{egZurAusführbarenDatei}\"",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using var process = new Process { StartInfo = startInfo };
        process.Start();
        await process.WaitForExitAsync();

    }
}
```

## g

## h

In der Client-Server-Architektur hat man einen Client und mehrere Server und beim Verteilten Betriebssystem ist jeder Teilnehmer Client und Server zugleich.

## i

