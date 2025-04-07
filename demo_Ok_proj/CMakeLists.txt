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

# Translate .c files to .o object files using TRANSFORMER_PATH
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/opt.o
    COMMAND ${TRANSFORMER_PATH} -O2 -c ${TO_BE_OPTIMIZED_FILES} -o ${CMAKE_CURRENT_BINARY_DIR}/opt.o
    DEPENDS ${TRANSFORMER_PATH} ${TO_BE_OPTIMIZED_FILES}
)

# Create a custom target that depends on the custom command output
add_custom_target(optimized_obj DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/opt.o)

# Make the main target depend on the optimized_obj target
add_dependencies(main optimized_obj)

# Link the object file directly to the main target
target_link_libraries(main ${CMAKE_CURRENT_BINARY_DIR}/opt.o)
