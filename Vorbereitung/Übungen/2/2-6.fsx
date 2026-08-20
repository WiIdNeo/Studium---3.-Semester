let rec fib y =
    if y = 0 then
        1
    elif y = 1 then
        2
    else
        fib (y - 1) + fib (y - 2)

let y = System.Console.ReadLine() |> int

printfn "Die %d. Fibonacci-Zahl ist %d." y (fib y)