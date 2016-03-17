cmake_minimum_required (VERSION 2.6)
project (Thermo2Cli)
set(CMAKE_CXX_FLAGS "-std=c++11")
add_subdirectory(cpr)
add_subdirectory(json)
include_directories(${CPR_INCLUDE_DIRS} ${SRC_DIR}/json/src)
add_executable(thermo2cli main.cc Api.cc)
target_link_libraries(thermo2cli ${CPR_LIBRARIES})

