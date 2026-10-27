class binary_search_tree {
    public:
        struct Knoten
        {
            int value;
            Knoten* parent;
            Knoten* left;
            Knoten* right;
        };
        binary_search_tree(int value) {
            root = new Knoten{value, nullptr, nullptr, nullptr};
            size = 1;
        }
        binary_search_tree() {
            root = nullptr;
            size = 0;
        }
        void insert(int value) {
            if (size != 0) {
                Knoten* current = root;
                while (true) {
                    if (value < current->value && current->left) {
                        current = current->left;
                    }
                    else if (value > current->value && current->right) {
                        current = current->right;
                    }
                    else if (value < current->value && !current->left) {
                        current->left = new Knoten{value, current, nullptr, nullptr};
                        ++size;
                        break;
                    }
                    else if (value > current->value && !current->right) {
                        current->right = new Knoten{value, current, nullptr, nullptr};
                        ++size;
                        break;
                    }
                }
            }
            else {
                root = new Knoten{value, nullptr, nullptr, nullptr};
                ++size;
            }
        }
        Knoten* search(int value) {
            if (size == 0) {
                return nullptr;
            }
            Knoten* current = root;
            while (true) {
                if (current->value == value) {
                    return current;
                }
                else if (value < current->value) {
                    if (current->left) {
                        current = current->left;
                    }
                    else {
                        return nullptr;
                    }
                }
                else {
                    if (current->right) {
                        current = current->right;
                    }
                    else {
                        return nullptr;
                    }
                }
            }
        }
        Knoten* next_greater(int value) {
            if (root) {
                return nullptr;
            }
            Knoten* current = root;
            Knoten* cnext_greater = nullptr;
            while (true) {
                if (value < current->value) {
                    cnext_greater = current;
                    if (current->left) {
                        current = current->left;
                    }
                    else {
                        return cnext_greater;
                    }
                }
                else if (value >= current->value) {
                    if (current->left) {
                        current = current->left;
                    }
                    else {
                        return cnext_greater;
                    }
                }
            }
        }
    private:
        int size;
        Knoten* root;
};


int main() {



    return 0;
}