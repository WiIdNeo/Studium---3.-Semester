int greaterThan(int a, int b) {
    if (a > b) {
        return 1;
    }
    return 0;
}

int main() {
    int a;
    int b;
    scanf("%d", &a);
    scanf("%d", &b);

    int c = greaterThan(a, b);
    printf("%d", c);
}