#include "DoppeltVerketteteListe.hpp"
#include <iostream>
#include <stdexcept>

template <typename T>
Liste<T>::Liste(T input)
    : head(nullptr), tail(nullptr), size(1)
{
    head = new val{nullptr, nullptr, input};
    tail = head;
}

template <typename T>
void Liste<T>::Add(T input) {
    val* n = new val{tail, nullptr, input};  // previous = alter tail (bei leerer Liste nullptr)

    if (head == nullptr) {
        head = n;            // Liste war leer
    } else {
        tail->next = n;      // alter letzter Knoten zeigt auf den neuen
    }

    tail = n;
    ++size;
}

template <typename T>
void Liste<T>::Delete(int index) {
    if (index < 0 || index >= size) {
        return;   // oder: throw std::out_of_range("...");
    }

    val* current = head;
    for (int i = 0; i < index; i++) {
        current = current->next;
    }

    // Vorgänger umhängen
    if (current->previous != nullptr) {
        current->previous->next = current->next;
    } else {
        head = current->next;        // current war der erste Knoten
    }

    // Nachfolger umhängen
    if (current->next != nullptr) {
        current->next->previous = current->previous;
    } else {
        tail = current->previous;    // current war der letzte Knoten
    }

    delete current;
    size--;
}

template <typename T>
int Liste<T>::GetSize() {
    return size;
}

template <typename T>
T Liste<T>::GetValue(int index) {
    if (index < 0 || index >= size) {
        throw std::out_of_range("Index außerhalb der Liste");
    }

    val* current = head;
    for (int i = 0; i < index; i++) {
        current = current->next;
    }
    return current->value;
}

template <typename T>
int Liste<T>::GetIndex(T value) {
    val* current = head;
    for (int i = 0; i < size; ++i) {
        if (current.value == value) {
            return i;
        }
        current = current->next;
    }    
    std::cout << "Kein Gültiger Index gefunden";
    return -1;
}

template <typename T>
Liste<T>::~Liste() {
    for (int i = 0; i < size; ++i) {
        Delete(head);
    }
    // Wie die Klasse selbst löschen?
}

template <typename T>
void Iterator<T>::createIterators(Liste<T> list) {
    current = list.head;
    first = current;
    end = nullptr;
}

template <typename T>
void Iterator<T>::operator++() {
    current = current->next;
}

template <typename T>
void Iterator<T>::operator--() {
    current = current->previous;
}

template <typename T>
void Liste<T>::Delete(val* a) {
    if (a == nullptr) return;

    if (a->previous != nullptr)
        a->previous->next = a->next;
    else
        head = a->next;          // a war der erste Knoten

    if (a->next != nullptr)
        a->next->previous = a->previous;
    else
        tail = a->previous;      // a war der letzte Knoten

    delete a;
    --size;
}
template <typename T>
T GetValue(val* a) {
    if (a != nullptr) {
        return a->current;
    };
};