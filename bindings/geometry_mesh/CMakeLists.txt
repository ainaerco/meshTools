include_directories("${CMAKE_SOURCE_DIR}/src")

# _geometry extension
nanobind_add_module(_geometry module_geometry.cpp)
target_link_libraries(_geometry PRIVATE geometry)

# _mesh extension
nanobind_add_module(_mesh module_mesh.cpp)
target_link_libraries(_mesh PRIVATE geometry mesh)

# When built by scikit-build-core (pip install), install into package dir
if(DEFINED SKBUILD)
  set(_ext_install_dir "${SKBUILD_PLATLIB_DIR}/meshTools")
else()
  set(_ext_install_dir scripts)
endif()
install(TARGETS _geometry _mesh
  LIBRARY DESTINATION ${_ext_install_dir}
  RUNTIME DESTINATION ${_ext_install_dir}
)
