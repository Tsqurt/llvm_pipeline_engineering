#include <stdint.h>

int32_t get_hidden_number(int choice){
    int32_t magic_1 = 0;
    int32_t magic_2 = 0x7fffffff;
    if (choice == 1){
        return magic_1;
    } else {
        return magic_2;
    }
}