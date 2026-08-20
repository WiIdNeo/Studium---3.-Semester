namespace Uebung;

class Program
{
    static void Main()
    {
        int x = Console.ReadLine();
        Console.WriteLine($"Die {x}. Fibonacci Zahl ist {Fib(x)}.");
    }
    static int Fib(int x)
    {
        if (x == 1)
        {
            return 2;
        }
        if (x == 0)
        {
            return 1;
        }
        else
        {
            return x + x-1;
        }
    }
}