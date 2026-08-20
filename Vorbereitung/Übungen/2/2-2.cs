namespace Uebung;

class Program {
    static void Main(string [] Args) {
        int x = Console.ReadLine();

        string Note = x switch {
            int p when p <= 100 && p >= 90 => "Sehr gut",
            int p when p < 90 && p >= 75 => "Gut",
            int p when p < 75 && p >= 60 => "Befriedigend",
            int p when p < 60 && p >= 50 => "Ausreichend"
            _ => "Nicht bestanden"
        };

        print(Note);
    }
}