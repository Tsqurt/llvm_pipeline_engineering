#include <stdio.h>

// Clang only availability 
__attribute__((availability(macos,introduced=10.10,deprecated=10.12,obsoleted=10.14)))
void oldFunction(void) {
    printf("oldfucntion\n");
}

int main() {
    oldFunction();  
    return 0;
}