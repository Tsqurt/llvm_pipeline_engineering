cmake_minimum_required(VERSION 3.10)
project(demo_Ok_proj C)

set(CMAKE_C_COMPILER "clang")

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_executable(main
    main.c
    no_opt.c
    # opt.c
    hidden_numbers.c
)

set(TO_BE_OPTIMIZED_FILES ${CMAKE_CURRENT_SOURCE_DIR}/opt.c)
set(TRANSFORMER_PATH)

if(TO_BE_OPTIMIZED_FILES AND NOT TRANSFORMER_PATH)
    message(FATAL_ERROR "Run \
        \"[PYTHONPATH=...] demo.py --project-dir ${PROJECT_SOURCE_DIR} --output <transformer_path>\" \
        to get a transformer")
endif()

# Translate .c files to .a library using TRANSFORMER_PATH
set(optimized_lib ${CMAKE_CURRENT_BINARY_DIR}/main_opt.a)
add_custom_command(
    OUTPUT ${optimized_lib}
    COMMAND ${TRANSFORMER_PATH} -c ${TO_BE_OPTIMIZED_FILES} -o ${optimized_lib}
    DEPENDS ${TRANSFORMER_PATH} ${TO_BE_OPTIMIZED_FILES}
)
target_link_libraries(main ${optimized_lib})
