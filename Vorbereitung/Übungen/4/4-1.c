int main() {
    struct book
    {
        char title[100];
        char autor[50];
        int year;
    };
    
    struct book y = {
        "Test",
        "niemand",
        0
    };
}