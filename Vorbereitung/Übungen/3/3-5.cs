using Microsoft.VisualBasic;

namespace Uebung;

class Program
{
    static void Main()
    {
        int.TryParse(Console.ReadLine(), out int a);
        int.TryParse(Console.ReadLine(), out int b);
        var c = Funk(a, b);
        Console.WriteLine($"Die Summe aus {a} und {b} ist {c[0]}.\\Die Differenz ist {c[1]}");
    }
    static int Funk(int x, int y)
    {
        return (x+y, x-y);
    }
}