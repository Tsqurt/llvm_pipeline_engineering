#include <stdint.h>

extern int32_t get_hidden_number(int choice);

static int test(int32_t x){
    return x < x + 1;
}

// returns 1 if this file has no optimizations
int no_opt_test(){
    return test(get_hidden_number(1)) && !test(get_hidden_number(2));
}