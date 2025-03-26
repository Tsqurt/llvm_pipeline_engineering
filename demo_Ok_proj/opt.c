#include <stdint.h>

extern int32_t get_hidden_number(int choice);

static int test(int32_t x){
    return x < x + 1;
}

// returns 1 if this file has optimizations
int opt_test(){
    return test(get_hidden_number(1)) && test(get_hidden_number(2));
}

int some_code_to_be_optimized(int x){
    int result = x;
    
    int buffer[1000];
    
    for (int i = 0; i < 1000; i++) {
        buffer[i] = (i * x) % 997;
    }
    
    for (int iter = 0; iter < 100; iter++) {
        for (int i = 0; i < 999; i++) {
            for (int j = 0; j < 999 - i; j++) {
                if (buffer[j] > buffer[j + 1]) {
                    int temp = buffer[j];
                    buffer[j] = buffer[j + 1];
                    buffer[j + 1] = temp;
                }
            }
        }

        result = (result * 31 + buffer[iter % 1000]) % 0x7fffffff;
        
        for (int i = 0; i < 1000; i++) {
            buffer[i] = (buffer[i] * result + i) % 997;
        }
    }
    
    int sum = 0;
    for (int i = 0; i < 1000; i++) {
        sum += buffer[i];
    }
    
    return (result + sum) % 0x7fffffff;
}