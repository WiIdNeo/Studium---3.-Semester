let l = [1;2;3;4;7;5;6]

let mutable max = 0;

for i in l do
    if max < i then
        max <- i

printfn "%d" max