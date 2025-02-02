cmake_minimum_required(VERSION 3.10)
project(WiiUseExample)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 11)

# Specify the path to the WiiUse library and include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/wiiuse-lib/src)
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/wiiuse-lib/build/src/Release)

# Define build output directories for executables and libraries
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/build/src/$<CONFIG>")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/build/src/$<CONFIG>")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/build/src/$<CONFIG>")

# Add the executable target
add_executable(main main.cpp)

# Link the wiiuse library (static linking in this case)
target_link_libraries(main wiiuse)
