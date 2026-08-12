namespace Uebung;

class Program {
    static void Main(string[] Args) {
        int x = int.Parse(Console.ReadLine());
        int y = int.Parse(Console.ReadLine());

        bool z = GreaterThan(x, y);
        Console.WriteLine(z);
    }
    static bool GreaterThan(int x, int y) {
        return x > y;
    }
}