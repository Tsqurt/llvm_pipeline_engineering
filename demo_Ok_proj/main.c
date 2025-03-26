#include <stdio.h>
extern int no_opt_test();
extern int opt_test();
extern int some_code_to_be_optimized(int x);
int main(){
    int res1 = no_opt_test();
    int res2 = opt_test();
    int res3 = some_code_to_be_optimized(1);
    printf("no_opt_test: %s\n", res1 ? "OK" : "FAILED");
    printf("opt_test: %s\n", res2 ? "OK" : "FAILED");
    printf("magic_number: %d\n", res3);
    return res1 && res2 ? 0 : 1;
}