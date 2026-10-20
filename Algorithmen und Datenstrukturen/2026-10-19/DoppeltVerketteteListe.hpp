#ifndef DoppeltVerketteteListe_HPP
#define DoppeltVerketteteListe_HPP

template <typename T>
class Liste {
    struct val;
public:
    Liste(T input);
    void Add(T input);
    void Delete(int index);
    void Delete(val* a);
    int GetSize();
    T GetValue(int index);
    T GetValue(val* a);
    int GetIndex(T a);
    ~Liste();

private:
    struct val {
        val* previous;
        val* next;
        T value;
    };

    val* head;
    val* tail;
    int size;

    friend class Iterator;
};

template <typename T>
class Iterator {
    public:
        val* end;
        val* first;
        val* current;

        void operator++();
        void operator--();
    private:
        void createIterators(Liste<T> a);
        friend class Liste;
};
#endif