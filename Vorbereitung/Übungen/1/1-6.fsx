let GreaterThan (x: int) (y: int) = x>y

let x: int = int (System.Console.ReadLine())
let y: int = int (System.Console.ReadLine())

let a: bool = GreaterThan x y

printfn "%b" a