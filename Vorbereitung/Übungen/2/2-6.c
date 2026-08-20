int fib(int x) {
    if (x == 0) {
        return 1;
    }
    if (x == 1) {
        return 2;
    }
    else {
        return x + x-1;
    }
}

int main() {
    int a;
    scanf("%d", a);
    printf("Die %d. Fibonacci-Zahl ist %d", a, fib(a));
}

