namespace Uebung;

class Program {
    static int square(int x) {
        x = x * x;
        return x;
    }
    
    static void Main(string[] args) {
        int x = int.Parse(Console.ReadLine());
        x = square(x);
        Console.WriteLine(x);
    }
}