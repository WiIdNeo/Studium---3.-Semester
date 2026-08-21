int main() {
    int x[] = {1, 2, 3, 4};
    int sum = 0;
    for (int i = 0; i < sizeof(x)/sizeof(x[0]); i++) {
        sum = sum + x[i];
    }
}