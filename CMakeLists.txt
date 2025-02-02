cmake_minimum_required(VERSION 3.10)
project(WiiUseExample)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 11)


# add_library(wiimote_controller_lib STATIC wiimote_controller.cpp)

# Specify the path to the WiiUse library and include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/wiiuse/src)
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/wiiuse/build/src/Release)
#target_link_libraries(wiimote_controller_lib PRIVATE ${CONAN_LIBS})

# The lib is in the "src" subdirectory
# add_subdirectory(src)
# Define build output directories for executables and libraries
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/build/src/$<CONFIG>")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/build/src/$<CONFIG>")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/build/src/$<CONFIG>")

# Add the executable target
add_executable(main main.cpp)

# Link the wiiuse library (static linking in this case)
target_link_libraries(main wiiuse)

# Optionally, for dynamic linking with the DLL, make sure the DLL is available at runtime.
# If you want to link against the dynamic library (DLL), use this instead:
# target_link_libraries(main wiiuse.dll)
