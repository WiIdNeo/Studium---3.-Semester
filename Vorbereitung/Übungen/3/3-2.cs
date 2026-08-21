using System.Diagnostics.CodeAnalysis;

namespace Uebung;

class Program
{
    static void Main(string[] args)
    {
        List<int> i = new List<int>() {1, 2, 3, 4};
        int sum = 0;

        foreach (int y in i)
        {
            sum += y;
        }
        Console.WriteLine(sum);
    }
}