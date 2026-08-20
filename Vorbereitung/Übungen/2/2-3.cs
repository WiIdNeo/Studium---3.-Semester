namespace Uebung;

class Program
{
    static void Main(string[] args)
    {
        var a = List(3);
        var b = List(5);

        for (int i = 1; i < 31; i++)
        {
            if (a.Contains(i))
            {
                if (b.Contains(i))
                {
                    Console.WriteLine($"FizzBuzz {i}");
                }
                else
                {
                    Console.WriteLine($"Fizz {i}");
                }
            }
            else if (b.Contains(i)) {
                Console.WriteLine($"Buzz  {i}");
            }
            else
            {
                Console.WriteLine(i);
            }
        }
    }
    static int[] List(int x)
    {
        List<int> y = new List<int>();

        for (int i = 1; i * x < 31; i++)
        {
            y.Add(i * x);
        }

        return y.ToArray();
    }
}