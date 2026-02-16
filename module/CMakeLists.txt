include_directories("${CMAKE_SOURCE_DIR}")

# _geometry extension
nanobind_add_module(_geometry module_geometry.cpp)
target_link_libraries(_geometry PRIVATE geometry)

# _mesh extension
nanobind_add_module(_mesh module_mesh.cpp)
target_link_libraries(_mesh PRIVATE geometry mesh)

install(TARGETS _geometry _mesh
  LIBRARY DESTINATION scripts
  RUNTIME DESTINATION scripts
)
