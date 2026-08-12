namespace Uebung;

class Program() {
    static void Main(string[] Args) {
        int a = int.Parse(Console.ReadLine());
        int b = int.Parse(Console.ReadLine());

        Console.WriteLine($"Fläche: {a * b}");
    }
}