cmake_minimum_required(VERSION 3.10)
project(demo_Ok_proj C)

# 设置C标准
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# 添加可执行文件
add_executable(main
    main.c
    no_opt.c
    opt.c
    hidden_numbers.c
)

# 设置编译器为clang
set(CMAKE_C_COMPILER "clang")
