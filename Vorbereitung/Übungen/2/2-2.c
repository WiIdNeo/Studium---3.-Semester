int main() {
    int x;
    scanf("%d", &x);

    switch (x)
    {
    case 90 ... 100:
        printf("Sehr gut");
        break;
    case 75 ... 89: 
        printf("Gut");
        break;
    case 60 ... 74:
        printf("Befriedigend");
        break;
    case 50 ... 59:
        print("Ausreichend");
    default:
        printf("Nicht bestanden");
        break;
    }
    return 0;
}