#include <malloc.h>

class RingBuffer {
    public:
        RingBuffer(int capacity_) {
            if (capacity_ <= 0) {
                return;
            }
            data = (int*)malloc(capacity * sizeof(int));
            capacity = capacity_;
            filled = 0;
        }
        bool push(int v) {
            if (filled == capacity) {
                return false;
            }
            data[filled] = v;
            filled++;
            return true;
        }
        bool pop(int& out) {
            if (filled == 0) {
                return false;
            }
            out = data[0];
            data[0] = NULL; // ist null hier richtig? Also ist null der Originalzustand?
            rotate();
            filled--;
            return true;
        }
        bool empty() {
            return filled == 0;
        }
        bool full() {
            return filled == capacity;
        }
        int size() {
            return capacity - filled;
        }
        ~RingBuffer() {
            free(data);
            data = nullptr;
        }
    private:
        int capacity;
        int* data;
        int filled;
        void rotate() {
            int temp = data[0];
            for (int i = 1; i < capacity; i++) {
                data[i-1] = data[i];
            }
            data[capacity-1] = temp;
        }
};