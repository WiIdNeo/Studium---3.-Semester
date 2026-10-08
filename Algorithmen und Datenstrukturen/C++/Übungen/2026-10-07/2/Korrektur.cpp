#include <cstdlib>

class RingBuffer {
public:
    RingBuffer(int capacity_) : data(nullptr), capacity(0), head(0), count(0) {
        if (capacity_ <= 0) return;
        data = (int*)malloc(capacity_ * sizeof(int));
        if (data == nullptr) return;     // capacity bleibt 0
        capacity = capacity_;
    }

    RingBuffer(const RingBuffer&) = delete;
    RingBuffer& operator=(const RingBuffer&) = delete;

    bool push(int v) {
        if (count >= capacity) return false;   // voll (oder kein Speicher)
        data[(head + count) % capacity] = v;
        count++;
        return true;
    }

    bool pop(int& out) {
        if (count == 0) return false;
        out = data[head];
        head = (head + 1) % capacity;
        count--;
        return true;
    }

    bool empty() const { return count == 0; }
    bool full()  const { return count == capacity; }
    int  size()  const { return count; }

    ~RingBuffer() {
        free(data);
        data = nullptr;
    }

private:
    int* data;
    int capacity;
    int head;
    int count;
};