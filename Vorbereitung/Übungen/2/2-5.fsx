let rec fac x =
    if x < 0 then
        failwith "Fakultäten für negative Werte sind nicht definiert"
    elif x <= 1 then
        1
    else
        x * fac (x - 1)

let y = System.Console.ReadLine() |> int
printfn "Die Fakultät von %d ist %d" y (fac y)

