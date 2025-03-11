// 1. GCC 嵌套函数 (Nested Functions)
int outer_function() {
    int x = 10;
    
    int inner_function() {
        return x + 5;  // 可以访问外部函数的变量
    }
    
    return inner_function();
}