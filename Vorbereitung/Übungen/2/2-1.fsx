let a: int = int (System.Console.ReadLine())

// Bedingung
if a % 2 = 0 then 
    printfn "Gerade"
else
    printfn "Ungerade"

// Match-case
let f a = 
    match (a % 2) with 
    | 0 -> "Gerade"
    | _ -> "Ungerade"

printfn "%s" (f a)
