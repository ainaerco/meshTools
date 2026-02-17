# C++ Unit Tests using Google Test

include_directories(${CMAKE_SOURCE_DIR}/src)

# Test executable for geometry tests
add_executable(geometry_tests
    test_vector.cpp
    test_transform.cpp
    test_bbox.cpp
    test_ray.cpp
    test_math.cpp
)

# MSVC does not define M_PI unless _USE_MATH_DEFINES is set
if(MSVC)
  target_compile_definitions(geometry_tests PRIVATE _USE_MATH_DEFINES)
endif()

target_link_libraries(geometry_tests
    geometry
    GTest::gtest_main
)

# Test executable for bezier tests
add_executable(bezier_tests
    test_curves.cpp
)

target_link_libraries(bezier_tests
    bezier
    GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(geometry_tests)
gtest_discover_tests(bezier_tests)
