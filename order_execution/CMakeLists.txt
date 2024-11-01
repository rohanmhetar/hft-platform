# order_execution/cpp/CMakeLists.txt

cmake_minimum_required(VERSION 3.10)
project(OrderExecutor)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Boost REQUIRED COMPONENTS system thread)
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

include_directories(${Boost_INCLUDE_DIRS} ${Python3_INCLUDE_DIRS})

add_library(order_executor SHARED order_executor.cpp)

target_link_libraries(order_executor PRIVATE ${Boost_LIBRARIES} ${Python3_LIBRARIES})
