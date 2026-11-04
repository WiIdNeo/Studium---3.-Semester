#ifndef SUCHBAUM_HPP
#define SUCHBAUM_HPP

template<typename T>
struct node {
    node* parent;
    node* left_child;
    node* right_child;
    T value;
};
template<typename T>
class tree {
    public:
        inline tree() {
            root = nullptr;
            size = 0;
        }
        inline void insert(T value) {
            node<T>* current = root;
            node<T>* current_par = nullptr;
            while (true) {
                if (current == nullptr) {
                    root = new node<T>{current_par, nullptr, nullptr, value};
                    ++size;
                    return;
                }
                else if (value == current->value) {
                    return;
                }
                else if (value < current->value) {
                    current_par = current;
                    current = current->left_child;
                }
                else {
                    current_par = current;
                    current = current->right_child;
                }
            }
        }
        void erase(T value) {
            node<T>* current = root;
            while (true) {
                if (current == nullptr) {
                    return;
                }
                else if (current->value == value) {

                }
            }
        }
        inline ~tree() {
            while (root != nullptr) {
                delete(root);
            }
        }
    private:
        int size;
        node<T>* root;
};

#endif
