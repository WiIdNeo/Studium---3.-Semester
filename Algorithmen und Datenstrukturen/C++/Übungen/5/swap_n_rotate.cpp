#include <vector>
#include <iostream>

template <typename T>
void swap_elements(std::vector<T>& v, size_t a, size_t b) {
    T temp = v[a];
    v[a] = v[b];
    v[b] = temp;
}

template <typename T>
void shift(std::vector<T>& v, int n) {
    if (v.empty()) return;
    for (int j = 0; j < n; j++) {
        T temp = v[0];
        for (size_t i = 1; i < v.size(); i++) {
            v[i - 1] = v[i];
        }
        v.back() = temp;
    }
}

template <typename T>
void print(const std::vector<T>& v) {
    for (const T& x : v) std::cout << x << ' ';
    std::cout << '\n';
}

int main() {
    std::vector<int> vec;
    for (int i = 0; i < 3; i++) {
        int x;
        std::cin >> x;
        vec.push_back(x);
    }

    print(vec);
    swap_elements(vec, 0, 1);
    print(vec);
    shift(vec, 2);
    print(vec);
}