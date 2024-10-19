cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(CMAKE_CXX_STANDARD 14)

add_executable(main src/main.cpp)
target_link_libraries(main raylib)
