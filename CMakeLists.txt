cmake_minimum_required(VERSION 3.18)

project (trans LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

if(CMAKE_VERSION VERSION_LESS "3.7.0")
    set(CMAKE_INCLUDE_CURRENT_DIR ON)
endif()

set(QT_MIN_VERSION "5.15.2")

find_package(Qt5 ${QT_MIN_VERSION} CONFIG REQUIRED COMPONENTS
    Core
    Widgets
)

file(GLOB SOURCE_FILE ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB HEADER_FILE ${PROJECT_SOURCE_DIR}/include/*.h)
file(GLOB UI_FILE ${PROJECT_SOURCE_DIR}/ui/*.ui)

include_directories(${PROJECT_SOURCE_DIR}/include)
include_directories(${PROJECT_BINARY_DIR})

find_package(Qt5 COMPONENTS Widgets REQUIRED)
add_executable(${PROJECT_NAME} ${SOURCE_FILE} ${UI_FILE} ${HEADER_FILE})
target_link_libraries(${PROJECT_NAME} Qt5::Widgets Qt5::Core)