#include <vector>
#include <iostream>

int main() {
    std::vector<int> Primzahlen;
    Primzahlen.push_back(2);

    int n = 100;
    bool probably = false;
    for (int i = 2; i <= n; i++) {
        probably = true;
        for (const auto& x : Primzahlen)  { // Wieso wird die Addresse hier automatisch dereferenziert, macht auto das?
            if (i%x == 0) {
                probably = false;
                break;
            }  
        }
        if (probably) {
            Primzahlen.push_back(i);
        }
    }

    for (int i = 0; i < Primzahlen.size(); i++) {
        std::cout << Primzahlen[i] << ' ';
        if ((i + 1) % 10 == 0) {
            std::cout << '\n';
        }
    }
    std::cout << '\n';
}