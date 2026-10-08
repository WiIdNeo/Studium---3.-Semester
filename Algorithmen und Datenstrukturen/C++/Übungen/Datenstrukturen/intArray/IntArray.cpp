#include <malloc.h>
#include <iostream>

class IntArray {
    public:
        IntArray() {
            capacity = 0;
            pointer = nullptr;
        }
        void push_back(int value) {
            if (capacity == 0) {
                pointer = (int*)malloc(sizeof(int));
                pointer[0] = value;
                capacity = 1;
            }
            else {
                int* tmp = (int*)realloc(pointer, (capacity +1) * sizeof(int));
                if (tmp == nullptr) {
                    std::cout << "Ein Fehler ist aufgetreten, Anhängen ist fehlgeschlagen";
                    return;
                }
                pointer = tmp;
                pointer[capacity] = value;
                capacity++;
            }
        }
        int get(int index) {
            if (index < 0 || index >= capacity) {
                std::cout << "Index Out of Range";
                return -1;
            }
            return pointer[index];
        }
        int size() {
            return capacity;
        }
        int find(int value) {
            for (int i = 0; i < capacity; i++) {
                if (value == pointer[i]) {
                    return i;
                }
            }
            return -1; //negativer index -> Fehler
        }
        void clear() {
            free(pointer);
            pointer = nullptr;
            capacity = 0;
        }
        ~IntArray() {
            free(pointer);
            pointer = nullptr;
        }
    private:
        int capacity;
        int* pointer;
};