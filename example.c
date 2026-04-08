#include <stdio.h>

int main() {
    int t;
    scanf("%d", &t);

    while (t--) {
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);

        int sum = a + b + c;
        int product = a * b * c;

        printf("Sum: %d, Product: %d\n", sum, product);
    }

    return 0;
}