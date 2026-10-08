#ifndef STRING_HPP
#define STRING_HPP

#include <cstddef>

class string {
public:
    string();
    string(const char* data);
    ~string();
    char* data();
    void clear();
    void print();
    int find(char c);
    void append(const char* data);

private:
    char* text;
    int laenge;
    static int count(const char* s);
};

#endif