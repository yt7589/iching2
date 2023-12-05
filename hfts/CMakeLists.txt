cmake_minimum_required(VERSION 3.0)

project(LowLatencyApp)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_COMPILER g++)
set(CMAKE_CXX_FLAGS "-std=c++2a -Wall -Wextra -Werror -Wpedantic")
set(CMAKE_VERBOSE_MAKEFILE on)

add_subdirectory(common)
add_subdirectory(exchange)
add_subdirectory(trading)
add_subdirectory(benchmarks)

list(APPEND LIBS libexchange)
list(APPEND LIBS libtrading)
list(APPEND LIBS libcommon)
list(APPEND LIBS pthread)

include_directories(${PROJECT_SOURCE_DIR})
include_directories(${PROJECT_SOURCE_DIR}/exchange)
include_directories(${PROJECT_SOURCE_DIR}/trading)
include_directories(${PROJECT_SOURCE_DIR}/libs/glog/build/glog)

LINK_DIRECTORIES(
    ${CMAKE_CURRENT_SOURCE_DIR}/../libs/googletest/build/lib
    ${CMAKE_CURRENT_SOURCE_DIR}/../libs/glog/build
    ${CMAKE_CURRENT_SOURCE_DIR}/../apis/sfit/lib/api/ctp
    ${PROJECT_BINARY_DIR}/lib
    /usr/local/lib
    /usr/lib
)
list(APPEND LIBS gtest)
list(APPEND LIBS glog)
list(APPEND LIBS thostmduserapi thosttraderapi)

add_executable(exchange_main exchange/exchange_main.cpp)
target_link_libraries(exchange_main PUBLIC ${LIBS})

add_executable(trading_main trading/trading_main.cpp)
target_link_libraries(trading_main PUBLIC ${LIBS})

add_executable(logger_benchmark benchmarks/logger_benchmark.cpp)
target_link_libraries(logger_benchmark PUBLIC ${LIBS})

add_executable(release_benchmark benchmarks/release_benchmark.cpp)
target_link_libraries(release_benchmark PUBLIC ${LIBS})

add_executable(hash_benchmark benchmarks/hash_benchmark.cpp)
target_link_libraries(hash_benchmark PUBLIC ${LIBS})
