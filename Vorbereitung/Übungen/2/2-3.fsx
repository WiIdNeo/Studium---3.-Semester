let x : int = 3

let list1 =
    [ for i in 1 .. 30 do
        if i * x < 31 then
            yield i * x ]

let y : int = 5

let list2 =
    [ for i in 1 .. 30 do
        if i * y < 31 then
            yield i * y ]

for i in 1 .. 30 do
    if List.contains i list1 then
        if List.contains i list2 then
            printfn "FizzBuzz %d" i
        else
            printfn "Fizz %d" i
    else
        if List.contains i list2 then
            printfn "Buzz %d" i
        else
            printfn "%d" i