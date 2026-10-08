#include <iostream>
#include <cstdlib>

class Stack {
public:
    Stack(int capacity_) : data(nullptr), capacity(0), filled(0) {
        if (capacity_ <= 0) {
            std::cout << "Wähle eine Kapazität von über 0.\n";
            return;
        }
        data = (char*)malloc(capacity_);
        if (data == nullptr) {
            std::cout << "Speicher konnte nicht angelegt werden.\n";
            return;
        }
        capacity = capacity_;
    }

    bool push(char c) {
        if (filled >= capacity) return false;  // voll (oder kein Speicher)
        data[filled++] = c;
        return true;
    }

    bool pop(char& out) {
        if (filled == 0) return false;         // leer
        out = data[--filled];
        return true;
    }

    bool empty() { return filled == 0; }
    int size()   { return filled; }

    ~Stack() {
        free(data);
        data = nullptr;
    }

private:
    char* data;
    int capacity;
    int filled;
};