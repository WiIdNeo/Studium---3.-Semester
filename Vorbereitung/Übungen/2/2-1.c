int main() {
    int x;
    scanf("%d",  &x);

    // Bedingung
    if (x%2 == 0) {
        printf("Gerade");
    }
    else {
        printf("Ungerade");
    }

    //switch-case
    switch (x%2) {
        case 0:
            printf("Gerade");
            break;
        default:
            print("Ungerade");
    }
}