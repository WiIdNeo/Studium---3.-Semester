#include <iostream>
#include <vector>

int main() {
    int dimensionen{};
    std::cout << "Wie viele Dimensionen hat dein Vektor?: ";
    if (!(std::cin >> dimensionen) || dimensionen <= 0) {
        std::cerr << "Bitte eine positive ganze Zahl eingeben.\n";
        return 1;
    }

    std::vector<double> vec(dimensionen);   // dimensionen Elemente, alle 0.0

    std::cout << "Gib nun alle Werte einzeln an\n";
    for (std::size_t i = 0; i < vec.size(); ++i) {
        std::cout << "Dimension " << i << ": ";
        if (!(std::cin >> vec[i])) {
            std::cerr << "Das war keine Zahl.\n";
            return 1;                        // kein Leck, vec räumt sich selbst auf
        }
    }

    std::cout << "(";
    for (std::size_t i = 0; i < vec.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << vec[i];
    }
    std::cout << ")\n";
}