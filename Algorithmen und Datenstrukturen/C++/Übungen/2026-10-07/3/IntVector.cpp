#include <malloc.h>

class IntVector {
    public:
        IntVector() {
            data = (int*)malloc(4 * sizeof(int));
            capacity = 4;
            filled = 0;
        }
        bool push_back(int v) {
            if (capacity == filled) {
                capacity = capacity*2;
                data = (int*)realloc(data, sizeof(int)*capacity);
            }
            data[filled] = v;
            filled++;
        } 
        bool get(int index, int& out) {
            if (index >= filled) {
                return false;
            }
            out = data[index];
            return true;
        }
        bool pop_back(int &out) {
            if (filled == 0) {
                return false;
            }
            out = data[filled-1];
            filled--;
            return true;
        }
        int size() {
            return filled;
        }
        int get_capacity() {
            return capacity;
        }
        ~IntVector() {
            free(data);
            data = nullptr;
        }
    private:
        int* data;
        int capacity;
        int filled;
};