let value : int = int (System.Console.ReadLine())

let note : string = 
    match value with
    | p when p >= 90 && p <= 100 -> "Sehr gut"
    | p when p >= 75 && p < 90  -> "Gut"
    | p when p >= 60 && p < 75  -> "Befriedigend"
    | p when p >= 50  && p < 60  -> "Ausreichend"
    | _ -> "Nicht bestanden"

printfn "%s" note