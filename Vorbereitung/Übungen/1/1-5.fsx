let square (x: int) = x * x

let mutable x: int = int (System.Console.ReadLine())

x <- square x

printfn "%d" x