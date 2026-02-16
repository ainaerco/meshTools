include_directories(
  "${CMAKE_SOURCE_DIR}"
  "${CMAKE_SOURCE_DIR}/bezier"
)

nanobind_add_module(_bezier module_bezier.cpp)
target_link_libraries(_bezier PRIVATE bezier)

install(TARGETS _bezier
  LIBRARY DESTINATION scripts
  RUNTIME DESTINATION scripts
)
