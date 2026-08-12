int square(int x) {
    x = x * x;
    return x;
}

int main() {
    int x;
    scanf("%d", &x);

    x = square(x);
    
    printf(x);
}