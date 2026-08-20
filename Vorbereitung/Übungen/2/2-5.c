#include <stdio.h>
#include <stdlib.h>

int main() {
    int num;
    scanf("%d", &num);
    print("Die Fakultät von %d ist %d", num, fac(num));
    return 0;
}
int fac(x) {
    if (x == 1 || x == 0) {
        return 0;
    }
    if (x < 0) {
        print("Für negative Werte nicht definiert");
        exit(EXIT_SUCCESS);
    }
    return x * fac(x-1);
}