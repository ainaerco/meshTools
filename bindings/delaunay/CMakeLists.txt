include_directories("${CMAKE_SOURCE_DIR}/src")

nanobind_add_module(_delaunay module_delaunay.cpp)
target_link_libraries(_delaunay PRIVATE geometry delaunay)

if(DEFINED SKBUILD)
  set(_ext_install_dir "${SKBUILD_PLATLIB_DIR}/meshTools")
else()
  set(_ext_install_dir scripts)
endif()
install(TARGETS _delaunay
  LIBRARY DESTINATION ${_ext_install_dir}
  RUNTIME DESTINATION ${_ext_install_dir}
)
