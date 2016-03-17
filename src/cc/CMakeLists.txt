cmake_minimum_required (VERSION 2.6)
project (Thermo2Cli)
set(CMAKE_CXX_FLAGS "-std=c++11")
add_executable(thermo2cli main.cc Api.cc)
