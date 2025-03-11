#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// A complex test case to stress test O2 optimization
// Includes:
// 1. Complex control flow with nested loops
// 2. Memory operations and pointer arithmetic
// 3. Function calls with multiple parameters
// 4. Bit manipulation
// 5. Array operations with dynamic allocation
#define SIZE 1000

int calculate_checksum(int* arr, int size) {
    int checksum = 0;
    for (int i = 0; i < size; i++) {
        checksum = ((checksum << 5) + checksum) + arr[i];
    }
    return checksum;
}

void transform_array(int* arr, int size, int key) {
    for (int i = 0; i < size; i++) {
        arr[i] = (arr[i] ^ key) + ((arr[i] << 4) | (arr[i] >> 28));
        if (i > 0) {
            arr[i] += arr[i-1];
        }
    }
}

int main() {
    int* data = (int*)malloc(SIZE * sizeof(int));
    int result = 0;
    
    // Initialize array with pseudo-random values
    for (int i = 0; i < SIZE; i++) {
        data[i] = (i * 1103515245 + 12345) & 0x7fffffff;
    }
    
    int iterations;
    scanf("%d", &iterations);
    // Multiple iterations of transformations
    for (int iter = 0; iter < iterations; iter++) {
        // Nested processing with different keys
        for (int j = 0; j < 5; j++) {
            int key = (iter * j * 16807) & 0xffff;
            transform_array(data, SIZE, key);
            
            // Conditional processing based on checksum
            int checksum = calculate_checksum(data, SIZE);
            if (checksum & 1) {
                for (int k = 0; k < SIZE; k += 2) {
                    data[k] = ~data[k];
                }
            } else {
                for (int k = 1; k < SIZE; k += 2) {
                    data[k] = data[k] >> 1;
                }
            }
        }
        
        // Accumulate results
        result ^= calculate_checksum(data, SIZE);
    }
    
    free(data);
    printf("%d\n", result);
    return 0;
}
