#include <stdio.h>

int i[] = {1, 2, 3, 4, 6, 5};

int biggest = 0;

for (int y = 0; y < sizeof(i)/sizeof(i[0]); y++)
{
    if (y > biggest) {
        biggest = y;
    }
}

printf(biggest)
