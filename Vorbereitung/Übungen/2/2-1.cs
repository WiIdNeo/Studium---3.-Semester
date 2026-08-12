namespace Uebung;

class Program {
    static void Main(string [] args) {
        int x = Console.ReadLine();

        // Bedingung

        if (x%2 == 0) {
            Console.WriteLine("Gerade");
        }
        else {
            Console.WriteLine("Ungerade");
        }

        // switch-case
        string IsFlat = x%2 switch {
            0 => "Gerade",
            _ => "Ungerade"
        }

        Console.WriteLine(IsFlat);
    }
}