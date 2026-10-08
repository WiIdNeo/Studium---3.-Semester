#include <cstddef>   // nullptr

void swap_ints(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

bool min_max(const int* arr, int n, int& min, int& max) {
    if (arr == nullptr || n <= 0) return false;

    int lo = arr[0];
    int hi = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] < lo) lo = arr[i];
        if (arr[i] > hi) hi = arr[i];
    }
    min = lo;   // Ausgaben erst am Ende schreiben
    max = hi;
    return true;
}

void reverse(char* s, int n) {
    if (s == nullptr) return;
    for (int i = 0; i < n / 2; i++) {
        char temp = s[i];
        s[i] = s[n - 1 - i];
        s[n - 1 - i] = temp;
    }
}
