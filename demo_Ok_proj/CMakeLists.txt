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

set(TO_BE_OPTIMIZED_FILES opt.c)
set(TRANSFORMER_PATH)

if(TO_BE_OPTIMIZED_FILES AND NOT TRANSFORMER_PATH)
    message(FATAL_ERROR "Run \
        \"[PYTHONPATH=...] demo.py --project-dir ${PROJECT_SOURCE_DIR} --output <transformer_path>\" \
        to get a transformer")
endif()

function(pipexplore)
    set(options)
    set(oneValueArgs TARGET_NAME)
    set(multiValueArgs CSRC_FILES)
    cmake_parse_arguments(PARSE_ARGV 0 ARG "${options}" "${oneValueArgs}" "${multiValueArgs}")

    # Translate .c files to .o files using TRANSFORMER_PATH
    set(OUTPUT_FILES)
    foreach(csrc_file IN LISTS ARG_CSRC_FILES)
        get_filename_component(csrc_file_name ${csrc_file} NAME_WE)
        set(output_file ${CMAKE_CURRENT_BINARY_DIR}/${csrc_file_name}.o)
        add_custom_command(
            OUTPUT ${output_file}
            COMMAND ${TRANSFORMER_PATH} -c ${CMAKE_CURRENT_SOURCE_DIR}/${csrc_file} -o ${output_file}
            DEPENDS ${TRANSFORMER_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/${csrc_file}
        )
        list(APPEND OUTPUT_FILES ${output_file})
    endforeach()
    add_library(${ARG_TARGET_NAME}_opt STATIC ${OUTPUT_FILES})
    set_target_properties(${ARG_TARGET_NAME}_opt PROPERTIES LINKER_LANGUAGE C)
    target_link_libraries(${ARG_TARGET_NAME} ${ARG_TARGET_NAME}_opt)
endfunction()

pipexplore(TARGET_NAME main CSRC_FILES opt.c)
