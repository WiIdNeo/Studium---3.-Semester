#include "string.hpp"
#include <iostream>

int main() {
    string s("Hallo");
    s.append(" Welt!"); 
    s.print(); // Hallo Welt!
    s.append(nullptr); 
    s.append("");
    s.print(); // Wallo Welt!
    std::cout << s.find('1'); // -1
    std::cout << s.find('e'); // 7
    s.clear();
    s.print(); // ""
    return 0;
}