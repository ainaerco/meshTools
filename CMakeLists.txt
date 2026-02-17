CMAKE_MINIMUM_REQUIRED(VERSION 3.18)
PROJECT(meshTools LANGUAGES CXX)

SET(WINDOWS FALSE)
IF(CMAKE_SYSTEM_NAME MATCHES "Windows")
  SET(WINDOWS TRUE)
  ADD_DEFINITIONS(-DPLATFORM_WINDOWS)
ENDIF()

SET(DARWIN FALSE)
IF(CMAKE_SYSTEM_NAME MATCHES "Darwin")
  SET(DARWIN TRUE)
  IF(NOT CMAKE_SYSTEM_VERSION VERSION_LESS "13.0.0")
    ADD_DEFINITIONS(-std=c++17)
  ENDIF()
ENDIF()

SET(LINUX FALSE)
IF(CMAKE_SYSTEM_NAME MATCHES "Linux")
  SET(LINUX TRUE)
  ADD_DEFINITIONS(-fPIC)
ENDIF()

# Require Python 3.12 and development headers (must be before nanobind)
find_package(Python 3.12 REQUIRED COMPONENTS Interpreter Development.Module)

# Nanobind: fetch and use (replaces Boost.Python)
include(FetchContent)
FetchContent_Declare(
  nanobind
  GIT_REPOSITORY https://github.com/wjakob/nanobind.git
  GIT_TAG        v2.0.0
  GIT_SUBMODULES "ext/robin_map"
)
set(NB_USE_SUBMODULE_DEPS ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(nanobind)
include(${nanobind_SOURCE_DIR}/cmake/nanobind-config.cmake)

# C++17 required by nanobind
set(CMAKE_CXX_STANDARD 17)

include_directories(${Python_INCLUDE_DIRS})

add_subdirectory(src)
add_subdirectory(bindings)
add_subdirectory(python)

# Google Test for C++ unit testing
option(BUILD_TESTS "Build the C++ unit tests" ON)
if(BUILD_TESTS)
  include(FetchContent)
  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.14.0
  )
  # For Windows: Prevent overriding the parent project's compiler/linker settings
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
  FetchContent_MakeAvailable(googletest)
  enable_testing()
  add_subdirectory(tests/cpp)
endif()
