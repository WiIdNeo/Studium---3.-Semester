namespace Uebung;

class Program
{
    static void Main(string [] args)
    {
        int x = Console.ReadLine();
        Console.WriteLine($"Die Fakultät von {x} ist {Fac(x)}");
    }
    static int Fac(int x)
    {
        if (x == 1 || x == 0)
        {
            return 0;
        }
        if (x < 0)
        {
            Console.WriteLine("Fakultät für negative Werte nicht definiert.");
            Environment.Exit(0);
        }
        return x * Fac(x-1);
    }
}