#include <format>
#include <iostream>

double calc(int celsius) {
    return celsius * 9.0 / 5.0 + 32.0;
}

int main() {
    std::cout << "    °C     °F\n";
    for (int i = -20; i <= 40; i += 5) {
        std::cout << std::format("{:6} {:6.1f}\n", i, calc(i));
    }
    return 0;
}