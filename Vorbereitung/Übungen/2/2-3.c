int Main() {
    int Fizz[] = List(3);
    int Buzz[] = List(5);

    for (int i = 1; 31; i++) {
        int inFizz = 0;
        int inBuzz = 0;
        for (int z = 0; sizeof(Fizz)/sizeof(Fizz[0]); z++) {
            if (i == Fizz[z]) {
                inFizz = 1;
            }
        }
        for (int z = 0; sizeof(Buzz)/sizeof(Buzz[0]); z++) {
            if (i == Buzz[z]) {
                inBuzz = 1;
            }
        }
        if (inFizz == 1) {
            if (inBuzz == 1) {
                printf("FizzBuzz " + i);
            }
            else {
                printf("Fizz " + i);
            }
        }
        else {
            if (inBuzz) {
                printf("Buzz " + i);
            }
            else {
                printf(i);
            }
        }
        
    }
}

int List(int x) {
    int y = 0;
    int List[10];
    while (x * y < 30) {
        y++;
        List[y-1] = y * x;  
    };
    return List;
}