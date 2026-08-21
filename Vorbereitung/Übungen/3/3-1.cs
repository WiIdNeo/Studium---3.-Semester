namespace Uebung;

class Program
{
    static void Main(string[] args)
    {
        List<int> x = new List<int>();
        foreach (int i in [1, 2, 3, 4, 5])
        {
            x.Add(i);
        }
        foreach (int i in x)
        {
            Console.WriteLine(i);
        }
    }
}