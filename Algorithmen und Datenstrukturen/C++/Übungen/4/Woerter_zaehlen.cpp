#include <iostream>
#include <string>
#include <sstream>
#include <unordered_map>
#include <cctype>
#include <fstream>

int main() {
    std::ifstream datei("./woerter.txt");
    if (!datei) {
        std::cerr << "Datei konnte nicht geöffnet werden\n";
        return 1;
    }

    std::stringstream buffer;
    buffer << datei.rdbuf();
    std::string text = buffer.str();   // <- das war der fehlende Schritt

    // 1. Lowercase + Sonderzeichen entfernen
    std::string clean;
    for (unsigned char c : text)
        if (std::isalnum(c) || std::isspace(c))
            clean += std::tolower(c);

    // 2. Entlang von Whitespace splitten und gleichzeitig zählen
    std::unordered_map<std::string, int> counts;
    std::istringstream iss(clean);
    std::string word;
    while (iss >> word)
        ++counts[word];

    // 3. Ausgeben
    for (const auto& [w, n] : counts)
        std::cout << w << ": " << n << '\n';
}